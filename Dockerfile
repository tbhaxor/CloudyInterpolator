FROM python:3.10-alpine

# install build dependencies
RUN apk add --no-cache openmpi openmpi-dev hdf5-dev hdf5 git musl-dev gcc g++ build-base wget freetype-dev libpng-dev openblas-dev gfortran && \
    pip install --root-user-action=ignore -qU pip

# install pip packages
WORKDIR /tmp
COPY requirements.txt ./
RUN pip install -r requirements.txt && \ 
    apk del git g++ gcc musl-dev gfortran build-base wget freetype-dev libpng-dev openblas-dev && \
    rm -rf /tmp/requirements.txt
RUN ln -s /usr/include/locale.h /usr/include/xlocale.h

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