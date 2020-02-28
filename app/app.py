from flask import Flask, jsonify
import requests
import app.errors

app = Flask(__name__)


# TODO: сейчас работать не будет, потому что зашифрованные данные передать сложновато через GET-запрос
@app.route('/auth/<secret>')
def auth(secret):
    token = requests.get('http://auth:5000/' + secret)
    if not token:
        return jsonify({'error': app.ERRORS[0]})
    else:
        return jsonify({'token': token})
