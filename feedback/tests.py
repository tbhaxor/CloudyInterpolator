from urllib.parse import parse_qs, urlparse

from django.test import Client, TestCase
from django.urls import reverse_lazy

from .forms import FeedbackForm


# Create your tests here.
class TestSubmissionForm(TestCase):
    def test_all_empty(self):
        form = FeedbackForm(data={})
        assert form.is_bound, "Form is not bounded to data"
        assert not form.is_valid(), "Invalid field, but form is valid"

        for field in form.fields:
            assert form.has_error(field), "Unable to find error in element field"
            error, *_sink = form.errors.get_json_data().get(field)
            assert error["code"] == "required", f"Invalid error code for field {field}"

    def test_empty_name(self):
        form = FeedbackForm(
            data={
                "name": "",
                "message": "hello world",
                "email": "test@example.com",
            }
        )
        assert form.is_bound, "Form is not bounded to data"
        assert not form.is_valid(), "Invalid field, but form is valid"
        assert form.has_error("name"), '"name" should have error'
        assert form.errors.as_data()["name"][0].code == "required", "Invalid error code"

    def test_empty_email(self):
        form = FeedbackForm(
            data={
                "name": "hello world",
                "message": "hello world",
                "email": "",
            }
        )
        assert form.is_bound, "Form is not bounded to data"
        assert not form.is_valid(), "Invalid field, but form is valid"
        assert form.has_error("email"), '"email" should have error'
        assert (
            form.errors.as_data()["email"][0].code == "required"
        ), "Invalid error code"

    def test_empty_message(self):
        form = FeedbackForm(
            data={
                "name": "hello world",
                "message": "",
                "email": "test@example.com",
            }
        )
        assert form.is_bound, "Form is not bounded to data"
        assert not form.is_valid(), "Invalid field, but form is valid"
        assert form.has_error("message"), '"message" should have error'
        assert (
            form.errors.as_data()["message"][0].code == "required"
        ), "Invalid error code"

    def test_invalid_email(self):
        form = FeedbackForm(
            data={
                "name": "hello world",
                "message": "hello world",
                "email": "hello world",
            }
        )
        assert form.is_bound, "Form is not bounded to data"
        assert not form.is_valid(), "Invalid field, but form is valid"
        assert form.has_error("email"), '"email" should have error'
        assert form.errors.as_data()["email"][0].code == "invalid", "Invalid error code"

    def test_valid_inputs(self):
        form = FeedbackForm(
            data={
                "name": "hello world",
                "message": "hello world",
                "email": "test@example.com",
            }
        )

        assert form.is_bound, "Form is not bounded to data"
        assert form.is_valid(), "Form should be valid"


class TestSubmissionFormView(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=False)
        return super().setUp()

    def test_error_on_invalid_form(self):
        payload = {
            "name": "hello world",
            "email": "test@email.com",
            "message": "some message",
        }

        for k, v in payload.items():
            response = self.client.post(reverse_lazy("feedback:submit"), data={k: v})

            assert response.status_code == 200, "Response code should be 200"
            assert response.get("location") is None, "Redirect location should be None"
            assert "form" in response.context, 'Context should have "form" with errors'

    def test_redirect_on_success(self):
        response = self.client.post(
            reverse_lazy("feedback:submit"),
            data={
                "name": "hello world",
                "email": "test@email.com",
                "message": "some message",
            },
        )

        assert response.status_code == 302, "Couldn't find redirect status code"

        location = response.get("location")
        assert location is not None, "Redirection url is not set"

        location_parsed = urlparse(location)
        assert location_parsed.path == reverse_lazy(
            "feedback:thank-you"
        ), "Invalid redirection path"

        parsed_qs = parse_qs(location_parsed.query)
        assert "name" in parsed_qs, '"name" is required in query parameter'
        assert (
            parsed_qs["name"][0] == "hello world"
        ), '"name" should be same as submission'


class TestThankyouView(TestCase):
    def test_redirect_if_no_name(self):
        response = self.client.get(reverse_lazy("feedback:thank-you"))
        assert response.status_code == 302, "Invalid redirect status"

        location = response.get("location")
        assert location == reverse_lazy(
            "feedback:submit"
        ), "Redirection is not to the submit page"

    def test_set_name_context(self):
        checks = ["some name", "some%20name", "some+name"]
        for check in checks:
            response = self.client.get(
                reverse_lazy("feedback:thank-you") + f"?name={check}"
            )

            assert "name" in response.context, '"name" field does not exist in context'
            assert (
                response.context["name"] == "some name"
            ), "Invalid name is rendered, it should be unescaped"
