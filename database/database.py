from pymongo import MongoClient
import functools
import json
from flask import Flask, jsonify, request, make_response
import copy, requests

client = MongoClient('mongo', 27017, username='root', password='root')

app = Flask(__name__)
app.debug = True


def error(message, code):
    return make_response(jsonify({"error": message}), code)


def check_params(params_get, params_post):
    def __check_params(func):
        @functools.wraps(func)
        def check_params_inner(*args, **kwargs):
            if request.method == 'GET':
                for param in params_get:
                    if not param in request.args:
                        return error("incorrect GET input", 400)
            if request.method == 'POST':
                for param in params_post:
                    if not param in request.get_json().keys():
                        return error("incorrect POST input", 400)
            return func(*args, **kwargs)

        return check_params_inner

    return __check_params

# curl "http://127.0.0.1:5002?collection=shopping_list&database=organizer"
# curl --header "Content-Type: application/json" --request POST --data '{ "collection": "shopping_list", "database": "organizer", "data": [{"name":"test4", "user": "zaqwer101"}]}' http://127.0.0.1:5002 -k

@app.route('/', methods=['GET', 'POST'])
@check_params(params_get=['database', 'collection'],
              params_post=['database', 'collection', 'data'])
def database_handler():
    # получаем данные из БД
    # query=get
    if request.method == 'GET':
        service_params = ['database', 'collection']
        db_name = request.args['database']
        collection_name = request.args['collection']
        query = {}
        result = []
        for arg in request.args.keys():
            if arg not in service_params:
                query[arg] = request.args[arg]
        app.logger.info(query)
        db = client[db_name]
        collection = db[collection_name]
        for elem in collection.find(query, {'_id': False}):
            app.logger.info(elem)
            result.append(elem)
        return jsonify(result)  # статус 200 по умолчанию
    # вносим данные в БД
    elif request.method == 'POST':
        db_name = request.get_json()['database']
        collection_name = request.get_json()['collection']
        db = client[db_name]
        collection = db[collection_name]
        data = request.get_json()['data']
        app.logger.info(data)

        if len(data) != 0:
            out = []
            for elem in request.get_json()['data']:
                app.logger.info(elem)
                out.append(str(collection.insert_one(elem).inserted_id))
            return make_response(jsonify({"output": out}), 201)  # объект создан
        else:
            return error("empty data", 400)
