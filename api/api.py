from flask import Flask, jsonify, request
import requests

app = Flask(__name__)


# curl --header "Content-Type: application/json" --request POST --data '{"secret":"xyz"}' http://127.0.0.1:5000/auth

@app.route('/auth', methods=['POST', 'GET'])
def auth():
    if request.method == 'POST':
        try:
            login = request.get_json()['login']
            password = request.get_json()['password']
            print(login + ", " + password)
        except:
            return jsonify({'error': 'no login or password provided'})
        if not login or not password:
            return jsonify({'error': 'empty login or password'})
        headers = {'content-type': 'application/json'}
        url = "http://auth:5000/auth"
        data = {'login': login, 'password': password}
        token = requests.post(url, json=data, headers=headers).content
        print(token)
        if not token:
            return jsonify({'error': 'invalid login or password'})
        else:
            return token
    if request.method == 'GET':
        if 'token' in request.args:
            token = request.args['token']
            url = "http://auth:5000/auth"
            r = requests.get(url + "/" + token)
            return r.json()
        else:
            return jsonify({'error': 'token not set'})


@app.route('/', methods=['GET'])
def root():
    return 'Hello!'
