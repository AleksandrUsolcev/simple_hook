import hashlib
import hmac
import os
import subprocess

from dotenv import load_dotenv
from flask import Flask, abort, request
from git import Repo

load_dotenv()
app = Flask(__name__)
app.config['DEBUG'] = False

# secret key from github webhooks
SECRET = os.getenv('SECRET')
# local repository path, example: /home/my_project/repo_folder/
REPO_PATH = os.getenv('REPO_PATH')
# local docker-compose path
COMPOSE_PATH = os.getenv('COMPOSE_PATH')


@app.route('/webhook', methods=['POST'])
def webhook():
    signature = request.headers.get('X-Hub-Signature')

    if not is_valid_signature(signature, request.data, SECRET):
        abort(403, 'Signature is failed')

    # data = request.get_json()
    # repo_url = data.get('repository').get('html_url')

    if is_git_repository(REPO_PATH):
        git_pull(REPO_PATH)
        docker_compose(COMPOSE_PATH)


def is_valid_signature(signature, payload, secret):
    if signature is None:
        return False
    _, signature = signature.split('=')
    expected_signature = hmac.new(
        secret.encode(),
        payload, hashlib.sha1).hexdigest()
    return hmac.compare_digest(signature, expected_signature)


def is_git_repository(folder_path):
    try:
        repo = Repo(folder_path)
        return repo.git_dir.endswith('.git')
    except Exception:
        return False


def git_pull(folder_path):
    subprocess.run(['git', 'pull'], cwd=folder_path)


def docker_compose(folder_path):
    command = ['docker', 'compose', 'up', '-d', '--build']
    subprocess.run(command, cwd=folder_path)


if __name__ == '__main__':
    app.run()
