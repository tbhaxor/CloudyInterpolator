from django.test import TestCase

from astrodata.base.forms import InterpolateForm


class TestInterpolateForm(TestCase):
    def test_failure_on_empty_form(self):
        form = InterpolateForm(data={})
        assert not form.is_valid(), 'Empty form is valid'

        for field in form.fields:
            assert form.has_error(field), f'Field {field} suppose to have error'
            error, *_sink = form.errors.get_json_data().get(field)

            assert error['code'] == 'required', f'Invalid error code for field {field}'

    def test_invalid_nh(self):
        form = InterpolateForm(data={'nh': 'hello world'})
        assert form.is_bound, 'Form is not bounded to data'
        assert not form.is_valid(), 'Invalid field, but form is valid'
        assert form.has_error('nh'), 'Unable to find error in element field'

        error, *_sink = form.errors.get_json_data().get('nh')
        assert error['code'] == 'invalid', 'Invalid error code'

    def test_invalid_mode(self):
        form = InterpolateForm(data={'mode': 'HELLO'})
        assert form.is_bound, 'Form is not bounded to data'
        assert not form.is_valid(), 'Invalid field, but form is valid'

        error, *_sink = form.errors.get_json_data().get('mode')
        assert error['code'] == 'invalid_choice', 'Invalid error code'

    def test_invalid_temperature(self):
        form = InterpolateForm(data={'temperature': 'hello world'})
        assert form.is_bound, 'Form is not bounded to data'
        assert not form.is_valid(), 'Invalid field, but form is valid'
        assert form.has_error('temperature'), 'Unable to find error in element field'

        error, *_sink = form.errors.get_json_data().get('temperature')
        assert error['code'] == 'invalid', 'Invalid error code'

    def test_invalid_metallicity(self):
        form = InterpolateForm(data={'metallicity': 'hello world'})
        assert form.is_bound, 'Form is not bounded to data'
        assert not form.is_valid(), 'Invalid field, but form is valid'
        assert form.has_error('metallicity'), 'Unable to find error in element field'

        error, *_sink = form.errors.get_json_data().get('metallicity')
        assert error['code'] == 'invalid', 'Invalid error code'

    def test_invalid_redshift(self):
        form = InterpolateForm(data={'redshift': 'hello world'})
        assert form.is_bound, 'Form is not bounded to data'
        assert not form.is_valid(), 'Invalid field, but form is valid'
        assert form.has_error('redshift'), 'Unable to find error in element field'

        error, *_sink = form.errors.get_json_data().get('redshift')
        assert error['code'] == 'invalid', 'Invalid error code'


"""
TODO: implement this when server is live
class TestInterpolateView(TestCase):
    def setUp(self) -> None:
        self.emission = EmissionSpectrum(base_dir=os.getenv('EMISSION_DATASET_DIR'))
        self.url = reverse('emission:interpolation')
        self.client = Client(enforce_csrf_checks=False)
        return super().setUp()

    def test_valid_inputs(self):
        response = self.client.post(self.url, data={
            'nh': self.emission.nH_data[0],
            'mode': MODE_TYPES[0][0],
            'temperature': self.emission.T_data[0],
            'redshift': self.emission.red_data[0],
            'metallicity': self.emission.Z_data[0],
        })

        interpolation = response.context.get('interpolation')
        assert interpolation is not None, 'Interpolation data key is missing in context'
        assert type(interpolation) == dict, 'Interpolation data should be of dict type'
        assert 'data' in interpolation, '"data" key is missing in interpolation'
"""
