import unittest
from flask import request

from app import db
from app.parks_db import Park
from base import BaseTests


class TestRoutesPark(BaseTests):

  # Test parks page logged in
  def test_valid_parks_logged_in(self):
    with self.app as c:
      with c.session_transaction() as sess:
        sess['url'] = '/'

      self.login()
      response = self.app.get('/parks', follow_redirects=True)
      req = request.url

    self.assertIn(b'/parks', req)
    self.assertEqual(response.status_code, 200)


  # Test parks page not logged in
  def test_invalid_parks_not_logged_in(self):
    with self.app:
      response = self.app.get('/parks', follow_redirects=True)
      req = request.url

    self.assertIn(b'/login', req)
    self.assertEqual(response.status_code, 200)


  # Test park page with no parks
  def test_valid_park(self):
    # Add park to database
    park = Park(
        name='NY Park',
        park_id='W450',
        borough='Queens',
        address='30 Broadway',
        cb='04'
    )
    db.session.add(park)
    db.session.commit()

    with self.app as c:
      with c.session_transaction() as sess:
        sess['url'] = '/'

      self.login()
      response = self.app.get('/park/1', follow_redirects=True)
      req = request.url

    self.assertIn(b'/park/1', req)
    self.assertEqual(response.status_code, 404)


  # Test park page with no parks
  def test_invalid_park_no_parks(self):
    with self.app as c:
      with c.session_transaction() as sess:
        sess['url'] = '/'

      self.login()
      response = self.app.get('/park/1', follow_redirects=True)
      req = request.url

    self.assertIn(b'/park/1', req)
    self.assertEqual(response.status_code, 404)


  # Test parks page not logged in


  # Test park CREATE page not logged in

  # Test park CREATE page logged in


  # Test park EDIT page not logged in

  # Test park EDIT page logged in


  # Test park DELETE page not logged in

  # Test park DELETE page logged in

if __name__ == "__main__":
  unittest.main()