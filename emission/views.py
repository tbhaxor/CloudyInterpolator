import os
import sys
from itertools import product
from pathlib import Path
from wsgiref.util import FileWrapper

import h5py
import numpy as np
from django.http import StreamingHttpResponse
from django.shortcuts import render
from django.views.generic import FormView, View

from astrodata.utils import is_server_running

from .forms import InterpolateForm

nH_data, T_data, Z_data, red_data, batch_size, total_size = None, None, None, None, None, None
if is_server_running():
    DATASET_DIR = Path(os.getenv('EMISSION_DATASET_DIR', ''))
    FILE_NAME_TEMPLATE = 'emission.b_{:06d}.h5'
    CHUNK_SIZE = int(os.getenv('DOWNLOAD_CHUNK_SIZE', 1 << 12))

    FIRST_FILE = DATASET_DIR / FILE_NAME_TEMPLATE.format(0)
    if not FIRST_FILE.exists():
        raise FileNotFoundError(f'Batch file \'{FIRST_FILE}\' not found')

    with h5py.File(FIRST_FILE) as file:
        nH_data = np.array(file['params/nH'])
        T_data = np.array(file['params/temperature'])
        Z_data = np.array(file['params/metallicity'])
        red_data = np.array(file['params/redshift'])
        energy = np.array(file['output/energy'])

        batch_size = np.prod(np.array(file['header/batch_dim']))
        total_size = np.prod(np.array(file['header/total_size']))


class InterpolateView(FormView):
    form_class = InterpolateForm
    template_name = 'emission/interpolate.html'

    def _get_nearest_neighbours(self, nH, temperature, metallicity, redshift):
        i_vals, j_vals, k_vals, l_vals = None, None, None, None
        if (np.sum(nH == nH_data) == 1):
            i_vals = [np.where(nH == nH_data)[0][0], np.where(nH == nH_data)[0][0]]
        else:
            i_vals = [np.sum(nH > nH_data)-1, np.sum(nH > nH_data)]

        if (np.sum(temperature == T_data) == 1):
            j_vals = [np.where(temperature == T_data)[0][0], np.where(temperature == T_data)[0][0]]
        else:
            j_vals = [np.sum(temperature > T_data)-1, np.sum(temperature > T_data)]

        if (np.sum(metallicity == Z_data) == 1):
            k_vals = [np.where(metallicity == Z_data)[0][0], np.where(metallicity == Z_data)[0][0]]
        else:
            k_vals = [np.sum(metallicity > Z_data)-1, np.sum(metallicity > Z_data)]

        if (np.sum(redshift == red_data) == 1):
            l_vals = [np.where(redshift == red_data)[0][0], np.where(redshift == red_data)[0][0]]
        else:
            l_vals = [np.sum(redshift > red_data)-1, np.sum(redshift > red_data)]

        return i_vals, j_vals, k_vals, l_vals

    def _get_batch_ids(self, i_vals, j_vals, k_vals, l_vals):
        batches = {}

        # identify unique batches
        for i, j, k, l in product(i_vals, j_vals, k_vals, l_vals):
            if (i == nH_data.shape[0]):
                i = i-1
            if (i == -1):
                i = i+1
            if (j == T_data.shape[0]):
                j = j-1
            if (j == -1):
                j = j+1
            if (k == Z_data.shape[0]):
                k = k-1
            if (k == -1):
                k = k+1
            if (l == red_data.shape[0]):
                l = l-1
            if (l == -1):
                l = l+1
            counter = (l)*Z_data.shape[0]*T_data.shape[0]*nH_data.shape[0] + \
                      (k)*T_data.shape[0]*nH_data.shape[0] + \
                      (j)*nH_data.shape[0] + \
                      (i)
            batch_id = int(counter//batch_size)
            batches[str(batch_id)] = FILE_NAME_TEMPLATE.format(batch_id)
        return batches

    def form_valid(self, form: InterpolateForm):
        data: dict = form.cleaned_data
        i_vals, j_vals, k_vals, l_vals = self._get_nearest_neighbours(
            data.get('nh'),
            data.get('temperature'),
            data.get('metallicity'),
            data.get('redshift'))

        batches = self._get_batch_ids(i_vals, j_vals, k_vals, l_vals)

        return render(self.request, self.template_name, {
            'form': form,
            'batches': batches
        })


class DownloadFileView(View):
    def get(self, request, batch_id: int):
        target_file = DATASET_DIR / FILE_NAME_TEMPLATE.format(batch_id)
        content = FileWrapper(open(target_file, 'rb'), CHUNK_SIZE)
        response = StreamingHttpResponse(content, content_type='application/x-hdf5')
        response['Content-Length'] = target_file.stat().st_size
        response['Content-Disposition'] = f"attachment; filename={target_file.name}"
        return response
