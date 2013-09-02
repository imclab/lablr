import os
import easypost
from flask import Flask
from flask.ext.restful import Api
from constants import *

#project paths
app_dir = os.path.abspath(os.path.join(os.path.dirname(__file__)))
base_dir = os.path.abspath(os.path.join(app_dir, '..'))

#startup app
app = Flask(__name__, static_folder=os.path.join(base_dir, 'static'))

#set secret key
from app.constants import APP_SECRET_KEY
app.secret_key = APP_SECRET_KEY

#api
api = Api(app)

#initialize urls and api endpoints
from urls import initialize_urls
initialize_urls()

#set easypost api key
easypost.api_key = EASYPOST_TEST_KEY

