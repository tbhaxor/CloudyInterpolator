FROM busybox:1.36

# add secure user and switch
RUN adduser -D -h /home/astro-data astro-data
WORKDIR /home/astro-data
USER astro-data

# copy static files
COPY --chown=astro-data:astro-data ./astrodata/staticfiles/ ./

EXPOSE 80
ENTRYPOINT [ "httpd", "-f" , "-vv" ]
