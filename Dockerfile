# Dockerfile to build Blog App images
# cmd to build:
    # docker build -t blog-image:v1 .
# cmd to run:
    # docker run
    # -p 8000:8000
    # -v /var/run/postgresql:/run/postgresql
    # --env DB_USER=$DB_USER
    # --env DB_PASS=$DB_PASS
    # --env DB_ADDRESS=$DB_ADDRESS
    # --env FLASK_SECRET=$FLASK_SECRET
    # --env FLASK_SALT=$FLASK_SALT
    # --name blog
    # blog-image:v1 python3 -m app.manage runserver -h 0.0.0.0 -p 8000

FROM debian:10
LABEL maintainer="https://github.com/KazakovDenis"
WORKDIR /blog
COPY . .
COPY configs/supervisor.conf /etc/supervisor/supervisord.conf

RUN apt-get update && apt-get install -y python3 python3-pip python3-dev libpq-dev
RUN pip3 install --no-cache-dir -r requirements/production.txt
RUN apt-get autoclean && apt-get autoremove

EXPOSE 8000 5000
