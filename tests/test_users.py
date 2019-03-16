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





if __name__ == "__main__":
  unittest.main()
