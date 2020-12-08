from flask import Flask
from flask_migrate import Migrate
from flask_security import Security, SQLAlchemyUserDatastore
from flask_sqlalchemy import SQLAlchemy
from werkzeug.middleware.proxy_fix import ProxyFix

from .config import Configuration
from .services.functions import configure_logger


db = SQLAlchemy()
migrate = Migrate()
security = Security()


def create_app(config: type = Configuration, datastore: SQLAlchemyUserDatastore = None) -> Flask:
    """Create a configured app"""
    app = Flask(__name__)
    app.config.from_object(config)
    app.wsgi_app = ProxyFix(app.wsgi_app)

    db.init_app(app)
    migrate.init_app(app, db)
    security.init_app(app, datastore)

    configure_logger(app)
    return app
