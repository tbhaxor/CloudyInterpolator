FROM python:3.10-slim-bullseye

# install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends --no-install-suggests libffi-dev libpq-dev postgresql-client postgresql libhdf5-dev libopenmpi-dev openmpi-bin git gcc g++ && \
    pip install --no-cache-dir --root-user-action=ignore -qU pip poetry && \
    poetry config virtualenvs.create false

# create secure user
RUN useradd -m -d /home/astrodata astrodata

# install pip packages
WORKDIR /tmp
COPY pyproject.toml poetry.lock ./
RUN poetry install --only main && \
    apt-get remove -y git gcc g++ && \
    apt-get autoremove -y && \
    apt-get autoclean -y && \
    rm -rf /var/lib/apt/lists/* && \
    pip uninstall poetry -y && \
    rm -rf pyproject.toml poetry.lock && \
    chown -R astrodata:astrodata "/usr/local/lib/python3.10/site-packages/astro_plasma/data"

# switch to secure user
WORKDIR /home/astrodata
USER astrodata

# copy files into the new workdir
COPY --chown=astrodata:astrodata astrodata/ ./astrodata
COPY --chown=astrodata:astrodata emission/ ./emission
COPY --chown=astrodata:astrodata feedback/ ./feedback
COPY --chown=astrodata:astrodata ionization/ ./ionization
COPY --chown=astrodata:astrodata templates/ ./templates
COPY --chown=astrodata:astrodata accounts/ ./accounts
COPY --chown=astrodata:astrodata deployment/scripts/ ./scripts
COPY --chown=astrodata:astrodata manage.py ./

EXPOSE 5000
ENTRYPOINT [ "bash", "scripts/django-init.bash" ]
