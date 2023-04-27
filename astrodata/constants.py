from django.utils.html import format_html

# Enumeration / Choices
MODE_TYPES = [
    ["CIE", "Collisional Ionisation Equilibrium"],
    ["PIE", "Photoionization Equilibrium"],
]
MODE_TYPES = sorted(MODE_TYPES, key=lambda x: x[0])
MODE_TYPES = tuple(map(tuple, MODE_TYPES))

# Labels
NH_LABEL = format_html("Number Density of Hydrogen (cm<sup>-3</sup>)")
TEMPERATURE_LABEL = format_html("Temperature (in Kelvins)")
METALLICITY_LABEL = format_html("Metallicity (Z<sub>&#8857;</sub>)")
REDSHIFT_LABEL = format_html("Cosmical Redshift")
