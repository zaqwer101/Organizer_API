import functools
from flask import Flask, jsonify, request, make_response
import requests, json

database = "organizer"
collection = "shoplist"
database_url = "http://database:5000"
json_headers = {'content-type': 'application/json'}

app = Flask(__name__)
app.debug = True


def error(message, code):
    return make_response(jsonify({"error": message}), code)


def check_params(params_get=None, params_post=None, params_delete=None, params_put=None):
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
            if request.method == 'DELETE':
                for param in params_delete:
                    if not param in request.get_json().keys():
                        return error("incorrect DELETE input", 400)
            if request.method == 'PUT':
                for param in params_put:
                    if not param in request.get_json().keys():
                        return error("incorrect PUT input", 400)
            return func(*args, **kwargs)

        return check_params_inner

    return __check_params


@check_params(params_get=["user"],
              params_post=["user", "name"],  # amount необязательное поле
              params_delete=["user", "name"])
@app.route("/", methods=["GET", "POST", "DELETE"])
def shoplist():
    pass


def get_item_by_name(user, name):
    r = reqests.get(database_url, params={"user": user, "name": name, "database": database, "collection": collection},
                    headers=json_headers)
    if r.status_code == 400:
        error("incorrect params", 400)
    if r.status_code == 404:
        return None
    return r.json()

def get_items_by_user(user):
    pass