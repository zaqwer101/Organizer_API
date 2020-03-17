from flask import Flask, jsonify, request
import hashlib
import string
import random
import requests
import redis as __redis

def error(message):
    return jsonify({'error': message})

token_ttl = 600
app = Flask(__name__)
redis = __redis.Redis(host='redis', port=6379, db=0)
database_url = 'http://database:5000'


@app.route('/register', methods=['POST'])
def register():
    user = request.get_json()['user']
    password = request.get_json()['password']
    password = encode_password(password)

    # проверяем есть ли уже такой юзер в бд
    if get_user_by_name(user):
        return error('user exists')

    data = {'user': user, 'password': password}

    # вносим юзера в БД
    r = requests.post(database_url + '/users', json=data)
    app.logger.info(get_user_by_name(user))
    if r.json()['success'] == 'true':
        return jsonify({'token': generate_token(user)})


@app.route('/', methods=['POST'])
def authorize():
    # log in with password
    user = request.get_json()['user']
    password = request.get_json()['password']
    password = encode_password(password)
    app.logger.info("Encoded password: " + password)
    if is_password_match(user, password):
        token = generate_token(user)
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


def generate_token(user):
    letters = string.ascii_letters
    token = ''.join(random.choice(letters) for i in range(50))
    redis.set(token, user)
    redis.expire(token, token_ttl)
    return token


def check_token(token):
    if redis.get(token):
        redis.expire(token, token_ttl)
        return True
    else:
        return False


def is_password_match(user, password):
    # TODO отрефакторить на JSON
    user = get_user_by_name(user)
    if user:
        if user['password'] == password:
            return True
    return False


def encode_password(password):
    return hashlib.md5(password.encode()).hexdigest()


def get_user_by_name(user):
    user = requests.get(database_url + '/users/' + user).json()
    if 'error' in user:
        return None
    return user


@app.route('/get_user_by_token/<token>')
def get_user_by_token(token):
    user = redis.get(token).decode()
    if user:
        return jsonify({"user": user})
    else:
        return jsonify({'error': 'invalid token'})
