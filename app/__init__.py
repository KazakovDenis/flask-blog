"""
The module to be pointed in WSGI configurations
"""
from .blog import *
from . import view


if __name__ == "__main__":
    app.run()
