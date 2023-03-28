import os

from astro_plasma import Ionization
from django.test import Client, TestCase
from django.urls import reverse

from .forms import MODE_TYPES, SPECIES_TYPES, TATVAS, InterpolateForm


class TestInterpolationForm(TestCase):

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

    def test_invalid_element(self):
        form = InterpolateForm(data={'element': 0})
        assert form.is_bound, 'Form is not bounded to data'
        assert not form.is_valid(), 'Invalid field, but form is valid'
        assert form.has_error('element'), 'Unable to find error in element field'

        error, *_sink = form.errors.get_json_data().get('element')

        assert error['code'] == 'invalid_choice', 'Invalid error code'

    def test_invalid_ion_count(self):
        form = InterpolateForm(data={'element': 1, 'ion': 0})
        assert form.is_bound, 'Form is not bounded to data'
        assert not form.is_valid(), 'Invalid field, but form is valid'
        assert form.has_error('ion'), 'Unable to find error in element field'

        error, *_sink = form.errors.get_json_data().get('ion')
        assert error['code'] == 'min_value', 'Invalid error code'

    def test_ion_greater_than_element_plus_1(self):
        form = InterpolateForm(data={'element': 1, 'ion': 3})
        assert form.is_bound, 'Form is not bounded to data'
        assert not form.is_valid(), 'Invalid field, but form is valid'
        assert form.has_error('ion'), 'Unable to find error in element field'

        error, *_sink = form.errors.get_json_data().get('ion')
        assert error['code'] == 'gt_element', 'Invalid error code'

    def test_invalid_mode(self):
        form = InterpolateForm(data={'mode': 'HELLO'})
        assert form.is_bound, 'Form is not bounded to data'
        assert not form.is_valid(), 'Invalid field, but form is valid'
        assert form.has_error('mode'), 'Unable to find error in element field'

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

    def test_invalid_species_type(self):
        form = InterpolateForm(data={'species_type': 'hello world'})
        assert form.is_bound, 'Form is not bounded to data'
        assert not form.is_valid(), 'Invalid field, but form is valid'
        assert form.has_error('species_type'), 'Unable to find error in element field'

        error, *_sink = form.errors.get_json_data().get('species_type')
        assert error['code'] == 'invalid_choice', 'Invalid error code'


class TestInterpolateView(TestCase):
    def setUp(self) -> None:
        self.ionization = Ionization(base_dir=os.getenv('IONIZATION_DATASET_DIR'))
        self.url = reverse('ionization:interpolation')
        self.client = Client(enforce_csrf_checks=False)
        return super().setUp()

    def test_valid_input(self):
        response = self.client.post(self.url, data={
            'nh': self.ionization.nH_data[0],
            'mode': MODE_TYPES[0][0],
            'temperature': self.ionization.T_data[0],
            'redshift': self.ionization.red_data[0],
            'metallicity': self.ionization.Z_data[0],
            'element': TATVAS[0][0],
            'species_type': SPECIES_TYPES[0][0],
            'ion': 1,
        })

        interpolation: dict = response.context.get('interpolation')
        assert interpolation is not None, 'Interpolation data key is missing in context'
        assert 'ion_frac' in interpolation, '"ion_frac" key does not exists in interpolation data'
        assert 'mu_mass' in interpolation, '"mu_mass" key does not exists in interpolation data'
        assert 'number_density' in interpolation, '"number_density" key does not exists in interpolation data'

        for property, value in interpolation.items():
            assert type(value) == float, f'"{property}" has invalid type {type(value).__name__}'
            # pass
