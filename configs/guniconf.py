import multiprocessing
from pathlib import Path
from sys import platform

from blog.config import LOG_DIR


bind = '0.0.0.0:8000'
workers = multiprocessing.cpu_count() * 2 + 1
timeout = 600

if platform == 'linux':
    pythonpath = '/usr/bin/env python3'

LOG_DIR = Path(LOG_DIR, 'gunicorn')
accesslog = str(LOG_DIR / 'access.log')
errorlog = str(LOG_DIR / 'error.log')
