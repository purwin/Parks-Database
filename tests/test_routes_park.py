import unittest
from flask import request

from base import BaseTests



class TestRoutesPark(BaseTests):

  # Test parks page not logged in
  def test_invalid_parks_not_logged_in(self):
    with self.app:
      response = self.app.get('/parks', follow_redirects=True)

      req = request.url

    self.assertIn(b'/login', req)
    self.assertEqual(response.status_code, 200)


  # Test parks page logged in


  # Test park page not logged in

  # Test park page logged in


  # Test park CREATE page not logged in

  # Test park CREATE page logged in


  # Test park EDIT page not logged in

  # Test park EDIT page logged in


  # Test park DELETE page not logged in

  # Test park DELETE page logged in

if __name__ == "__main__":
  unittest.main()