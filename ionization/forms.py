from enum import Enum

from django import forms
from django.core.exceptions import ValidationError

MODE_TYPES = (
    ('CIE', 'Collisional Ionisation Equilibrium (CIE)'),
    ('PIE', 'Photoionization Equilibrium (PIE)')
)


class InterpolateForm(forms.Form):
    nh = forms.FloatField(required=True, label='nH')
    mode = forms.ChoiceField(choices=MODE_TYPES, required=True, initial=MODE_TYPES[0])
    temperature = forms.FloatField(required=True, help_text='Provide the template in Kelvins.')
    metallicity = forms.FloatField(required=True)
    redshift = forms.FloatField(required=True)
    element = forms.IntegerField(required=True, min_value=1, max_value=30,
                                 help_text='Provide the atomic number of the element.')
    ion = forms.IntegerField(required=True, min_value=1,
                             help_text='Ion count could be less than equal to the element number.')

    def clean_ion(self):
        ion = self.cleaned_data['ion']
        element = self.cleaned_data['element']

        if ion > element:
            raise ValidationError(f'Cannot exceed the element count.')

        return ion
