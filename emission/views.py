import os
from pathlib import Path
from typing import Any, Dict

from astro_plasma.core.spectrum import EmissionSpectrum
from django.shortcuts import render
from django.views.generic import FormView, View
from plotly import graph_objs as pgo

from astrodata.base.responses import download_file_response
from astrodata.constants import MODE_TYPES, SESSION_FORM_DATA
from astrodata.utils import is_server_running, is_test_running

from .forms import InterpolateForm

if is_server_running() or is_test_running():
    dataset_base_path = Path(os.getenv("EMISSION_DATASET_DIR"))

    FILE_NAME_TEMPLATE = "ionization.b_{:06d}.h5"


class InterpolateView(FormView):
    form_class = InterpolateForm
    template_name = "emission/interpolation.html"

    def get_form_kwargs(self):
        initial_values: Dict[str, Any] = self.request.session.get(SESSION_FORM_DATA)
        kwargs = {**super().get_form_kwargs(), "data": {}}

        for field in self.form_class():
            v = initial_values.get(field.name, field.initial)
            v = v[0] if type(v) == tuple else v
            v = "{:.1e}".format(v) if type(v) == float else v
            kwargs["data"][field.name] = v
        return kwargs

    def form_invalid(self, form: InterpolateForm):
        is_autofocus = False
        for name, field in form.fields.items():
            if name in form.errors:
                field.widget.attrs = {
                    "class": "is-invalid",
                    "autofocus": "true" if is_autofocus else "false",
                }
                is_autofocus = True

        return super().form_invalid(form)

    def form_valid(self, form: InterpolateForm):
        self.request.session[SESSION_FORM_DATA] = self.request.session.get(SESSION_FORM_DATA, {})
        for field, value in form.cleaned_data.items():
            self.request.session[SESSION_FORM_DATA][field] = value

        emission = EmissionSpectrum(dataset_base_path)
        data_0 = emission.interpolate_spectrum(**{**form.cleaned_data, "mode": MODE_TYPES[0][0]})
        data_1 = emission.interpolate_spectrum(**{**form.cleaned_data, "mode": MODE_TYPES[1][0]})

        fig = pgo.Figure(
            data=[
                pgo.Scatter(x=data_0[:, 0], y=data_0[:, 1], mode="lines", name=f"{MODE_TYPES[0][1]} ({MODE_TYPES[0][0]})"),
                pgo.Scatter(x=data_1[:, 0], y=data_1[:, 1], mode="lines", name=f"{MODE_TYPES[1][1]} ({MODE_TYPES[1][0]})"),
            ]
        )
        fig.update_xaxes(title_text=r"Energy (keV)", type="log")
        fig.update_yaxes(title_text=r"Emissivity (erg cm<sup>-3</sup> s<sup>-1</sup>)", type="log")

        fig.update_layout(width=1200, height=900, legend={"x": 0, "y": 1, "bgcolor": "rgba(0,0,0,0)"})

        return render(self.request, self.template_name, {"form": form, "interpolation": fig.to_json()})


class DownloadFileView(View):
    def get(self, request, batch_id: int):
        target_file = dataset_base_path / FILE_NAME_TEMPLATE.format(batch_id)
        return download_file_response(target_file)
