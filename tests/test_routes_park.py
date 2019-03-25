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


  # Test park page
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
      response = self.app.get('/parks/1', follow_redirects=True)
      req = request.url

    self.assertIn(b'/parks/1', req)
    self.assertEqual(response.status_code, 200)


  # Test park page with no parks
  def test_invalid_park_no_parks(self):
    with self.app as c:
      with c.session_transaction() as sess:
        sess['url'] = '/'

      self.login()
      response = self.app.get('/parks/1', follow_redirects=True)
      req = request.url

    self.assertIn(b'/parks/1', req)
    self.assertEqual(response.status_code, 404)


  # Test park page not logged in
  def test_invalid_park_not_logged_in(self):
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

    with self.app:
      response = self.app.get('/parks/1', follow_redirects=True)
      req = request.url

    self.assertIn(b'/login', req)
    self.assertEqual(response.status_code, 200)


  # Test GET park CREATE page
  def test_invalid_park_create_get(self):
    with self.app:
      response = self.app.get('/parks/create', follow_redirects=True)

    self.assertIn('Method Not Allowed', response.data)
    self.assertEqual(response.status_code, 405)


  # Test park CREATE page logged in
  def test_valid_park_create_post(self):
    with self.app as c:
      with c.session_transaction() as sess:
        sess['url'] = '/'

      self.login()
      response = self.app.post(
          '/parks/create',
          data=dict(
              name='NY Park',
              park_id='W450',
              borough='Queens',
              address='30 Broadway',
              cb='04'
          ),
          follow_redirects=True
      )

    self.assertIn('"success": true', response.data)
    self.assertEqual(response.status_code, 200)


  # Test POST park CREATE page not logged in
  def test_invalid_park_create_post_not_logged_in(self):
    with self.app:
      response = self.app.post('/parks/create', follow_redirects=True)
      req = request.url

    self.assertIn(b'/login', req)
    self.assertEqual(response.status_code, 200)


  # Test GET park EDIT page
  def test_invalid_park_edit_get(self):
    with self.app:
      response = self.app.get('/parks/1/edit', follow_redirects=True)

    self.assertIn('Method Not Allowed', response.data)
    self.assertEqual(response.status_code, 405)


  # Test POST park EDIT page not logged in
  def test_invalid_park_edit_post_not_logged_in(self):
    with self.app:
      response = self.app.post('/parks/1/edit', follow_redirects=True)
      req = request.url

    self.assertIn(b'/login', req)
    self.assertEqual(response.status_code, 200)

  # Test park EDIT page logged in


  # Test park DELETE page not logged in

  # Test park DELETE page logged in

if __name__ == "__main__":
  unittest.main()