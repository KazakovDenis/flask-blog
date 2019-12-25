import multiprocessing
from config.prod import _path, user


bind = "127.0.0.1:8000"
workers = multiprocessing.cpu_count() * 2 + 1
timeout = 600

#pythonpath = _path + '/venv/bin/'
#accesslog = _path + '/log/gunicorn/access.log'
#errorlog = _path + '/log/gunicorn/error.log'
