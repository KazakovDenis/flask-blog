# -*- coding: utf-8 -*-
# https://github.com/KazakovDenis
import os


PATH = os.path.abspath(os.path.curdir)

# database
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')

# Github webhooks
GH_SECRET = os.environ.get('GH_SECRET')
GH_SENDER_ID = os.environ.get('GH_SENDER_ID')
GH_REPO_ID = os.environ.get('GH_REPO_ID')

# logging
LOG_LEVEL = 20
LOG_FORMAT = "[%(asctime)s] @%(name)s  %(levelname)s in %(module)s: %(message)s"


class Configuration:
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{DB_USER}:{DB_PASS}@localhost/blog'
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///data/test.db'
    SECRET_KEY = os.environ.get('FLASK_SECRET')
    UPLOAD_FOLDER = os.path.abspath('../static/uploads/')
    ALLOWED_EXTENSIONS = ('txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    # flask security
    SECURITY_PASSWORD_SALT = os.environ.get('FLASK_SALT')
    SECURITY_PASSWORD_HASH = 'sha512_crypt'
