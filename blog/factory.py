from flask import Flask
from flask_migrate import Migrate
from flask_security import Security, SQLAlchemyUserDatastore
from flask_sqlalchemy import SQLAlchemy
from werkzeug.middleware.proxy_fix import ProxyFix

from blog import config
from .services.functions import configure_logger


db = SQLAlchemy()
migrate = Migrate()
security = Security()


def set_jinja_globals(app):
    """Set Jinja2 environment globals"""
    app.jinja_env.globals['DOMAIN'] = config.DOMAIN
    app.jinja_env.globals['DISQUS_URL'] = config.DISQUS_URL
    app.jinja_env.globals['CONTACT_EMAIL'] = config.CONTACT_EMAIL
    app.jinja_env.globals['CONTACT_GITHUB'] = config.CONTACT_GITHUB
    app.jinja_env.globals['CONTACT_TELEGRAM'] = config.CONTACT_TELEGRAM


def create_app(
        conf: type = config.Configuration,
        datastore: SQLAlchemyUserDatastore = None,
        migrations_dir: str = '') -> Flask:
    """Create a configured app"""
    app = Flask(
        __package__,
        template_folder=config.TEMPLATES_DIR,
        static_folder=config.STATIC_DIR,
    )
    app.config.from_object(conf)
    app.wsgi_app = ProxyFix(app.wsgi_app)

    db.init_app(app)
    migrate.init_app(app, db, directory=migrations_dir)
    security.init_app(app, datastore)

    set_jinja_globals(app)
    configure_logger(app)
    return app
