from flask import Flask
import requests
import configparser

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello world!'
