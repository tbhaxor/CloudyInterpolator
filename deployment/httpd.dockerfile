FROM busybox:1.36

RUN adduser -D -h /home/astro-data astro-data
WORKDIR /home/astro-data
USER astro-data

COPY --chown=astro-data:astro-data ./astrodata/staticfiles/ ./

ENTRYPOINT [ "httpd", "-f" , "-vv" ]
