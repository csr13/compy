FROM nginx:latest

RUN rm -rfvd /etc/nginx/conf.d && mkdir -p /var/www/html/static /var/www/html/media

COPY ./docker/nginx/conf.d /etc/nginx

