# -*- coding: utf-8 -*-
# https://github.com/KazakovDenis
from .app import app, db
from . import view


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8000)   # принимает булев аргумент debug, host=ip, port=port
