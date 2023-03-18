FROM python:3.10

RUN apt update && \
    apt install -y openmpi-bin openmpi-common libopenmpi-dev mpich libhdf5-dev libhdf5-serial-dev && \
    apt clean && \
    apt autoclean && \
    apt autoremove && \
    pip install --root-user-action=ignore -qU pip poetry && \
    poetry config virtualenvs.create false
WORKDIR /app
COPY poetry.lock pyproject.toml ./
RUN poetry install

COPY astrodata/ ./astrodata
COPY emission/ ./emission
COPY ionization/ ./ionization
COPY templates/ ./templates

EXPOSE 5000

ENTRYPOINT ["gunicorn", "astrodata.wsgi:application", \
    "-b", "0.0.0.0:5000", \
    "--error-logfile","-", "--access-logfile", "-", \
    "--capture-output"]