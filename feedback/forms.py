from django.forms.models import ModelForm

from .models import FeedbackModel


class FeedbackForm(ModelForm):
    class Meta:
        model = FeedbackModel
        fields = ['email', 'name', 'message']
