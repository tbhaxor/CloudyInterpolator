from django.forms import FloatField, Form

from astrodata.constants import METALLICITY_LABEL, NH_LABEL, REDSHIFT_LABEL, TEMPERATURE_LABEL


class InterpolateForm(Form):
    nH = FloatField(required=True, label=NH_LABEL)
    temperature = FloatField(required=True, label=TEMPERATURE_LABEL)
    metallicity = FloatField(required=True, label=METALLICITY_LABEL)
    redshift = FloatField(required=True, label=REDSHIFT_LABEL)
