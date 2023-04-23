FROM nginx:stable-alpine-slim

# copy static files
WORKDIR /usr/share/astrodata
COPY --chown=astro-data:astro-data ./astrodata/staticfiles/ ./

EXPOSE 80
