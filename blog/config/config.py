# -*- coding: utf-8 -*-
# https://github.com/KazakovDenis
import os


PATH = os.path.abspath('..')

# database
USER = os.environ.get('USER')
PASSWORD = os.environ.get('DB_PASS')

# Github webhooks
GH_SECRET = os.environ.get('GH_SECRET')
GH_SENDER_ID = os.environ.get('GH_SENDER_ID')
GH_REPO_ID = os.environ.get('GH_REPO_ID')


class Configuration:
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{USER}:{PASSWORD}@localhost/blog'
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///data/test.db'
    SECRET_KEY = os.environ.get('FLASK_SECRET')
    UPLOAD_FOLDER = os.path.abspath('../static/uploads/')
    ALLOWED_EXTENSIONS = ('txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    # flask security
    SECURITY_PASSWORD_SALT = os.environ.get('FLASK_SALT')
    SECURITY_PASSWORD_HASH = 'sha512_crypt'
