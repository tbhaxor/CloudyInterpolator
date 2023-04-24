#!/bin/bash

set -ex

# Fix for the pre-initialized Ionization and EmissionSpectrum
if [[ ! -L "/usr/local/lib/python3.10/site-packages/astro_plasma/data/emission" ]]; then
    ln -s "$EMISSION_DATASET_DIR" /usr/local/lib/python3.10/site-packages/astro_plasma/data/emission
fi

if [[ ! -L "/usr/local/lib/python3.10/site-packages/astro_plasma/data/ionization" ]]; then
    ln -s "$IONIZATION_DATASET_DIR" /usr/local/lib/python3.10/site-packages/astro_plasma/data/ionization
fi

./manage.py migrate --no-input
./manage.py createmanager --username="${ADMIN_USERNAME:-astrodata}" --silent
gunicorn astrodata.wsgi:application -b "0.0.0.0:5000" --error-logfile - --access-logfile -
