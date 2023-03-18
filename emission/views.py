import json
import os
from pathlib import Path
from wsgiref.util import FileWrapper

from astro_plasma import EmissionSpectrum
from django.http import JsonResponse, StreamingHttpResponse
from django.shortcuts import render
from django.views.generic import FormView, View

from astrodata.base.forms import InterpolateForm
from astrodata.utils import is_server_running

if is_server_running():
    dir_path = os.getenv('EMISSION_DATASET_DIR')
    if dir_path is None:
        raise ValueError('Emission dataset directory is required')
    dataset_base_path = Path(dir_path)

    CHUNK_SIZE = int(os.getenv('DOWNLOAD_CHUNK_SIZE', 1 << 12))
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
                    'class': f"{field.widget.attrs.get('class', '')} is-invalid".strip(),
                    'autofocus': 'true' if is_autofocus else 'false'
                }
                is_autofocus = True

        return super().form_invalid(form)

    def form_valid(self, form: InterpolateForm):
        print("valid form")
        emission = EmissionSpectrum(dataset_base_path)
        print(emission)
        data = emission.interpolate(nH=form.cleaned_data['nh'],
                                    metallicity=form.cleaned_data['metallicity'],
                                    mode=form.cleaned_data['mode'],
                                    redshift=form.cleaned_data['redshift'],
                                    temperature=form.cleaned_data['temperature'])
        interpolation = {
            'data': data,
        }

        if self.request.GET.get('format') == 'json':
            return JsonResponse(data={'data': interpolation, 'request': form.cleaned_data})

        print(interpolation)
        context = {'form': form,
                   'interpolation': interpolation}
        return render(self.request, self.template_name, context)


class DownloadFileView(View):
    def get(self, request, batch_id: int):
        target_file = dataset_base_path / FILE_NAME_TEMPLATE.format(batch_id)
        content = FileWrapper(open(target_file, 'rb'), CHUNK_SIZE)
        response = StreamingHttpResponse(content, content_type='application/x-hdf5')
        response['Content-Length'] = target_file.stat().st_size
        response['Content-Disposition'] = f"attachment; filename={target_file.name}"
        return response
