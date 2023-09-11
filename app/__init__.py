
from flask import Flask
app = Flask(__name__)
app.config.from_object('app.config.DefaultConfig')
from app import run