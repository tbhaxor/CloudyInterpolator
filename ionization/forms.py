from django.core.exceptions import ValidationError
from django.forms import FloatField, Form, IntegerField, TypedChoiceField

from astrodata.constants import (
    ELEMENT_LABEL,
    ION_LABEL,
    METALLICITY_LABEL,
    NH_LABEL,
    REDSHIFT_LABEL,
    SPECIES_TYPES,
    SPECIES_TYPES_LABEL,
    TATVAS,
    TEMPERATURE_LABEL,
    TEMPERATURE_RANGE_BINS_LABEL,
    TEMPERATURE_RANGE_END_LABEL,
    TEMPERATURE_RANGE_START_LABEL,
)


class BaseIonizationForm(Form):
    nH = FloatField(required=True, label=NH_LABEL)
    metallicity = FloatField(required=True, label=METALLICITY_LABEL)
    redshift = FloatField(required=True, label=REDSHIFT_LABEL)


class BaseElementIonForm(Form):
    element = TypedChoiceField(required=True, coerce=int, label=ELEMENT_LABEL, choices=TATVAS, initial=TATVAS[0])
    ion = IntegerField(required=True, label=ION_LABEL, min_value=1, initial=1)
    pass


class InterpolateIonFracForm(BaseIonizationForm, BaseElementIonForm):
    temperature = FloatField(required=True, label=TEMPERATURE_LABEL)

    def clean_ion(self):
        ion = self.cleaned_data["ion"]
        element = self.cleaned_data.get("element")

        if ion > element + 1:
            raise ValidationError(f"Cannot exceed the element+1 count (here, {element+1}).", code="gt_element")

        return ion


class InterpolateIonFracTemperatureForm(BaseIonizationForm, BaseElementIonForm):
    temperature_start = FloatField(required=True, label=TEMPERATURE_RANGE_START_LABEL)
    temperature_stop = FloatField(required=True, label=TEMPERATURE_RANGE_END_LABEL)
    temperature_bins = IntegerField(required=True, label=TEMPERATURE_RANGE_BINS_LABEL)

    def clean_ion(self):
        ion = self.cleaned_data["ion"]
        element = self.cleaned_data.get("element")

        if ion > element + 1:
            raise ValidationError(f"Cannot exceed the element+1 count (here, {element+1}).", code="gt_element")

        return ion

    pass


class InterpolateMDForm(BaseIonizationForm):
    temperature = FloatField(required=True, label=TEMPERATURE_LABEL)
    species_type = TypedChoiceField(required=True, choices=SPECIES_TYPES, initial=SPECIES_TYPES[1], label=SPECIES_TYPES_LABEL)
