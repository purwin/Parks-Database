import unittest

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
    self.app = app.test_client()

    db.drop_all()
    db.create_all()

    db.session.add(User("admin", "admin123456"))
    db.session.commit()

    self.assertEqual(app.debug, False)

  def tearDown(self):
    pass


  ########################
  #### helper methods ####
  ########################


  # Function to create user in app database
  def signup(self, username, password, remember):
    return self.app.post(
      '/signup',
      data=dict(username=username, password=password, remember=remember),
      follow_redirects=True
    )

  # Function to log user into app
  # Set admin username/password as defaults
  def login(self, username="admin", password="admin123456", remember=True):
    return self.app.post(
      '/login',
      data=dict(username=username, password=password, remember=remember),
      follow_redirects=True
    )

  # Function to create log user out of app
  def logout(self):
    return self.app.get(
      '/logout',
      follow_redirects=True
    )