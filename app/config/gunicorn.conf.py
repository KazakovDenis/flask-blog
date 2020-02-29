from os import cpu_count
from config.config import PATH


bind = '127.0.0.1:8000'
workers = cpu_count() * 2 + 1
timeout = 1000

pythonpath = f'{PATH}/venv/bin/'
accesslog = f'{PATH}/log/gunicorn/access.log'
errorlog = f'{PATH}/log/gunicorn/error.log'
