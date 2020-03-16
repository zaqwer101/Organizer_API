from flask import Flask, jsonify, request
import hashlib
import string
import random
import requests
import redis as __redis

token_ttl = 600
app = Flask(__name__)
redis = __redis.Redis(host='redis', port=6379, db=0)


@app.route('/', methods=['POST'])
def authorize():
    # log in with password
    login = request.get_json()['login']
    password = request.get_json()['password']
    password = encode_password(password)
    app.logger.info("Encoded password: " + password)
    if is_password_match(login, password):
        token = generate_token(login)
        if not token:
            return jsonify({'error': 'max tokens exceeded'})
        return jsonify({'token': token})
    else:
        return jsonify({"error": "invalid credentials"})


@app.route('/auth/<token>', methods=['GET'])
def authenticate(token):
    app.logger.info("Token: " + token)
    if check_token(token):
        return jsonify({"status": "valid"})
    else:
        return jsonify({"status": "invalid"})


def generate_token(login):
    letters = string.ascii_letters
    token = ''.join(random.choice(letters) for i in range(50))
    redis.set(token, login)
    redis.expire(token, token_ttl)
    return token


def check_token(token):
    if redis.get(token):
        redis.expire(token, token_ttl)
        return True
    else:
        return False


def is_password_match(login, password):
    user = get_user(login)
    if user:
        if user['password'] == password:
            return True
    return False


def encode_password(password):
    return hashlib.md5(password.encode()).hexdigest()


def get_user(login):
    user = requests.get('http://database:5000/users/' + login).json()
    if 'error' in user:
        return None
    return user
