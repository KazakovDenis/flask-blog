from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
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
