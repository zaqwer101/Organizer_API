import functools

from flask import Flask, jsonify, request
import requests, json

app = Flask(__name__)
auth_url = "http://auth:5000"
database_url = "http://database:5000"
json_headers = {'content-type': 'application/json'}

def error(message):
    return jsonify({'error': message})

def auth_needed(func):
    @functools.wraps(func)
    def check_auth(*args, **kwargs):
        if request.method == 'GET':
            app.logger.info('Wrapper GET request')
            if 'token' in request.args:
                token = request.args['token']
                r = requests.get(auth_url + "/auth/" + token)
                if r.json()['status'] == 'invalid':
                    return error('invalid token')
            else:
                return error('token not set')
        elif request.method == 'POST':
            app.logger.info("Wrapper POST request")
            if 'token' in request.get_json():
                app.logger.info(request.get_data())
                app.logger.info(request.get_json())
                token = request.get_json()['token']
                app.logger.info(token)
                r = requests.get(auth_url + "/auth/" + token)
                if r.json()['status'] == 'invalid':
                    return error('invalid token')
            else:
                return error('token not set')
        return func(*args, **kwargs)
    return check_auth


# curl --header "Content-Type: application/json" --request POST --data '{"secret":"xyz"}' http://127.0.0.1:5000/auth

@app.route('/auth', methods=['POST', 'GET'])
def auth():
    # авторизация
    if request.method == 'POST':
        try:
            user = request.get_json()['user']
            password = request.get_json()['password']
        except:
            return error('no user or password provided')
        if not user or not password:
            return error('empty user or password')
        data = {'user': user, 'password': password}
        token = requests.post(auth_url, json=data, headers=json_headers).content
        if not token:
            return error('invalid user or password')
        else:
            return token
    # аутентификация
    if request.method == 'GET':
        if 'token' in request.args:
            token = request.args['token']
            r = requests.get(auth_url + "/auth/" + token)
            return r.json()
        else:
            return error('token not set')

@app.route('/shoplist', methods=['POST'])
@auth_needed
def shoplist_add():
    ### Получаем данные
    token = request.get_json()['token']
    if 'name' in request.get_json():
        item_name = request.get_json()['name']
    else:
        return error('no name provided')
    if 'amount' in request.get_json():
        item_amount = request.get_json()['amount']
    else:
        item_amount = 1

    url = auth_url + "/get_user_by_token/" + token
    data = requests.get(url).json()
    app.logger.info(data)

    if not data['user']:
        return error('can not find user')

    user = data['user']

    ### Отправляем запрос
    data = {'name': item_name, 'amount': item_amount, 'user': user}
    r = requests.post(database_url + "/shoplist", json=data, headers=json_headers)

    return r.json()

@app.route('/', methods=['GET'])
@auth_needed
def root():
    return 'Hello!'

@app.route('/shoplist', methods=['GET'])
@auth_needed
def shoplist_get():
    r = requests.get(database_url + "/shoplist", params={'token': request.args['token']})
    return r.json()

@app.route('/register', methods=['POST'])
def register():
    if not 'user' in request.get_json() or not 'password' in request.get_json():
        return error('user and password required')
    user = request.get_json()['user']
    password = request.get_json()['password']
    data = {'user': user, 'password': password}
    r = requests.post(auth_url + "/register", json=data)
    return r.json()

