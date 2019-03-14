import unittest

from app import app, db
from base import BasicTests



class TestUsers(BasicTests):

  # Test signup success
  def test_valid_user_signup(self):
    # Login as Admin
    self.login()

    response = self.signup('cool_username', 'party123456', True)

    print "test_valid_user_signup: ", response

    user = User.query.filter_by(username = 'cool_username').first()

    self.assertEqual(response.status_code, 200)
    self.assertIsNotNone(user)
    self.assertTrue(current_user.name == "cool_username")
    self.assertTrue(current_user.is_active())
    self.assertTrue(check_password_hash(user.password, 'admin123456'))
    self.assertFalse(check_password_hash(user.password, 'foobar'))


  # Test signup duplicate
  def test_invalid_user_signup_duplicate(self):
    # Login as Admin
    self.login()

    self.signup('cool_username', 'party123456', True)

    # Sign up duplicate user
    response = self.signup('cool_username', 'surfing123456', True)

    print "test_invalid_user_signup_duplicate: ", response

    self.assertIn(b'Please use a different username.', response.data)
    self.assertIn(b'/signup/', request.url)


  # Test signup not admin
  def test_invalid_user_signup_not_admin(self):
    response = self.signup('cool_username', 'party123456', True)

    print "test_invalid_user_signup_not_admin: ", response

    user = User.query.filter_by(username = 'cool_username').first()

    self.assertIn(b'/signup/', request.url)
    self.assertIsNone(user)


  # Test login admin
  def test_valid_admin_login(self):
    # Login as Admin
    self.login()

    response = self.signup('cool_username', 'party123456', True)

    print "test_valid_admin_login: ", response

    self.assertEqual(response.status_code, 200)


  # Test login success
  def test_valid_user_login(self):
    # Login as Admin
    self.login()

    # Create user
    self.signup('cool_username', 'party123456', True)

    # Logout Admin
    self.logout()

    response = self.signup('cool_username', 'party123456', True)

    print "test_valid_user_login: ", response

    self.assertEqual(response.status_code, 200)


  # Test login wrong password
  def test_invalid_user_login_password(self):
    # Login as Admin
    self.login()

    # Create user
    self.signup('cool_username', 'party123456', True)

    # Logout Admin
    self.logout()

    response = self.signup('cool_username', '123456party', True)

    print "test_invalid_user_login_password: ", response

    self.assertIn(b'Incorrect password!', response.data)
    self.assertIn(b'/login/', request.url)


  # Test login wrong user
  def test_invalid_user_login_no_user(self):
    response = self.signup('cool_username', 'party123456', True)

    print "test_invalid_user_login_no_user: ", response

    self.assertIn(b'User not found!', response.data)
    self.assertIn(b'/login/', request.url)


  # Test logout
  def test_valid_user_logout(self):
    # Login as Admin
    self.login()

    response = self.logout()

    print "test_valid_user_logout RESPONSE: ", response

    retry = self.client.get('/', follow_redirects=True)

    print "test_valid_user_logout RETRY: ", retry

    self.assertEqual(response.status_code, 200)
    self.assertIn(b'/login/', retry.url)



  # Test logout not signed in
  # FUTURE: Views: Update to redirect to home()


if __name__ == "__main__":
  unittest.main()
