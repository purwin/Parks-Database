import unittest
from werkzeug.security import generate_password_hash

from app import app, db
from app.users import User


class BaseTests(unittest.TestCase):


  ############################
  #### setup and teardown ####
  ############################


  def create_app(self):
    app.config.from_object('config.TestConfig')
    return app


  def setUp(self):
    self.create_app()
    self.app = app.test_client()
    db.create_all()
    pw = generate_password_hash("admin123456",
      method='sha256')
    db.session.add(User(username="admin", password=pw))
    db.session.commit()


  def tearDown(self):
    db.session.remove()
    db.drop_all()


  ########################
  #### helper methods ####
  ########################


  # Function to create user in app database
  def signup(self, username, password):
    return self.app.post(
      '/signup',
      data=dict(username=username, password=password),
      follow_redirects=True
    )

  # Function to log user into app
  # Set admin username/password as defaults
  def login(self, username="admin", password="admin123456"):
    return self.app.post(
      '/login',
      data=dict(username=username, password=password),
      follow_redirects=True
    )

  # Function to create log user out of app
  def logout(self):
    return self.app.get(
      '/logout',
      follow_redirects=True
    )