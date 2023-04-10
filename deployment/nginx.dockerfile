FROM nginx:alpine

COPY deployment/nginx.conf /etc/nginx/conf.d/default.conf
COPY astrodata/staticfiles/ /usr/share/nginx/static/
