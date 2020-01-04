import os
from flask import Flask, request, redirect
from config.config import *


depl = Flask('Deployer')
depl.logger.filename = PATH + '/log/deployer/deployer.log'
depl.logger.level = 20


def update_app():
    commands = (f'cd {PATH}', 'git pull origin master', 'supervisorctl restart blog')
    for command in commands:
        depl.logger.info(f'Выполняем "{command}"')
        try:
            os.system(command)
        except Exception as e:
            depl.logger.error(f'Не удалось выполнить "{command}": {e}')
            break


def verify_signature(received_signature, request_body) -> bool:
    # from hmac import HMAC, compare_digest
    # from hashlib import sha1
    # secret = CONFIG.GITHUB_SECRET.encode()
    # expected_sign = HMAC(key=secret, msg=request_body, digestmod=sha1).hexdigest()
    # return compare_digest(received_signature, expected_sign)
    return bool(received_signature)


def check_request(req) -> bool:
    received_sign = req.headers.get('X-Hub-Signature').split('sha1=')[-1].strip()
    conditions = (verify_signature(received_sign, req.data),
                  req.json.get('repository').get('id') == GH_REPO_ID,
                  req.json.get('sender').get('id') == GH_SENDER_ID,)
    return all(conditions)


@depl.route('/hook', methods=['POST', 'GET'])
def hook():
    if request.method == 'POST':
        if check_request(request):
            update_app()
            return 'Successfully', 200
        else:
            return 'Forbidden', 403
    return redirect('', code=301)


if __name__ == '__main__':
    depl.run()
