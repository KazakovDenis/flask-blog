from flask_migrate import MigrateCommand
from flask_script import Manager

from .wsgi import app


manager = Manager(app)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
