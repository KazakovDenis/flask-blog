from configparser import ConfigParser
from pathlib import Path


APP_ROOT = Path(__file__).parent.absolute()
PROJECT_DIR = APP_ROOT.parent
STATIC_DIR = APP_ROOT / 'public' / 'static'
TEMPLATES_DIR = APP_ROOT / 'public' / 'templates'

parser = ConfigParser()
parser.read(PROJECT_DIR / '.env')


def get_env(name, default=None):
    return parser.get('env', name, fallback=default)


# database
DB_USER = get_env('POSTGRES_USER')
DB_PASS = get_env('POSTGRES_PASS')
DB_ADDRESS = get_env('POSTGRES_ADDRESS')

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
GH_SECRET = get_env('GH_SECRET')
GH_SENDER_ID = get_env('GH_SENDER_ID')
GH_REPO_ID = get_env('GH_REPO_ID')

# sitemap
DOMAIN = get_env('DOMAIN')


# Flask app
class Configuration:
    DEBUG = False
    SQLALCHEMY_ECHO = DEBUG
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = DB_URI
    SECRET_KEY = get_env('FLASK_SECRET')
    UPLOAD_FOLDER = Path(APP_ROOT, 'public/static', 'uploads')
    ALLOWED_EXTENSIONS = ('txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    # flask security
    SECURITY_PASSWORD_SALT = get_env('FLASK_SALT')
    SECURITY_PASSWORD_HASH = 'sha512_crypt'
