from configparser import ConfigParser
from pathlib import Path


__all__ = 'APP_ROOT', 'PROJECT_DIR', 'get_secret', 'parser'

APP_ROOT = Path(__file__).parent.parent.absolute()
PROJECT_DIR = APP_ROOT.parent
SECRETS_SRC = PROJECT_DIR / '.secrets'

if not SECRETS_SRC.exists() or SECRETS_SRC.is_dir():
    raise FileNotFoundError('.secrets does not exist or directory is mounted')

parser = ConfigParser()
parser.read(SECRETS_SRC)


def get_secret(name, default=None):
    return parser.get('secrets', name, fallback=default)
