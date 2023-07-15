from flask import Flask

from flask_script import Manager

import mysql.connector

from dotenv import load_dotenv
load_dotenv()
from os import environ
host = environ['DB_HOST']
user = environ['DB_USER']
password = environ['DB_PASSWORD']
database = environ['DB_NAME']

app = Flask(__name__)
app.config.from_object('config')

db  = mysql.connector.connect(
  host=host,
  user=user,
  password=password,
  database=database
)

manager = Manager(app)

from app.controllers import default
from app.services import ai_analysis, social_media