import multiprocessing
import os
from pathlib import Path
from sys import platform

from blog.config import LOG_DIR


if platform == 'linux':
    pythonpath = '/usr/bin/env python3'

bind = '0.0.0.0:8000'
workers = multiprocessing.cpu_count() * 2 + 1
timeout = 600

LOG_DIR = Path(LOG_DIR, 'gunicorn')
os.makedirs(LOG_DIR, exist_ok=True)

accesslog = str(LOG_DIR / 'access.log')
errorlog = str(LOG_DIR / 'error.log')
