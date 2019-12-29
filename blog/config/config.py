# -*- coding: utf-8 -*-
# https://github.com/KazakovDenis
import os
#from .prod import Configuration


Configuration = None


class TestConfiguration:
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data/test.db'
    SECRET_KEY = 'AG8WMcd0nQ'
    UPLOAD_FOLDER = os.path.abspath('../static/uploads/')
    ALLOWED_EXTENSIONS = ('txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    # flask security
    SECURITY_PASSWORD_SALT = 'kF4jHNrBCpm'
    SECURITY_PASSWORD_HASH = 'sha512_crypt'


CONFIG = TestConfiguration if not Configuration else Configuration
