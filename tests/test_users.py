import unittest
from flask_login import current_user
from werkzeug.security import check_password_hash
from flask import request, session

from base import BaseTests

from app.users import User


class TestUsers(BaseTests):

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
    signup_user = {
      "username": 'cool_username',
      "password": 'party123456'
    }

    with self.app as c:
      with c.session_transaction() as sess:
        sess['url'] = '/'

      self.login()

      response = self.signup(
          username=signup_user['username'],
          password=signup_user['password']
      )

      user = current_user.username

    self.assertEqual(response.status_code, 200)
    self.assertEqual(user, signup_user['username'])





if __name__ == "__main__":
  unittest.main()
