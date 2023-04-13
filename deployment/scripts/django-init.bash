#!/bin/bash

set -ex

./manage.py migrate --no-input
./manage.py create-manager --username="$ADMIN_USERNAME" --silent
gunicorn astrodata.wsgi:application -b "0.0.0.0:5000" --error-logfile - --access-logfile -
