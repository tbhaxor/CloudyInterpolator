from typing import Any, Dict

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


class InterpolateMDForm(BaseIonizationForm, BaseElementIonForm):
    temperature = FloatField(required=True, label=TEMPERATURE_LABEL)
    species_type = TypedChoiceField(required=True, choices=SPECIES_TYPES, initial=SPECIES_TYPES[1], label=SPECIES_TYPES_LABEL)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.fields["element"].required = False
        self.fields["element"].choices = [(0, "None")] + TATVAS
        self.fields["element"].initial = None

        self.fields["ion"].required = False
        self.fields["ion"].initial = None

    def clean(self) -> Dict[str, Any]:
        data: Dict[str, Any] = self.cleaned_data

        try:
            element = int(data.get("element", 0))
        except ValueError:
            element = 0

        try:
            ion = data.get("ion", 1)
        except ValueError:
            ion = 1

        data["element"] = None if element == 0 else element
        data["ion"] = None if data["element"] is None else ion

        if data["element"] is not None and ion > element + 1:
            self.add_error("ion", ValidationError(f"Cannot exceed the element+1 count (here, {element+1}).", code="gt_element"))

        return data
