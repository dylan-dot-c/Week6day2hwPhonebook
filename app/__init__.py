from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
# setting project config to app.config
app.config.from_object(Config)

login = LoginManager()
login.login_view = 'login'
login.init_app(app)



db = SQLAlchemy(app)

migrate = Migrate(app, db)

from app.blueprints.api import api 
app.register_blueprint(api)



# importing routes and forms so they can be used and access 
from . import routes, models
from . import forms