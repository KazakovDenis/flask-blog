"""
sudo chown root:user deployer.py
sudo chmod go-rwx deployer.py && sudo chmod g+x deployer.py
sudo visudo
add to the end: "nobody ALL = NOPASSWD: deployer.py"
"""
import os
from time import time


def main():
    commands = ('cd ~/www/blog', 'git pull origin master', 'supervisorctl restart blog')
    for command in commands:
        try:
            os.system(command)
        except Exception as e:
            with open('update.log', 'a') as f:
                f.write(f'{time()} --- Error during execution the command: {command} \n {e}')
            break


if __name__ == '__main__':
    main()
