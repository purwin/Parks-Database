from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CsrfProtect
from flask_talisman import Talisman


app = Flask(__name__, instance_relative_config=True)

# Config currently set to Development Mode
app.config.from_object('config.DevelopmentConfig')
# app.config.from_object('config.ProductionConfig')


CsrfProtect(app)

csp = {
    'default-src': [
      '\'self\'',
      '*.trusted.com'
    ],
    'img-src': '* data:;',
    'script-src': [
      '\'self\'',
      '*.trusted.com',
      'https://code.jquery.com',
      'https://cdnjs.cloudflare.com',
      'https://maxcdn.bootstrapcdn.com'
    ],
    'style-src': [
      '\'self\'',
      '*.trusted.com',
      'https://maxcdn.bootstrapcdn.com',
      'https://fonts.googleapis.com',
      'https://use.fontawesome.com'
    ],
    'font-src': [
      'https://fonts.gstatic.com',
      'https://use.fontawesome.com'
    ]
}

Talisman(
    app,
    content_security_policy=csp,
    content_security_policy_nonce_in=['script-src']
)

db = SQLAlchemy(app)

migrate = Migrate(app, db)

from app import views, parks_db, forms, users