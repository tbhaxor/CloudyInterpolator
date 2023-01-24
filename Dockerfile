FROM python:3.10-slim-bullseye

RUN apt-get update && \
    apt-get install -y --no-install-recommends --no-install-suggests libhdf5-dev libhdf5-serial-dev && \
    apt-get clean && \
    apt-get autoclean && \
    apt-get autoremove && \
    pip install -qU pip

WORKDIR /home/astro-data
RUN useradd -d /home/astro-data astro-data && \
    chown astro-data:astro-data -R /home/astro-data
USER astro-data
ENV PATH=/home/astro-data/.local/bin:${PATH}

COPY --chown=astro-data:astro-data requirements.txt ./
RUN pip install -qr requirements.txt && rm requirements.txt 

COPY --chown=astro-data:astro-data astrodata/ ./astrodata
COPY --chown=astro-data:astro-data emission/ ./emission
COPY --chown=astro-data:astro-data ionization/ ./ionization
COPY --chown=astro-data:astro-data templates/ ./templates
COPY --chown=astro-data:astro-data manage.py ./

RUN python manage.py migrate

EXPOSE 5000

ENTRYPOINT ["gunicorn", "astrodata.wsgi:application", "-b", "0.0.0.0:5000", \
    "--error-logfile","-", "--access-logfile", "-", "--capture-output"]