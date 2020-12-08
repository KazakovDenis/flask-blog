from flask_migrate import MigrateCommand
from flask_script import Manager

from app.blog import app
from app import view


manager = Manager(app)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
