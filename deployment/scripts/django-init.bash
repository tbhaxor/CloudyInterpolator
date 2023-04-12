#!/bin/bash

set -ex

./manage.py migrate --no-input
gunicorn astrodata.wsgi:application -b "0.0.0.0:5000" --error-logfile - --access-logfile -
