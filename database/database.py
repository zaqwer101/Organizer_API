from pymongo import MongoClient

from flask import Flask, jsonify, request
import copy

app = Flask(__name__)
app.debug = True

client = MongoClient('mongo', 27017, username='root', password='root')
db = client.organizer
users = db['users']
shopping_list = db['shopping_list']


@app.route('/users/<login>')
def get_user(login):
    app.logger.info(login)
    data = users.find_one({"login": login}, {"login": 1, "password": 1, "_id": 0})
    app.logger.info(data)
    if not data:
        return jsonify({"error": "user not found"})
    return data


@app.route('/shoplist', methods=['POST'])
def shoplist_add():
    login = request.get_json()['login']
    name = request.get_json()['name']
    amount = request.get_json()['amount']
    app.logger.info(request.get_json())

    if not login or not name or not amount:
        return jsonify({"error": "incorrect data"})

    data = {'name': name, 'amount': amount, 'login': login}
    out = copy.deepcopy(data)
    app.logger.info(data)
    shopping_list.insert_one(data)
    return out
