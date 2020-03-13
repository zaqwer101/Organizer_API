from flask import Flask, jsonify, request
import requests

app = Flask(__name__)


# curl --header "Content-Type: application/json" --request POST --data '{"secret":"xyz"}' http://127.0.0.1:5000/auth

@app.route('/auth', methods=['POST'])
def auth():
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


@app.route('/', methods=['GET'])
def root():
    return 'Hello!'
