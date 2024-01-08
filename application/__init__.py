from flask import Flask
from config import Config
from flask_restx import Api


app = Flask(__name__)
app.config.from_object(Config)

api = Api()
from application import routes
