from flask import Flask

from flask_script import Manager

import mysql.connector

app = Flask(__name__)
app.config.from_object('config')

db  = mysql.connector.connect(
  host="localhost",
  user="root",
  password="suasenhaaq", #trocar
  database="tweet_gpt"
)

manager = Manager(app)

from app.controllers import default
from app.services import ai_analysis, social_media