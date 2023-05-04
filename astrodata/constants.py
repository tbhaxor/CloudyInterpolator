from django.utils.html import format_html
from PyAstronomy.pyasl.asl.atomicNo import AtomicNo

# Enumeration / Choices
MODE_TYPES = [
    ["CIE", "Collisional Ionisation Equilibrium"],
    ["PIE", "Photoionization Equilibrium"],
]
MODE_TYPES = sorted(MODE_TYPES, key=lambda x: x[0])
MODE_TYPES = tuple(map(tuple, MODE_TYPES))

SPECIES_TYPES = [
    ["all", "All"],
    ["electron", "Electron"],
    ["ion", "ION"],
]
SPECIES_TYPES = sorted(SPECIES_TYPES, key=lambda x: x[0])
SPECIES_TYPES = tuple(map(tuple, SPECIES_TYPES))
PARMANU = AtomicNo()
TATVAS = [(atn, f"{PARMANU.getElementName(atn)} ({PARMANU.getElSymbol(atn)})") for atn in range(1, 31)]


# Labels
NH_LABEL = format_html("Number Density of Hydrogen (cm<sup>-3</sup>)")
TEMPERATURE_LABEL = format_html("Temperature (in Kelvins)")
TEMPERATURE_RANGE_START_LABEL = format_html("Temperature Range Start (in Kelvins)")
TEMPERATURE_RANGE_END_LABEL = format_html("Temperature Range End (in Kelvins)")
TEMPERATURE_RANGE_BINS_LABEL = format_html("Temperature Bins")
SPECIES_TYPES_LABEL = format_html("Select Species Type")
METALLICITY_LABEL = format_html("Metallicity (Z<sub>&#8857;</sub>)")
REDSHIFT_LABEL = format_html("Cosmical Redshift")
ELEMENT_LABEL = format_html("Select Element")
ION_LABEL = format_html("Ion Count")

# Session keys
SESSION_FORM_DATA = "form_data"
SESSION_INTERPOLATE_MD_MISC_DATA = "interpolate_md_misc_data"
