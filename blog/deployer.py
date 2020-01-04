"""
sudo chown root:user deployer.py
sudo chmod go-rwx deployer.py && sudo chmod g+x deployer.py
sudo visudo
add to the end: "nobody ALL = NOPASSWD: deployer.py"
"""
import logging
import os
from time import time


logging.basicConfig(filename="flask.log", level=logging.DEBUG)
logging.info('Запустили деплоер')


def main():
    commands = ('cd ~/www/blog && pwd', 'git pull origin master', 'supervisorctl restart blog')
    for command in commands:
        try:
            logging.info(f'Выполняем {command}')
            logging.info(f'Выполнено: {os.system(command)}')
        except Exception as e:
            logging.error(f'Не удалось выполнить {command}: {e}')
            break
    return 'Success!', 200


if __name__ == '__main__':
    main()
