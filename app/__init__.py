import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import app_config

app = Flask(__name__)
app.config.from_object(app_config.get(os.environ.get('APP_SETTINGS')))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
