import os

from .parser import *


PUBLIC_DIR = PROJECT_DIR / 'public'
if os.getenv('DOCKER'):
    PUBLIC_DIR /= 'volume'

TEMPLATES_DIR = PUBLIC_DIR / 'templates'
STATIC_DIR = PUBLIC_DIR / 'static'
UPLOADS_DIR = PUBLIC_DIR / 'uploads'

INITIAL_FIXTURES = APP_ROOT / 'fixtures' / 'initial.json'
ALLOWED_EXTENSIONS = ('txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif')

# Database
DB_USER = get_secret('POSTGRES_USER')
DB_PASS = get_secret('POSTGRES_PASS')
DB_ADDRESS = get_secret('POSTGRES_ADDRESS', '')     # defaults to unix socket

if DB_USER and DB_PASS:
    DB_URI = f'postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_ADDRESS}/blog'
else:
    db_name = PROJECT_DIR / 'blog.sqlite3'
    DB_URI = f'sqlite:///{db_name}'

# Common
DOMAIN = get_secret('DOMAIN')
MAINTAINER = get_secret('MAINTAINER')
LOG_LEVEL = 30
LOG_FORMAT = "[%(asctime)s] @%(name)s  %(levelname)s in %(module)s: %(message)s"
LOG_DIR = PROJECT_DIR / 'log'

# Contacts
GITHUB_USER = get_secret('GITHUB_USER')
CONTACT_EMAIL = get_secret('CONTACT_EMAIL')
CONTACT_TELEGRAM = get_secret('CONTACT_TELEGRAM')

# Integrations
DISQUS_URL = get_secret('DISQUS_URL')
YANDEX_METRIKA_ID = get_secret('YANDEX_METRIKA_ID')
GOOGLE_ANALYTICS_ID = get_secret('GOOGLE_ANALYTICS_ID')


# Flask app
class Configuration:
    DEBUG = False
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    SECRET_KEY = get_secret('FLASK_SECRET')
    SECURITY_PASSWORD_SALT = get_secret('FLASK_SALT')
    SECURITY_PASSWORD_HASH = 'sha512_crypt'
    SQLALCHEMY_ECHO = DEBUG
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = DB_URI
