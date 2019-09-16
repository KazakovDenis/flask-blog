# -*- coding: utf-8 -*-
# https://github.com/KazakovDenis


class Configuration(object):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:@localhost/test1'
    SECRET_KEY = 'AG8WMcd0nQ'

    ### flask security
    SECURITY_PASSWORD_SALT = 'kF4jHNrBCpm'
    SECURITY_PASSWORD_HASH = 'sha512_crypt'
