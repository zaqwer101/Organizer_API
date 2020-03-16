from pymongo import MongoClient

from flask import Flask, jsonify, request

app = Flask(__name__)

client = MongoClient('mongo', 27017, username='root', password='root')
db = client.organizer
users = db['users']


@app.route('/users/<login>')
def get_user(login):
    app.logger.info(login)
    data = users.find_one({"login": login}, {"login": 1, "password": 1, "_id": 0})
    app.logger.info(data)
    if not data:
        return jsonify({"error": "user not found"})
    return data


@app.route('/add_shoplist_item')
def add_shoplist_item():
    pass
