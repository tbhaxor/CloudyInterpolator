from django.forms.models import ModelForm
from django.forms.widgets import EmailInput, Textarea, TextInput

from .models import FeedbackModel


class FeedbackForm(ModelForm):
    class Meta:
        model = FeedbackModel
        fields = ['email', 'name', 'message']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'email': EmailInput(attrs={'class': 'form-control'}),
            'message': Textarea(attrs={'class': 'form-control'}),
        }

    pass
