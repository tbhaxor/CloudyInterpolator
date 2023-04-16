from django.core.exceptions import ValidationError
from django.forms import FloatField, Form, IntegerField, TypedChoiceField
from django.utils.html import format_html
from PyAstronomy.pyasl.asl.atomicNo import AtomicNo

from astrodata.base.forms import InterpolateForm

MODE_TYPES = (
    ('CIE', 'Collisional Ionisation Equilibrium (CIE)'),
    ('PIE', 'Photoionization Equilibrium (PIE)'),
)

SPECIES_TYPES = (
    ('all', 'All'),
    ('electron', 'Electron'),
    ('ion', 'ION'),
)

PARMANU = AtomicNo()

TATVAS = []
for atn in range(1, 31):
    TATVAS.append((atn, f'{PARMANU.getElementName(atn)} ({PARMANU.getElSymbol(atn)})'))


class InterpolateIonFractionForm(InterpolateForm):
    element = TypedChoiceField(
        required=True,
        coerce=int,
        label='Select Element',
        choices=TATVAS,
        initial=TATVAS[0],
    )

    ion = IntegerField(
        required=True,
        label='Ion Count',
        min_value=1,
        initial=1
    )

    def clean_ion(self):
        ion = self.cleaned_data['ion']
        element = self.cleaned_data.get('element')

        if ion > element + 1:
            raise ValidationError(f'Cannot exceed the element+1 count (here, {element+1}).', code='gt_element')

        return ion


class InterpolateIonFracTemperatureForm(Form):
    element = TypedChoiceField(
        required=True,
        coerce=int,
        label='Select Element',
        choices=TATVAS,
        initial=TATVAS[0],
    )

    ion = IntegerField(
        required=True,
        label='Ion Count',
        min_value=1,
        initial=1
    )

    nH = FloatField(
        required=True,
        label=format_html('Number Density of Hydrogen (cm<sup>-3</sup>)'),
    )

    temperature_start = FloatField(
        required=True,
        label=format_html('log<sub>10</sub>(Temperature Start Range) (in Kelvins)'),
    )

    temperature_stop = FloatField(
        required=True,
        label=format_html('log<sub>10</sub>(Temperature Start Range) (in Kelvins)'),
    )

    temperature_step = FloatField(
        required=True,
        label='Temperature Range Step Sizes',
    )

    metallicity = FloatField(
        required=True,
        label=format_html('Metallicity (Z<sub>&#8857;</sub>)'),
    )

    redshift = FloatField(
        required=True,
        label='Cosmical Redshift',
    )

    def clean_ion(self):
        ion = self.cleaned_data['ion']
        element = self.cleaned_data.get('element')

        if ion > element + 1:
            raise ValidationError(f'Cannot exceed the element+1 count (here, {element+1}).', code='gt_element')

        return ion
    pass


class InterpolateMDForm(InterpolateForm):
    species_type = TypedChoiceField(
        required=True,
        choices=SPECIES_TYPES,
        initial=SPECIES_TYPES[1],
        label='Select Species Type',
    )
