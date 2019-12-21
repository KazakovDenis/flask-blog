from .app import app, db
from . import view
"""
The module to be pointed in WSGI configurations
"""


if __name__ == "__main__":
    app.run()
