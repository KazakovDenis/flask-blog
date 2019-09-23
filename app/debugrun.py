# -*- coding: utf-8 -*-
# https://github.com/KazakovDenis
from app import app
from app import db
import view


if __name__ == '__main__':
    app.run()   # принимает булев аргумент debug, host=ip, port=port
