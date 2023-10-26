from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
# setting project config to app.config
app.config.from_object(Config)

db = SQLAlchemy(app)

migrate = Migrate(app, db)

# importing routes and forms so they can be used and access 
from . import routes, models
from . import forms