from flask import Flask, jsonify, request

app = Flask(__name__)


# log in with password
@app.route('/auth', methods=['POST'])
def authorize():
    login = request.get_json()['login']
    password = request.get_json()['password']
    print(login, password)
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
    return True


def generate_token(login):
    return "some token hehe"
