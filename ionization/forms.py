from django.core.exceptions import ValidationError
from django.forms import ChoiceField, FloatField, Form, IntegerField
from django.forms.widgets import NumberInput, Select

MODE_TYPES = (
    ('CIE', 'Collisional Ionisation Equilibrium (CIE)'),
    ('PIE', 'Photoionization Equilibrium (PIE)')
)

PART_TYPES = (
    ('element', 'Element'),
    ('ion', 'ION')
)


class InterpolateForm(Form):
    nh = FloatField(required=True,
                    label='Number of Hydrogen atoms',
                    widget=NumberInput(attrs={
                        'class': 'form-control',
                    }))

    mode = ChoiceField(choices=MODE_TYPES,
                       required=True,
                       initial=MODE_TYPES[0],
                       label="Select Mode",
                       widget=Select(attrs={
                           'class': 'form-control'
                       }))

    temperature = FloatField(required=True,
                             label='Temperature (in Kelvins)',
                             widget=NumberInput(attrs={
                                 'class': 'form-control'
                             }))

    metallicity = FloatField(required=True,
                             label='Metallicity',
                             widget=NumberInput(attrs={
                                 'class': 'form-control'
                             }))

    redshift = FloatField(required=True,
                          label='Redshift factor',
                          widget=NumberInput(attrs={
                              'class': 'form-control'
                          }))

    element = IntegerField(required=True,
                           min_value=1,
                           max_value=30,
                           label='Atomic Number of Element',
                           widget=NumberInput(attrs={
                               'class': 'form-control'
                           }))

    ion = IntegerField(required=True, label='Ion Count',
                       min_value=1,
                       widget=NumberInput(attrs={
                           'class': 'form-control'
                       }))

    part_type = ChoiceField(required=True,
                            choices=PART_TYPES,
                            initial=PART_TYPES[0],
                            label='Select Part Type',
                            widget=Select(attrs={
                                'class': 'form-control'
                            }))

    def clean_ion(self):
        ion = self.cleaned_data['ion']
        element = self.cleaned_data['element']

        if ion > element:
            raise ValidationError(f'Cannot exceed the element count.', code='GT_ELEMENT')

        return ion
