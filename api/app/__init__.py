from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object('config')

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:12345@localhost:3306/tweet_gpt'
db =  SQLAlchemy(app)
migrate = Migrate(app, db, command='migrate')

manager = Manager(app)

from app.models import tables
from app.controllers import default
from app.services import ai_analysis, social_media