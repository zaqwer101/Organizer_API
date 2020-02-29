from flask import Flask, jsonify, request
import requests
import errors

app = Flask(__name__)


# curl --header "Content-Type: application/json" --request POST --data '{"secret":"xyz"}' http://127.0.0.1:5000/auth

# TODO: сейчас работать не будет, потому что зашифрованные данные передать сложновато через GET-запрос
@app.route('/auth', methods=['POST'])
def auth():
    secret = request.get_json()['secret']
    print(secret)
    if not secret:
        return jsonify({'error': errors.ERRORS[0]})

    token = requests.get('http://auth:5000/' + secret).json()['token']

    if not token:
        return jsonify({'error': errors.ERRORS[0]})
    else:
        return jsonify({'token': token})


@app.route('/', methods=['GET'])
def root():
    return 'Hello!'
