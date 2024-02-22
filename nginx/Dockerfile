FROM nginx:1.25-bookworm

WORKDIR /usr/src/epaper_converter

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
