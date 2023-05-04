import os
from copy import deepcopy
from pathlib import Path
from typing import Any, Dict

import numpy as np
import plotly.graph_objects as pgo
import roman
from astro_plasma.core.ionization import Ionization
from django.forms import BaseForm
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.views.generic import TemplateView, View

from astrodata.base.responses import download_file_response
from astrodata.constants import MODE_TYPES, PARMANU, SESSION_FORM_DATA, SESSION_INTERPOLATE_MD_MISC_DATA
from astrodata.utils import is_server_running, is_test_running

from .forms import InterpolateIonFracForm, InterpolateIonFracTemperatureForm, InterpolateMDForm

if is_server_running() or is_test_running():
    dataset_base_path = Path(os.getenv("IONIZATION_DATASET_DIR"))
    FILE_NAME_TEMPLATE = "ionization.b_{:06d}.h5"


class InterpolationView(TemplateView):
    template_name = "ionization/interpolation.html"

    def get(self, request, *args, **kwargs):
        if request.GET.get("action") is None:
            return redirect(request.path + "?action=ion_frac")
        kwargs["action"] = request.GET.get("action")
        return super().get(request, *args, **kwargs)

    def get_form_class(self, action: str):
        match action:
            case "ion_frac":
                return InterpolateIonFracForm
            case "plot_ion_frac":
                return InterpolateIonFracTemperatureForm
            case "mass_density":
                return InterpolateMDForm

    def get_form_initials(self, action: str) -> Dict[str, Any]:
        initial_values: Dict[str, Any] = self.request.session.get(SESSION_FORM_DATA, {})
        md_form_ini_vals: Dict[str, Any] = self.request.session.get(SESSION_INTERPOLATE_MD_MISC_DATA, {})
        data = {}

        form: BaseForm = self.get_form_class(action)()
        for field in form:
            if field.name in md_form_ini_vals:
                v = md_form_ini_vals.get(field.name, field.initial)
            else:
                v = initial_values.get(field.name, field.initial)
            v = v[0] if type(v) == tuple else "{:.1e}".format(v) if type(v) == float else v
            data[field.name] = v

        return data

    def get_form(self, action: str) -> BaseForm:
        return self.get_form_class(action)(data=self.get_form_initials(action))

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        kwargs["form"] = self.get_form(kwargs["action"])
        return super().get_context_data(**kwargs)

    def post(self, request: HttpRequest):
        action = request.GET.get("action")
        form = self.get_form_class(action)(request.POST)

        if not form.is_valid():
            is_autofocus = False
            for name, field in form.fields.items():
                if name in form.errors:
                    field.widget.attrs = {
                        "class": "is-invalid",
                        "autofocus": "true" if is_autofocus else "false",
                    }
                    is_autofocus = True
            return render(request, self.template_name, {"form": form, "action": action})

        self.request.session[SESSION_FORM_DATA] = self.request.session.get(SESSION_FORM_DATA, {})
        self.request.session[SESSION_INTERPOLATE_MD_MISC_DATA] = self.request.session.get(SESSION_INTERPOLATE_MD_MISC_DATA, {})
        for k, v in form.cleaned_data.items():
            if v is None and action == "mass_density":
                self.request.session[SESSION_INTERPOLATE_MD_MISC_DATA][k] = v
            self.request.session[SESSION_FORM_DATA][k] = v

        interpolation_data = {}
        i = Ionization(dataset_base_path)
        match action:
            case "ion_frac":
                i.interpolate_ion_frac()
                interpolation_data["ion_frac"] = "{:.4e}".format(10 ** i.interpolate_ion_frac(**form.cleaned_data))
                symbol = PARMANU.getElSymbol(form.cleaned_data["element"])
                roman_ion = roman.toRoman(form.cleaned_data["ion"])
                interpolation_data["ionized_symbol"] = f"{symbol}{roman_ion}"
            case "plot_ion_frac":
                temp_array = np.linspace(
                    start=form.cleaned_data["temperature_start"],
                    stop=form.cleaned_data["temperature_stop"],
                    num=form.cleaned_data["temperature_bins"],
                )

                fIon_input = deepcopy(form.cleaned_data)
                del fIon_input["temperature_start"]
                del fIon_input["temperature_stop"]
                del fIon_input["temperature_bins"]

                fIon_input_0 = deepcopy({**fIon_input, "mode": MODE_TYPES[0][0]})
                fIon_input_1 = deepcopy({**fIon_input, "mode": MODE_TYPES[1][0]})
                fIon_output_PIE = []
                fIon_output_CIE = []

                for temp in temp_array:
                    fIon_input_0["temperature"] = temp
                    fIon_input_1["temperature"] = temp

                    fIon_output_PIE.append(10 ** i.interpolate_ion_frac(**fIon_input_0))
                    fIon_output_CIE.append(10 ** i.interpolate_ion_frac(**fIon_input_1))

                fig = pgo.Figure(
                    data=[
                        pgo.Scatter(x=temp_array, y=fIon_output_CIE, mode="lines", name=MODE_TYPES[0][1]),
                        pgo.Scatter(x=temp_array, y=fIon_output_PIE, mode="lines", name=MODE_TYPES[1][1]),
                    ]
                )

                symbol = PARMANU.getElSymbol(form.cleaned_data["element"])
                roman_ion = roman.toRoman(form.cleaned_data["ion"])

                fig.update_xaxes(title_text="Temperature (Kelvin)", type="log")
                fig.update_yaxes(title_text=f"Ion Fraction ({symbol}{roman_ion})", type="log")

                fig.update_layout(width=1200, height=900, legend={"x": 0, "y": 1, "bgcolor": "rgba(0,0,0,0)"})
                interpolation_data = fig.to_json()

            case "mass_density":
                form.cleaned_data["part_type"] = form.cleaned_data["species_type"]
                del form.cleaned_data["species_type"]

                mu_mass_input = deepcopy(form.cleaned_data)
                del mu_mass_input["element"]
                del mu_mass_input["ion"]

                num_density_input = deepcopy(form.cleaned_data)
                if num_density_input["element"] is not None:
                    del num_density_input["part_type"]
                else:
                    del num_density_input["element"]
                    del num_density_input["ion"]

                mean_mass = i.interpolate_mu(**mu_mass_input)
                number_density = i.interpolate_num_dens(**num_density_input)

                interpolation_data["mean_mass"] = "{:.4e}".format(mean_mass)
                interpolation_data["number_density"] = "{:.4e}".format(number_density)

                interpolation_data["mean_mass_symbol"] = "&mu;"
                interpolation_data["number_density_symbol"] = "n"
                match form.cleaned_data["part_type"]:
                    case "ion":
                        interpolation_data["mean_mass_symbol"] += "<sub>i</sub>"
                        interpolation_data["number_density_symbol"] += "<sub>i</sub>"
                    case "electron":
                        interpolation_data["mean_mass_symbol"] += "<sub>e</sub>"
                        interpolation_data["number_density_symbol"] += "<sub>e</sub>"

        return render(request, self.template_name, {"form": form, "action": action, "interpolation": interpolation_data})


class DownloadFileView(View):
    def get(self, request, batch_id: int):
        target_file = dataset_base_path / FILE_NAME_TEMPLATE.format(batch_id)
        return download_file_response(target_file)
