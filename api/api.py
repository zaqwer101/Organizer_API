import functools

from flask import Flask, jsonify, request
import requests

app = Flask(__name__)
auth_url = "http://auth:5000/auth"


def auth_needed(func):
    @functools.wraps(func)
    def check_auth(*args, **kwargs):
        if 'token' in request.args:
            token = request.args['token']
            r = requests.get(auth_url + "/" + token)
            if r.json()['status'] == 'invalid':
                return jsonify({'error': "invalid token"})
        else:
            return jsonify({'error': 'token not set'})
        return func(*args, **kwargs)

    app.logger.info('Wrapped!')
    return check_auth


# curl --header "Content-Type: application/json" --request POST --data '{"secret":"xyz"}' http://127.0.0.1:5000/auth

@app.route('/auth', methods=['POST', 'GET'])
def auth():
    # авторизация
    if request.method == 'POST':
        try:
            login = request.get_json()['login']
            password = request.get_json()['password']
        except:
            return jsonify({'error': 'no login or password provided'})
        if not login or not password:
            return jsonify({'error': 'empty login or password'})
        data = {'login': login, 'password': password}
        token = requests.post(auth_url, json=data, headers={'content-type': 'application/json'}).content
        if not token:
            return jsonify({'error': 'invalid login or password'})
        else:
            return token
    # аутентификация
    if request.method == 'GET':
        if 'token' in request.args:
            token = request.args['token']
            url = "http://auth:5000/auth"
            r = requests.get(url + "/" + token)
            return r.json()
        else:
            return jsonify({'error': 'token not set'})


@app.route('/', methods=['GET'])
@auth_needed
def root():
    return 'Hello!'
