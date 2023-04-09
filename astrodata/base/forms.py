from django.forms import FloatField, Form, TypedChoiceField
from django.forms.widgets import NumberInput, Select
from django.utils.html import format_html

MODE_TYPES = (
    ('CIE', 'Collisional Ionisation Equilibrium (CIE)'),
    ('PIE', 'Photoionization Equilibrium (PIE)'),
)


class InterpolateForm(Form):
    nH = FloatField(required=True,
                    label=format_html('Number Density of Hydrogen (cm<sup>-3</sup>)'),
                    widget=NumberInput(attrs={'class': 'block w-full rounded-md border-0 py-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-sky-500 sm:text-sm sm:leading-6'}))

    mode = TypedChoiceField(choices=MODE_TYPES,
                            required=True,
                            initial=MODE_TYPES[0],
                            label='Select Mode',
                            widget=Select(attrs={'class': 'block w-full rounded-md border-0 py-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-sky-500 sm:text-sm sm:leading-6'}))

    temperature = FloatField(required=True,
                             label='Temperature (in Kelvins)',
                             widget=NumberInput(attrs={'class': 'block w-full rounded-md border-0 py-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-sky-500 sm:text-sm sm:leading-6'}))

    metallicity = FloatField(required=True,
                             label=format_html('Metallicity (Z<sub>solar</sub>)'),
                             widget=NumberInput(attrs={'class': 'block w-full rounded-md border-0 py-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-sky-500 sm:text-sm sm:leading-6'}))

    redshift = FloatField(required=True,
                          label='Redshift Factor',
                          widget=NumberInput(attrs={'class': 'block w-full rounded-md border-0 py-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-sky-500 sm:text-sm sm:leading-6'}))
