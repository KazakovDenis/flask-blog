# cmd to build:
    # docker build -t blog:1.0 .
# cmd to run:
#     docker run -d \
#     --name blog \
#     --restart=on-failure:3 \
#     -p 127.0.0.1:8000:8000 \
#     -v /var/run/postgresql:/run/postgresql \
#     -v $HOME/blog/log:/www/log \
#     -v $HOME/blog/static:/www/blog/static \
#     -v $HOME/blog/templates:/www/blog/templates \
#     blog:1.0

FROM python:3.8-slim
LABEL maintainer="https://github.com/KazakovDenis"
EXPOSE 8000
ARG FLASK_APP="blog/wsgi.py"
ENV FLASK_APP=$FLASK_APP

WORKDIR /www
COPY Makefile manage.py .env configs/guniconf.py requirements/production.txt ./
COPY blog ./blog

RUN apt-get update && apt-get install -y libpq-dev make
RUN python3 -m pip install --upgrade pip && \
    pip3 install --no-cache-dir -r production.txt && \
    rm production.txt && \
    make init_app

CMD gunicorn blog.wsgi:app -c guniconf.py
