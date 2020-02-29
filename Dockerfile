############################################################
# Dockerfile to build Blog App container images
# cmd: docker build -t blog-image .
############################################################
FROM debian:latest
WORKDIR /blog
COPY . .
COPY other/nginx.conf /etc/nginx/conf.d
COPY other/supervisor.conf /etc/supervisor/supervisord.conf

RUN apt update && apt upgrade -y && apt install -y nginx-light python3 python3-pip python3-dev
RUN pip3 install -r requirements.txt
RUN rm /blog/other/*.conf

#RUN usr/sbin/nginx -g "daemon off;"
RUN service nginx start
RUN supervisord -c /etc/supervisor/supervisor.conf
EXPOSE 80
#CMD ["/usr/local/bin/supervisord", "-c", "/etc/supervisor/supervisor.conf"]
