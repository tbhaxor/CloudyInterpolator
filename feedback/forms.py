from django.forms.models import ModelForm
from django.forms.widgets import EmailInput, Textarea, TextInput

from .models import FeedbackModel


class FeedbackForm(ModelForm):
    class Meta:
        model = FeedbackModel
        fields = ['email', 'name', 'message']
        widgets = {
            'name': TextInput(),
            'email': EmailInput(),
            'message': Textarea(),
        }

    pass
