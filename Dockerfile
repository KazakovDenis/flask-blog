# cmd to build:
#     docker build -t kazakovdu/blog:$TAG .
# cmd to run:
#     docker run -d \
#     --name blog \
#     --restart always \
#     -p 127.0.0.1:8000:8000 \
#     -v /var/run/postgresql:/run/postgresql \
#     -v $PWD/volumes/log:/www/log \
#     -v $PWD/volumes/public:/www/public/volume \
#     -v $PWD/.secrets:/www/.secrets \
#     blog:$TAG

FROM python:3.8-slim as base
LABEL maintainer="https://github.com/KazakovDenis"
WORKDIR /www
COPY requirements/prod.txt requirements.txt
RUN apt update && apt install -y libpq-dev make
RUN python3 -m pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    rm requirements.txt

FROM base as source
EXPOSE 8000
ARG FLASK_APP="blog/wsgi.py"
ENV FLASK_APP=$FLASK_APP
ENV DOCKER=1
COPY Makefile manage.py configs/guniconf.py ./
COPY public ./public
COPY blog ./blog
COPY deploy/entrypoint.sh entrypoint.sh
RUN chmod +x entrypoint.sh

ENTRYPOINT ./entrypoint.sh
CMD make prod
