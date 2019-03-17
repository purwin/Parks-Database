import unittest
from flask_login import current_user
from werkzeug.security import check_password_hash
from flask import request, session

from base import BaseTests

from app import db
from app.users import User


class TestUsers(BaseTests):

  default_user = {
    "username": 'cool_username',
    "password": 'party123456'
  }

  # Test signup success
  def test_valid_admin_login(self):
    with self.app as c:
      with c.session_transaction() as sess:
        sess['url'] = '/'

      response = self.login()

      user = current_user.username

    self.assertEqual(response.status_code, 200)
    self.assertTrue(user, "admin")


  # Test signup success
  def test_valid_user_signup(self):
    with self.app as c:
      with c.session_transaction() as sess:
        sess['url'] = '/'

      self.login()

      response = self.signup(
          username=self.default_user['username'],
          password=self.default_user['password']
      )

      user = current_user.username

    self.assertEqual(response.status_code, 200)
    self.assertEqual(user, self.default_user['username'])


  # Test signup duplicate
  def test_invalid_user_signup_duplicate(self):
    db.session.add(User(
        username=self.default_user['username'],
        password=self.default_user['password']))
    db.session.commit()

    with self.app as c:
      with c.session_transaction() as sess:
        sess['url'] = '/'

      self.login()

      response = self.signup(
          username=self.default_user['username'],
          password='party123456'
      )

      req = request.url

    self.assertIn(b'Please use a different username.', response.data)
    self.assertIn(b'/signup', req)


  # Test signup not admin
  def test_invalid_user_signup_not_admin(self):
    with self.app as c:
      with c.session_transaction() as sess:
        sess['url'] = '/'

      response = self.signup(
          username=self.default_user['username'],
          password='party123456'
      )

      req = request.url

    print "test_invalid_user_signup_not_admin: ", response

    user = User.query.filter_by(username=self.default_user['username']).first()

    self.assertIn(b'/login', req)
    self.assertIsNone(user)


if __name__ == "__main__":
  unittest.main()
