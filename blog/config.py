import os
from configparser import ConfigParser
from pathlib import Path


APP_ROOT = Path(__file__).parent.absolute()

PROJECT_DIR = APP_ROOT.parent

parser = ConfigParser()
parser.read(PROJECT_DIR / '.secrets')


def get_secret(name, default=None):
    return parser.get('secrets', name, fallback=default)


PUBLIC_DIR = PROJECT_DIR / 'public'
if os.getenv('DOCKER'):
    PUBLIC_DIR /= 'volume'

TEMPLATES_DIR = PUBLIC_DIR / 'templates'

STATIC_DIR = PUBLIC_DIR / 'static'

UPLOADS_DIR = PUBLIC_DIR / 'uploads'

ALLOWED_EXTENSIONS = ('txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif')

# database
DB_USER = get_secret('POSTGRES_USER')
DB_PASS = get_secret('POSTGRES_PASS')
DB_ADDRESS = get_secret('POSTGRES_ADDRESS')

if DB_USER and DB_PASS and DB_ADDRESS:
    DB_URI = f'postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_ADDRESS}/blog'
else:
    db_name = APP_ROOT / 'blog.sqlite3'
    DB_URI = f'sqlite:///{db_name}'

# logging
LOG_LEVEL = 30
LOG_FORMAT = "[%(asctime)s] @%(name)s  %(levelname)s in %(module)s: %(message)s"
LOG_DIR = PROJECT_DIR / 'log'

# Github webhooks
GH_SECRET = get_secret('GH_SECRET')
GH_SENDER_ID = get_secret('GH_SENDER_ID')
GH_REPO_ID = get_secret('GH_REPO_ID')

# sitemap
DOMAIN = get_secret('DOMAIN')


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
