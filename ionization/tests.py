from django.test import TestCase

from .forms import InterpolateIonFractionForm, InterpolateMDForm


class TestInterpolateIonFractionForm(TestCase):
    def test_invalid_element(self):
        form = InterpolateIonFractionForm(data={'element': 0})
        assert form.is_bound, 'Form is not bounded to data'
        assert not form.is_valid(), 'Invalid field, but form is valid'
        assert form.has_error('element'), 'Unable to find error in element field'

        error, *_sink = form.errors.get_json_data().get('element')

        assert error['code'] == 'invalid_choice', 'Invalid error code'

    def test_invalid_ion_count(self):
        form = InterpolateIonFractionForm(data={'element': 1, 'ion': 0})
        assert form.is_bound, 'Form is not bounded to data'
        assert not form.is_valid(), 'Invalid field, but form is valid'
        assert form.has_error('ion'), 'Unable to find error in element field'

        error, *_sink = form.errors.get_json_data().get('ion')
        assert error['code'] == 'min_value', 'Invalid error code'

    def test_ion_greater_than_element_plus_1(self):
        form = InterpolateIonFractionForm(data={'element': 1, 'ion': 3})
        assert form.is_bound, 'Form is not bounded to data'
        assert not form.is_valid(), 'Invalid field, but form is valid'
        assert form.has_error('ion'), 'Unable to find error in element field'

        error, *_sink = form.errors.get_json_data().get('ion')
        assert error['code'] == 'gt_element', 'Invalid error code'


class TestInterpolateMDForm(TestCase):
    def test_invalid_species_type(self):
        form = InterpolateMDForm(data={'species_type': 'hello world'})
        assert form.is_bound, 'Form is not bounded to data'
        assert not form.is_valid(), 'Invalid field, but form is valid'
        assert form.has_error('species_type'), 'Unable to find error in element field'

        error, *_sink = form.errors.get_json_data().get('species_type')
        assert error['code'] == 'invalid_choice', 'Invalid error code'
    pass
