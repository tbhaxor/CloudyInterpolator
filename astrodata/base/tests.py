from django.test import TestCase

from .forms import InterpolateForm


class TestInterpolationForm(TestCase):
    def test_failure_on_empty_form(self):
        form = InterpolateForm(data={})
        assert not form.is_valid(), "Empty form is valid"

        for field in form.fields:
            assert form.has_error(field), f"Field {field} suppose to have error"

            error, *_sink = form.errors.get_json_data().get(field)
            assert error["code"] == "required", f"Invalid error code for field {field}"

    def test_invalid_nH(self):
        form = InterpolateForm(data={"nH": "hello world"})
        assert form.is_bound, "Form is not bounded to data"
        assert not form.is_valid(), "Invalid field, but form is valid"
        assert form.has_error("nH"), "Unable to find error in element field"

        error, *_sink = form.errors.get_json_data().get("nH")
        assert error["code"] == "invalid", "Invalid error code"

    def test_invalid_mode(self):
        form = InterpolateForm(data={"mode": "HELLO"})
        assert form.is_bound, "Form is not bounded to data"
        assert not form.is_valid(), "Invalid field, but form is valid"
        assert form.has_error("mode"), "Unable to find error in element field"

        error, *_sink = form.errors.get_json_data().get("mode")
        assert error["code"] == "invalid_choice", "Invalid error code"

    def test_invalid_temperature(self):
        form = InterpolateForm(data={"temperature": "hello world"})
        assert form.is_bound, "Form is not bounded to data"
        assert not form.is_valid(), "Invalid field, but form is valid"
        assert form.has_error("temperature"), "Unable to find error in element field"

        error, *_sink = form.errors.get_json_data().get("temperature")
        assert error["code"] == "invalid", "Invalid error code"

    def test_invalid_metallicity(self):
        form = InterpolateForm(data={"metallicity": "hello world"})
        assert form.is_bound, "Form is not bounded to data"
        assert not form.is_valid(), "Invalid field, but form is valid"
        assert form.has_error("metallicity"), "Unable to find error in element field"

        error, *_sink = form.errors.get_json_data().get("metallicity")
        assert error["code"] == "invalid", "Invalid error code"

    def test_invalid_redshift(self):
        form = InterpolateForm(data={"redshift": "hello world"})
        assert form.is_bound, "Form is not bounded to data"
        assert not form.is_valid(), "Invalid field, but form is valid"
        assert form.has_error("redshift"), "Unable to find error in element field"

        error, *_sink = form.errors.get_json_data().get("redshift")
        assert error["code"] == "invalid", "Invalid error code"
