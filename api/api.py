import functools

from flask import Flask, jsonify, request
import requests

app = Flask(__name__)
auth_url = "http://auth:5000"
database_url = "http://database:5000"
json_headers = {'content-type': 'application/json'}

def error(message):
    return jsonify({'error': message})

def auth_needed(func):
    @functools.wraps(func)
    def check_auth(*args, **kwargs):
        if 'token' in request.args:
            token = request.args['token']
            r = requests.get(auth_url + "/auth/" + token)
            if r.json()['status'] == 'invalid':
                return error('invalid token')
        else:
            return error('token not set')
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
            return error('no login or password provided')
        if not login or not password:
            return error('empty login or password')
        data = {'login': login, 'password': password}
        token = requests.post(auth_url, json=data, headers=json_headers).content
        if not token:
            return error('invalid login or password')
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

@app.route('/shoplist/add', methods=['POST'])
@auth_needed
def shoplist_add():
    '''
    Параметры: имя, количество
    :return:
    '''
    token = request.args['token']
    if 'name' in request.get_json():
        item_name = request.get_json()['name']
    else:
        return error('no name provided')
    if 'amount' in request.get_json():
        item_amount = request.get_json()['amount']
    else:
        item_amount = 1

    # r = requests.post(database_url + "/add_shoplist_item", data={'name': item_name, 'amount': item_amount}, headers=json_headers)
    # return r.json()
    return token

@app.route('/', methods=['GET'])
@auth_needed
def root():
    return 'Hello!'