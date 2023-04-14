import os
from copy import deepcopy
from wsgiref.util import FileWrapper

import numpy as np
import plotly.graph_objects as pgo
import roman
from astro_plasma.core.ionization import Ionization
from django.http import HttpRequest, StreamingHttpResponse
from django.shortcuts import redirect, render
from django.views.generic import TemplateView, View

from astrodata.utils import is_server_running, is_test_running

from .forms import PARMANU, InterpolateIonFracTemperatureForm, InterpolateIonFractionForm, InterpolateMDForm

if is_server_running() or is_test_running():
    dataset_base_path = os.getenv('IONIZATION_DATASET_DIR')

    CHUNK_SIZE = int(os.getenv('DOWNLOAD_CHUNK_SIZE', 1 << 12))
    FILE_NAME_TEMPLATE = 'ionization.b_{:06d}.h5'


class InterpolationView(TemplateView):
    template_name = 'ionization/interpolation.html'

    def get(self, request, *args, **kwargs):
        if request.GET.get('action') is None:
            return redirect(request.path + '?action=ion_frac')
        kwargs['action'] = request.GET.get('action')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        match kwargs.get('action'):
            case 'ion_frac':
                kwargs['form'] = InterpolateIonFractionForm()
            case 'plot_ion_frac':
                kwargs['form'] = InterpolateIonFracTemperatureForm()
            case 'mass_density':
                kwargs['form'] = InterpolateMDForm()
        return super().get_context_data(**kwargs)

    def post(self, request: HttpRequest):
        action = request.GET.get('action')
        match action:
            case 'ion_frac':
                form = InterpolateIonFractionForm(request.POST)
            case 'plot_ion_frac':
                form = InterpolateIonFracTemperatureForm(request.POST)
            case 'mass_density':
                form = InterpolateMDForm(request.POST)
            case _:
                return redirect(request.path + '?action=ion_frac')

        if not form.is_valid():
            is_autofocus = False
            for name, field in form.fields.items():
                if name in form.errors:
                    field.widget.attrs = {
                        'class': f"{field.widget.attrs.get('class', '')} is-invalid".strip(),
                        'autofocus': 'true' if is_autofocus else 'false',
                    }
                    is_autofocus = True
            return render(request, self.template_name, {'form': form, 'action': action})

        interpolation_data = {}
        i = Ionization(dataset_base_path)
        match action:
            case 'ion_frac':
                i.interpolate_ion_frac()
                interpolation_data['ion_frac'] = "{:.4e}".format(10**i.interpolate_ion_frac(**form.cleaned_data))
                symbol = PARMANU.getElSymbol(form.cleaned_data['element'])
                roman_ion = roman.toRoman(form.cleaned_data['ion'])
                interpolation_data['ionized_symbol'] = f'{symbol}{roman_ion}'
            case 'plot_ion_frac':
                temp_range = form.cleaned_data['temperature_stop'] - form.cleaned_data['temperature_start']
                space_num = round(temp_range / form.cleaned_data['temperature_step'] + 1)

                temp_array = np.logspace(
                    form.cleaned_data['temperature_start'],
                    form.cleaned_data['temperature_stop'],
                    space_num)

                fIon_input = deepcopy(form.cleaned_data)
                del fIon_input['temperature_start']
                del fIon_input['temperature_stop']
                del fIon_input['temperature_step']

                fIon_output = []
                for temp in temp_array:
                    fIon_input['temperature'] = temp
                    fIon_output.append(10**i.interpolate_ion_frac(**fIon_input))

                fig = pgo.Figure(data=[
                    pgo.Scatter(x=temp_array, y=fIon_output, mode='lines'),
                ])

                symbol = PARMANU.getElSymbol(form.cleaned_data['element'])
                roman_ion = roman.toRoman(form.cleaned_data['ion'])

                fig.update_xaxes(title_text='Temperature (Kelvin)',  type='log')
                fig.update_yaxes(title_text=f'Ion Fraction ({symbol}{roman_ion})', type='log')

                fig.update_layout(width=1200,
                                  height=900,
                                  legend={'x': 0, 'y': 1, 'bgcolor': 'rgba(0,0,0,0)'})
                interpolation_data = fig.to_json()

            case 'mass_density':
                form.cleaned_data['part_type'] = form.cleaned_data['species_type']
                del form.cleaned_data['species_type']

                mean_mass = i.interpolate_mu(**form.cleaned_data)
                number_density = i.interpolate_num_dens(**form.cleaned_data)

                interpolation_data['mean_mass'] = "{:.4e}".format(mean_mass)
                interpolation_data['number_density'] = "{:.4e}".format(number_density)

                interpolation_data['mean_mass_symbol'] = '&mu;'
                interpolation_data['number_density_symbol'] = 'n'
                match form.cleaned_data['part_type']:
                    case 'ion':
                        interpolation_data['mean_mass_symbol'] += '<sub>i</sub>'
                        interpolation_data['number_density_symbol'] += '<sub>i</sub>'
                    case 'electron':
                        interpolation_data['mean_mass_symbol'] += '<sub>e</sub>'
                        interpolation_data['number_density_symbol'] += '<sub>e</sub>'

        return render(request, self.template_name,
                      {'form': form, 'action': action, 'interpolation': interpolation_data})


class DownloadFileView(View):
    def get(self, request, batch_id: int):
        target_file = dataset_base_path / FILE_NAME_TEMPLATE.format(batch_id)
        content = FileWrapper(open(target_file, 'rb'), CHUNK_SIZE)
        response = StreamingHttpResponse(content, content_type='application/x-hdf5')
        response['Content-Length'] = target_file.stat().st_size
        response['Content-Disposition'] = f'attachment; filename={target_file.name}'
        return response
