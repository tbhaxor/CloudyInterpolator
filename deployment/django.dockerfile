FROM python:3.10-slim-bullseye

# install build dependencies
RUN apt update && \
    apt install -y --no-install-recommends libhdf5-dev libopenmpi-dev openmpi-bin git gcc g++ && \
    pip install --root-user-action=ignore -qU pip poetry && \
    poetry config virtualenvs.create false

# install pip packages
WORKDIR /home/astrodata
COPY --chown=astrodata:astrodata pyproject.toml poetry.lock ./
RUN poetry install && \
    apt remove -y git gcc g++ && \
    apt autoremove -y && \
    apt autoclean -y && \
    pip uninstall poetry -y

# create secure user
RUN useradd -m -d /home/astrodata astrodata && \
    chown astrodata:astrodata /home/astrodata -R && \
    mkdir -p /opt/data/database && \
    chown astrodata:astrodata /opt/data/database -R
USER astrodata

# copy files into the new workdir
COPY --chown=astrodata:astrodata astrodata/ ./astrodata
COPY --chown=astrodata:astrodata emission/ ./emission
COPY --chown=astrodata:astrodata feedback/ ./feedback
COPY --chown=astrodata:astrodata ionization/ ./ionization
COPY --chown=astrodata:astrodata templates/ ./templates
COPY --chown=astrodata:astrodata deployment/management ./deployment/management
COPY --chown=astrodata:astrodata deployment/*.py ./deployment/
COPY --chown=astrodata:astrodata deployment/scripts/ ./scripts
COPY --chown=astrodata:astrodata manage.py ./

EXPOSE 5000

ENTRYPOINT [ "bash", "scripts/django-init.bash" ]
