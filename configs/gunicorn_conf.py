import multiprocessing


bind = "127.0.0.1:8000"
workers = multiprocessing.cpu_count() * 2 + 1
timeout = 600

pythonpath = '/usr/bin/python3'
accesslog = '/blog/log/gunicorn/access.log'
errorlog = '/blog/log/gunicorn/error.log'
