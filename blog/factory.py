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


def set_jinja_globals(app: Flask):
    """Set Jinja2 environment globals"""
    app.jinja_env.globals.update(
        DOMAIN=config.DOMAIN,
        DISQUS_URL=config.DISQUS_URL,
        CONTACT_EMAIL=config.CONTACT_EMAIL,
        CONTACT_GITHUB=config.CONTACT_GITHUB,
        CONTACT_TELEGRAM=config.CONTACT_TELEGRAM,
        YANDEX_METRIKA_ID=config.YANDEX_METRIKA_ID,
        GOOGLE_ANALYTICS_ID=config.GOOGLE_ANALYTICS_ID,
    )


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
