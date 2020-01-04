import multiprocessing
from config.prod import PATH


bind = "127.0.0.1:8000"
workers = multiprocessing.cpu_count() * 2 + 1
timeout = 600

#pythonpath = PATH + '/venv/bin/'
#accesslog = PATH + '/log/gunicorn/access.log'
#errorlog = PATH + '/log/gunicorn/error.log'
