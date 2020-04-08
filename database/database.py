from pymongo import MongoClient
import functools

from flask import Flask, jsonify, request
import copy,requests

app = Flask(__name__)
app.debug = True

def error(message):
    return jsonify({'error': message})


def check_params(params):
    def __check_params(func):
        @functools.wraps(func)
        def check_params_inner(*args, **kwargs):
            if request.method == 'GET':
                for param in params:
                    if not param in request.args:
                        return jsonify({"error": "incorrect input"})
            if request.method == 'POST':
                for param in params:
                    if not param in request.get_json().keys():
                        return jsonify({"error": "incorrect input"})
            return func(*args, **kwargs)

        return check_params_inner

    return __check_params

user_fields = {"user": 1, "password": 1, "_id": 0}
shopping_list_fields = {"name": 1, "amount": 1, "_id": 0 }
client = MongoClient('mongo', 27017, username='root', password='root')
db = client.organizer
users_collection = db['users']
shopping_list_collection = db['shopping_list']
auth_url = 'http://auth:5000'


# @app.route('/users/<user>', methods=['GET'])
# def get_user(user):
#     app.logger.info(user)
#     data = users_collection.find_one({"user": user}, user_fields)
#     app.logger.info(data)
#     if not data:
#         return jsonify({"error": "user not found"})
#     return data
#
# @app.route('/users', methods=['POST'])
# def add_user():
#     user = request.get_json()['user']
#     password = request.get_json()['password']
#     data = { 'user': user, 'password': password }
#     users_collection.insert_one(data)
#     return jsonify({"success": "true"})
#
#
# @app.route('/shoplist', methods=['POST'])
# def shoplist_add():
#     user = request.get_json()['user']
#     name = request.get_json()['name']
#     amount = request.get_json()['amount']
#     app.logger.info(request.get_json())
#
#     if not user or not name or not amount:
#         return jsonify({"error": "incorrect data"})
#
#     data = {'name': name, 'amount': amount, 'user': user}
#     out = copy.deepcopy(data)
#     app.logger.info(data)
#     shopping_list_collection.insert_one(data)
#     return out
#
# def get_user_by_token(token):
#     content = requests.get(auth_url + "/get_user_by_token/" + token).json()
#     if not 'error'in content:
#         user = content['user']
#         return user
#     return None
#
#
# @app.route('/shoplist', methods=['GET'])
# def shoplist_get():
#     token = request.args['token']
#     app.logger.info(token)
#     user = get_user_by_token(token)
#     app.logger.info(user)
#     if not user:
#         return error('token not found')
#     shopping_list_query = shopping_list_collection.find({"user": user}, shopping_list_fields)
#     shopping_list = []
#     for elem in shopping_list_query:
#         shopping_list.append(elem)
#     shopping_list = {"elems": shopping_list}
#     app.logger.info(shopping_list)
#     return jsonify(shopping_list)


# curl "http://127.0.0.1:5002?table=shoplist&database=organizer&query=kek&token=dfssd"
# curl --header "Content-Type: application/json" --request POST --data '{ "table": "shoplist", "database": "organizer", "query": "none", "token":"asd" }' http://127.0.0.1:5002 -k
@app.route('/', methods=['GET', 'POST'])
@check_params(params=['database', 'table', 'query', 'token'])
def database_handler():
    # получаем данные из БД
    if request.method == 'GET':
        pass
    # вносим данные в БД
    elif request.method == 'POST':
        pass
    return jsonify({"status": "success"})
