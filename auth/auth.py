from flask import Flask, jsonify, request
import hashlib
import requests

app = Flask(__name__)


# log in with password
@app.route('/auth', methods=['POST'])
def authorize():
    login = request.get_json()['login']
    password = request.get_json()['password']
    password = encode_password(password)

    app.logger.info("Encoded password: " + password)
    if is_login_exists(login):
        if is_password_match(login, password):
            token = generate_token(login)
            return jsonify({'token': token})
        else:
            return jsonify({"error": "invalid credentials"})


# check permissions with token
def authenticate(token):
    if check_token(token):
        return jsonify({"status": "valid"})
    else:
        return jsonify({"status": "invalid"})


def check_token(login, token):
    return True


def is_login_exists(login):
    return True


def is_password_match(login, password):
    user = get_user(login)
    if user:
        if user['password'] == password:
            return True
    return False


def generate_token(login):
    return "some token hehe"


def encode_password(password):
    return hashlib.md5(password.encode()).hexdigest()


def get_user(login):
    user = requests.get('http://database:5000/users/' + login).json()
    if 'error' in user:
        return None
    return user
