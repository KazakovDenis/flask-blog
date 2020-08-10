# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from flask_security import SQLAlchemyUserDatastore, Security
from werkzeug.middleware.proxy_fix import ProxyFix

from app.config import *


app = Flask(__name__)
app.config.from_object(Configuration)
app.wsgi_app = ProxyFix(app.wsgi_app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

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
