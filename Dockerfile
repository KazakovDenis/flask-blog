# Dockerfile to build Blog App images
# cmd to build:
    # docker build -t blog:1.0 .
# cmd to run:
    # docker run
    # -p 8000:8000
    # -v /var/run/postgresql:/run/postgresql
    # -v /home/logs:/blog/app/logs
    # -v /home/uploads:/blog/app/static/uploads
    # --env DB_USER=$DB_USER
    # --env DB_PASS=$DB_PASS
    # --env DB_ADDRESS=$DB_ADDRESS
    # --env FLASK_SECRET=$FLASK_SECRET
    # --env FLASK_SALT=$FLASK_SALT
    # --name blog
    # blog:1.0
    # /usr/local/bin/gunicorn app:app -b 0.0.0.0:8000 -c /blog/configs/gunicorn_conf.py

FROM debian:10
LABEL maintainer="https://github.com/KazakovDenis"
WORKDIR /blog
COPY . .
COPY configs/supervisor.conf /etc/supervisor/supervisord.conf

RUN mkdir -p log/flask log/gunicorn log/supervisor app/static/uploads
RUN apt-get update && apt-get install -y python3 python3-pip python3-dev libpq-dev
RUN pip3 install --no-cache-dir -r requirements/production.txt
RUN apt-get autoclean && apt-get autoremove

EXPOSE 8000
