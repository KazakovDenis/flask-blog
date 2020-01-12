from os import cpu_count, path


bind = '127.0.0.1:8000'
workers = cpu_count() * 2 + 1
timeout = 1000
PATH = path.abspath('..')

pythonpath = f'{PATH}/venv/bin/'
accesslog = f'{PATH}/log/gunicorn/access.log'
errorlog = f'{PATH}/log/gunicorn/error.log'
