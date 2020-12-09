from flask_migrate import MigrateCommand
from flask_script import Manager

from .init import init_app


app = init_app()
manager = Manager(app)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
