# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from flask_security import SQLAlchemyUserDatastore, Security
from werkzeug.middleware.proxy_fix import ProxyFix

from .config import *


db = SQLAlchemy()
migrate = Migrate()


def create_app(config=Configuration):
    """Create a configured app"""
    application = Flask(__name__)
    application.config.from_object(config)
    application.wsgi_app = ProxyFix(application.wsgi_app)
    db.init_app(application)
    migrate.init_app(application, db)
    return application


app = create_app()

from app.services import log
from app.posts.blueprint import posts
app.register_blueprint(posts, url_prefix='/blog/')

from app.api.blueprint import api
app.register_blueprint(api, url_prefix='/api/')

from app.models import User, Role
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

from app.admin import admin
from app.sitemap import sm_view
app.add_url_rule('/sitemap.xml', endpoint='sitemap', view_func=sm_view)
