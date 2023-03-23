from django.core.exceptions import ValidationError
from django.forms import IntegerField, TypedChoiceField
from django.forms.widgets import NumberInput, Select
from PyAstronomy.pyasl.asl.atomicNo import AtomicNo

from astrodata.base.forms import InterpolateForm

MODE_TYPES = (
    ('CIE', 'Collisional Ionisation Equilibrium (CIE)'),
    ('PIE', 'Photoionization Equilibrium (PIE)')
)

SPECIES_TYPES = (
    ('all', 'All'),
    ('electron', 'Electron'),
    ('ion', 'ION')
)

parmanu = AtomicNo()

TATVAS = []
for atn in range(1, 31):
    TATVAS.append((atn, f"{parmanu.getElementName(atn)} ({parmanu.getElSymbol(atn)})"))
TATVAS = tuple(TATVAS)


class InterpolateForm(InterpolateForm):
    element = TypedChoiceField(coerce=int, required=True,
                               label='Select Element',
                               choices=TATVAS,
                               initial=TATVAS[0],
                               widget=Select(attrs={'class': 'form-select', }))

    ion = IntegerField(required=True, label='Ion Count',
                       min_value=1,
                       widget=NumberInput(attrs={'class': 'form-control'}))

    species_type = TypedChoiceField(required=True,
                                    choices=SPECIES_TYPES,
                                    initial=SPECIES_TYPES[1],
                                    label='Select Species Type',
                                    widget=Select(attrs={'class': 'form-select'}))

    def clean_ion(self):
        ion = self.cleaned_data['ion']
        element = self.cleaned_data.get('element')

        if element is None:
            return

        if ion > element+1:
            raise ValidationError(f'Cannot exceed the element+1 count (here, {element+1}).', code='gt_element')

        return ion
