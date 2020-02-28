from flask import Flask, jsonify
import requests

app = Flask(__name__)


@app.route('/')
def root():
    token = requests.get('http://auth:5000')
    return token.content
