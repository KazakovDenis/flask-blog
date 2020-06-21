from multiprocessing import Process
from time import sleep

from app.view import *


HOST, PORT = '127.0.0.1', 7999
BASE_URL = f'http://{HOST}:{PORT}'
server = Process(target=lambda: app.run(host=HOST, port=PORT))


def setup_module():
    server.start()
    sleep(5)             # while the server is not running


def teardown_module():
    server.terminate()
    server.join()
