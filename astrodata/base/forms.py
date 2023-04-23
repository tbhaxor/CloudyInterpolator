from django.forms import FloatField, Form, TypedChoiceField
from django.utils.html import format_html

MODE_TYPES = (
    ("CIE", "Collisional Ionisation Equilibrium (CIE)"),
    ("PIE", "Photoionization Equilibrium (PIE)"),
)


class InterpolateForm(Form):
    nH = FloatField(
        required=True,
        label=format_html("Number Density of Hydrogen (cm<sup>-3</sup>)"),
    )

    mode = TypedChoiceField(
        required=True,
        choices=MODE_TYPES,
        initial=MODE_TYPES[0],
        label="Select Mode",
    )

    temperature = FloatField(
        required=True,
        label="Temperature (in Kelvins)",
    )

    metallicity = FloatField(
        required=True,
        label=format_html("Metallicity (Z<sub>&#8857;</sub>)"),
    )

    redshift = FloatField(
        required=True,
        label="Cosmical Redshift",
    )
