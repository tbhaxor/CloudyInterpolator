import json
import os
from pathlib import Path

from astro_plasma.core.spectrum import EmissionSpectrum
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import FormView, View
from plotly import graph_objs as pgo

from astrodata.base.forms import InterpolateForm
from astrodata.base.responses import download_file_response
from astrodata.utils import is_server_running, is_test_running

if is_server_running() or is_test_running():
    dataset_base_path = Path(os.getenv('EMISSION_DATASET_DIR'))

    FILE_NAME_TEMPLATE = 'ionization.b_{:06d}.h5'


class InterpolateView(FormView):
    form_class = InterpolateForm
    template_name = 'emission/interpolation.html'

    def form_invalid(self, form: InterpolateForm):
        if self.request.GET.get('format') == 'json':
            errors = json.loads(form.errors.as_json())
            errors = {'errors': errors}
            return JsonResponse(data=errors, status=400)

        is_autofocus = False
        for name, field in form.fields.items():
            if name in form.errors:
                field.widget.attrs = {
                    'class': 'is-invalid',
                    'autofocus': 'true' if is_autofocus else 'false',
                }
                is_autofocus = True

        return super().form_invalid(form)

    def form_valid(self, form: InterpolateForm):
        emission = EmissionSpectrum(dataset_base_path)
        data_linear = emission.interpolate_spectrum(**form.cleaned_data)

        fig = pgo.Figure(data=[
            pgo.Scatter(x=data_linear[:, 0], y=data_linear[:, 1], mode='lines'),
        ])
        fig.update_xaxes(title_text=r'Energy (keV)', type='log')
        fig.update_yaxes(title_text=r'Emissivity (erg cm<sup>-3</sup> s<sup>-1</sup>)', type='log')

        fig.update_layout(width=1200,
                          height=900,
                          legend={'x': 0, 'y': 1, 'bgcolor': 'rgba(0,0,0,0)'})

        # with StringIO() as file:

        if self.request.GET.get('format') == 'json':
            return JsonResponse(data={'data': {
                'energy': data_linear[:, 0],
                'emissivity_linear': data_linear[:, 1],
            }, 'request': form.cleaned_data})

        context = {'form': form,
                   'interpolation': fig.to_json()}
        return render(self.request, self.template_name, context)


class DownloadFileView(View):
    def get(self, request, batch_id: int):
        target_file = dataset_base_path / FILE_NAME_TEMPLATE.format(batch_id)
        return download_file_response(target_file)
