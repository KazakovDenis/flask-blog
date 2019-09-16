# -*- coding: utf-8 -*-
# https://github.com/KazakovDenis
from app import app
from app import db
from posts.blueprint import posts
import view


# регистрируем блюпринт под адресом /блог
app.register_blueprint(posts, url_prefix='/blog')

if __name__ == '__main__':
    app.run()   # принимает булев аргумент debug
