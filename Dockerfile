FROM python:3.10-alpine

# install build dependencies
RUN apk add --no-cache openmpi openmpi-dev hdf5-dev hdf5 git musl-dev gcc g++ && \
    rm -rf /var/cache/apk/* && \
    pip install --root-user-action=ignore -qU pip

# install pip packages
WORKDIR /tmp
COPY requirements.txt ./
RUN pip install -r requirements.txt && \ 
    apk del git g++ gcc musl-dev && \
    apk cache --purge && \
    rm -rf /tmp/requirements.txt

# create secure user
RUN adduser -h /home/astrodata -D astrodata
WORKDIR /home/astrodata
USER astrodata

# copy files into the new workdir
COPY --chown=astrodata:astrodata astrodata/ ./astrodata
COPY --chown=astrodata:astrodata emission/ ./emission
COPY --chown=astrodata:astrodata ionization/ ./ionization
COPY --chown=astrodata:astrodata templates/ ./templates

EXPOSE 5000

ENTRYPOINT ["gunicorn", "astrodata.wsgi:application", \
    \\        "-b", "0.0.0.0:5000", \
    \\        "--error-logfile","-", "--access-logfile", "-", \
    \\        "--capture-output"]