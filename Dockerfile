# Dockerfile to build Blog App images
# cmd to build:
    # docker build -t blog:1.0 .
# cmd to run:
#     docker run -d \
#     --restart=on-failure:3 \
#     -p 127.0.0.1:8000:8000 \
#     -v /var/run/postgresql:/run/postgresql \
#     -v /home/log:/blog/log \
#     -v /home/uploads:/blog/app/static/uploads \
#     --env DB_USER=$DB_USER \
#     --env DB_PASS=$DB_PASS \
#     --env DB_ADDRESS=$DB_ADDRESS \
#     --env FLASK_SECRET=$FLASK_SECRET \
#     --env FLASK_SALT=$FLASK_SALT \
#     --name blog \
#     blog:1.0 \
#     gunicorn app:app -c /blog/configs/gunicorn_conf.py

# creating base image with env
FROM debian:10 as base
WORKDIR /home
RUN apt-get update && apt-get install -y python3 python3-pip python3-dev libpq-dev
COPY requirements/production.txt ./requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt
RUN apt-get clean

# creating app image from base
FROM base
LABEL maintainer="https://github.com/KazakovDenis"
WORKDIR /blog
COPY . .
RUN mkdir -p log/flask log/gunicorn app/static/uploads
EXPOSE 8000
