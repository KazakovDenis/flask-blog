# cmd to build:
    # docker build -t blog:1.0 .
# cmd to run:
#     docker run -d \
#     --name blog \
#     --restart always \
#     -p 127.0.0.1:8000:8000 \
#     -v /var/run/postgresql:/run/postgresql \
#     -v $PWD/volumes/log:/www/log \
#     -v $PWD/volumes/public:/www/public/volume \
#     blog:1.0

FROM python:3.8-slim
LABEL maintainer="https://github.com/KazakovDenis"
EXPOSE 8000
ARG FLASK_APP="blog/wsgi.py"
ENV FLASK_APP=$FLASK_APP
ENV DOCKER=1

WORKDIR /www
COPY Makefile manage.py .secrets configs/guniconf.py requirements/prod.txt ./
COPY public ./public
COPY blog ./blog

RUN apt-get update && apt-get install -y libpq-dev make
RUN python3 -m pip install --upgrade pip && \
    pip install --no-cache-dir -r prod.txt && \
    rm prod.txt && \
    make init_app

CMD make prod
