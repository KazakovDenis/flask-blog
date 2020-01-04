"""
sudo chown root:user deployer.py
sudo chmod o-rwx deployer.py && sudo chmod g+rwx deployer.py
sudo visudo
add to the end: "nobody ALL = NOPASSWD: deployer.py"
"""
import os
from flask import Flask, request, redirect
from blog.config.config import CONFIG


app = Flask(__name__)
app.logger.filename = 'log/deployer.log'
app.logger.level = 20


def update_app():
    commands = ('cd ~/www/blog', 'git pull origin master', 'supervisorctl restart blog')
    for command in commands:
        app.logger.info(f'Выполняем {command}')
        try:
            os.system(command)
        except Exception as e:
            app.logger.error(f'Не удалось выполнить "{command}": {e}')
            break


def verify_signature(received_signature: hex, request_body: request.data) -> bool:
    # from hmac import HMAC, compare_digest
    # from hashlib import sha1
    # secret = CONFIG.GITHUB_SECRET.encode()
    # expected_sign = HMAC(key=secret, msg=request_body, digestmod=sha1).hexdigest()
    # return compare_digest(received_signature, expected_sign)
    return bool(received_signature)


def check_request(req: request) -> bool:
    received_sign = request.headers.get('X-Hub-Signature').split('sha1=')[-1].strip()
    conditions = (verify_signature(received_sign, req.data),
                  req.data['repository']['id'] == CONFIG.GH_REPO_ID,
                  req.data['sender']['id'] == CONFIG.GH_SENDER_ID,)
    return all(conditions)


@app.route('/hook', methods=['POST', 'GET'])
def hook():
    if request.method == 'POST':
        if check_request(request):
            update_app()
        return 'Successfully', 200
    return redirect('/')


if __name__ == '__main__':
    app.run()
