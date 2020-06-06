# Dockerfile to build Blog App images
# cmd to build: docker build -t blog-image:v1 .
# cmd to run:   docker run -p 80:8000 -it --rm blog-image:v1

FROM debian:9
WORKDIR /blog
COPY . .
COPY configs/supervisor.conf /etc/supervisor/supervisord.conf

RUN apt update && apt upgrade -y && apt install -y python3 python3-pip python3-dev
RUN pip3 install -r requirements/production.txt
RUN supervisord -c /etc/supervisor/supervisor.conf

EXPOSE 8000
CMD ["/usr/local/bin/supervisord", "-c", "/etc/supervisor/supervisor.conf"]
