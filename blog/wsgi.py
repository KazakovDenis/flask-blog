"""
The module to be pointed in WSGI configurations
"""
from app import app, db
import view


if __name__ == "__main__":
    app.run()
