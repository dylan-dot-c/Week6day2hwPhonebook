from flask import Flask
from config import Config

app = Flask(__name__)
# setting project config to app.config
app.config.from_object(Config)

# importing routes and forms so they can be used and access 
from . import routes
from . import forms