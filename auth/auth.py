from flask import Flask, jsonify, request
import hashlib
import string
import random
import requests
import redis as __redis

MAX_TOKENS_PER_USER = 2

app = Flask(__name__)
redis = __redis.Redis(host='redis', port=6379, db=0)


@app.route('/auth', methods=['POST'])
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
    token = ''.join(random.choice(letters) for i in range(20))
    tokens_count = len(scan_keys(login + "__*"))
    if tokens_count >= MAX_TOKENS_PER_USER:
        return None
    tokens_count += 1
    redis.set(login + "__token__" + str(tokens_count), token)
    redis.expire(login + "__token__" + str(tokens_count), 60)
    return token


def scan_keys(pattern):
    """Returns a list of all the keys matching a given pattern"""
    result = []
    cur, keys = redis.scan(cursor=0, match=pattern, count=2)
    result.extend(keys)
    while cur != 0:
        cur, keys = redis.scan(cursor=cur, match=pattern, count=2)
        result.extend(keys)
    return result


def check_token(token):
    keys = scan_keys("*__token__*")
    app.logger.info("Elems: " + str(len(keys)))
    for key in keys:
        value = redis.get(key.decode()).decode()
        app.logger.info(key.decode() + " " + value)
        if value == token:
            redis.expire(key, 60)
            return True
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
