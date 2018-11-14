from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CsrfProtect


app = Flask(__name__, instance_relative_config=True)

# Config currently set to Development Mode
app.config.from_object('config.DevelopmentConfig')
# app.config.from_object('config')


CsrfProtect(app)

db = SQLAlchemy(app)

migrate = Migrate(app, db)

from app import views, parks_db, forms