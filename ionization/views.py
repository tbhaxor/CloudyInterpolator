import json
import os
from pathlib import Path
from wsgiref.util import FileWrapper

from astro_plasma import Ionization
from django.http import JsonResponse, StreamingHttpResponse
from django.shortcuts import render
from django.views.generic import FormView, View

from astrodata.utils import is_server_running

from .forms import InterpolateForm

if is_server_running():
    dir_path = os.getenv('IONIZATION_DATASET_DIR')
    if dir_path is None:
        raise ValueError('Ionization dataset directory is required')
    dataset_base_path = Path(dir_path)
    ionization = Ionization(base_dir=dataset_base_path)

    CHUNK_SIZE = int(os.getenv('DOWNLOAD_CHUNK_SIZE', 1 << 12))
    FILE_NAME_TEMPLATE = 'ionization.b_{:06d}.h5'


class Interpolation(FormView):
    form_class = InterpolateForm
    template_name = 'ionization/interpolation.html'

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
        ion_frac = ionization.interpolateIonFrac(nH=form.cleaned_data['nh'],
                                                 temperature=form.cleaned_data['temperature'],
                                                 metallicity=form.cleaned_data['metallicity'],
                                                 element=form.cleaned_data['element'],
                                                 ion=form.cleaned_data['ion'],
                                                 mode=form.cleaned_data['mode'],
                                                 redshift=form.cleaned_data['redshift'])

        mu_mass = ionization.interpolateMu(nH=form.cleaned_data['nh'],
                                           temperature=form.cleaned_data['temperature'],
                                           metallicity=form.cleaned_data['metallicity'],
                                           mode=form.cleaned_data['mode'],
                                           redshift=form.cleaned_data['redshift']
                                           )
        nrho = ionization.interpolateNumDens(nH=form.cleaned_data['nh'],
                                             temperature=form.cleaned_data['temperature'],
                                             metallicity=form.cleaned_data['metallicity'],
                                             mode=form.cleaned_data['mode'],
                                             redshift=form.cleaned_data['redshift'],
                                             part_type=form.cleaned_data['species_type'])

        interpolation = {
            'ion_frac': ion_frac,
            'mu_mass': mu_mass,
            'number_density': nrho
        }

        if self.request.GET.get('format') == 'json':
            return JsonResponse(data={'data': interpolation, 'request': form.cleaned_data})

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
