from app import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(30), unique=True)
  password = db.Column(db.String(80))


def init_db():
  db.create_all()


if __name__ == '__main__':
  init_db()