import random
import string
import keys_manager
from flask import Flask, jsonify

app = Flask(__name__)


def generate_token():
    return ''.join(random.choice(string.ascii_letters) for i in range(40))


def auth(incoming_data, verification_string):
    if keys_manager.decrypt(incoming_data) == keys_manager.decrypt(verification_string):
        token = generate_token()
        # TODO записываем token в БД куда-нить
        return token


@app.route('/<secret>')
def get_token(secret):
    return jsonify({'token': generate_token()})
