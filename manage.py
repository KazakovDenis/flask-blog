from flask_migrate import MigrateCommand
from flask_script import Manager

from blog.wsgi import app
from blog.commands.init_app import init_command


manager = Manager(app)
manager.add_command('db', MigrateCommand)
manager.add_command('init_app', init_command)


if __name__ == '__main__':
    manager.run()
