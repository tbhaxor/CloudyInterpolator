FROM python:3.10-slim-bullseye

# install build dependencies
RUN apt update && \
    apt install -y --no-install-recommends libhdf5-dev libopenmpi-dev openmpi-bin git gcc g++ && \
    pip install --root-user-action=ignore -qU pip

# install pip packages
WORKDIR /tmp
COPY requirements.txt ./
RUN pip install -r requirements.txt && \ 
    apt remove -y git gcc g++ && \
    apt autoremove -y && \
    apt autoclean -y && \
    rm -rf /tmp/requirements.txt

# create secure user
RUN useradd -m -d /home/astrodata astrodata 
WORKDIR /home/astrodata
USER astrodata

# copy files into the new workdir
COPY --chown=astrodata:astrodata astrodata/ ./astrodata
COPY --chown=astrodata:astrodata emission/ ./emission
COPY --chown=astrodata:astrodata ionization/ ./ionization
COPY --chown=astrodata:astrodata templates/ ./templates

EXPOSE 5000

ENTRYPOINT ["gunicorn", "astrodata.wsgi:application", \
    "-b", "0.0.0.0:5000", \
    "--error-logfile","-", "--access-logfile", "-", \
    "--capture-output"]