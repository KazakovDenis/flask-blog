# -*- coding: utf-8 -*-
# https://github.com/KazakovDenis
import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from flask_security import SQLAlchemyUserDatastore, Security
from werkzeug.middleware.proxy_fix import ProxyFix

from config.config import *


app = Flask(__name__)
app.config.from_object(Configuration)
app.wsgi_app = ProxyFix(app.wsgi_app)

# logger
log = app.logger
log.setLevel(LOG_LEVEL)
fh = logging.FileHandler(f'{PATH}/log/flask/flask.log', encoding='utf-8')
fh.setFormatter(logging.Formatter(LOG_FORMAT))
log.addHandler(fh)
log.info('Flask app initialized')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


from posts.blueprint import posts
app.register_blueprint(posts, url_prefix='/app/')

from api.blueprint import api
app.register_blueprint(api, url_prefix='/api/')

from models import User, Role
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

from sitemap import sm_view
app.add_url_rule('/sitemap.xml', endpoint='sitemap', view_func=sm_view)
