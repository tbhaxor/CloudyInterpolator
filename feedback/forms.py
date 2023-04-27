from django.forms.models import ModelForm

from .models import FeedbackModel


class FeedbackForm(ModelForm):
    SESSION_KEY = "fdbk_form"

    class Meta:
        model = FeedbackModel
        fields = ["email", "name", "message"]

        session_ignored_fields = ["message"]
