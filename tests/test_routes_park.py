import unittest
from flask import request

from app import db
from app.parks_db import Park
from base import BaseTests


class TestRoutesPark(BaseTests):

  default_park = dict(
      name='NY Park',
      park_id='W450',
      borough='Queens',
      address='30 Broadway',
      cb='04'
  )


  @staticmethod
  def create_park(**kwargs):
    """
    Static method to add park class object to database
    Takes the following string args: name, park_id, borough, address, cb
    Adds class to Park database, commits session, and flushes to get id val
    Returns the created class instance
    """
    park = Park(**kwargs)
    db.session.add(park)
    db.session.commit()
    db.session.flush()

    return park


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
    self.create_park(
        name=self.default_park['name'],
        park_id=self.default_park['park_id'],
        borough=self.default_park['borough'],
        address=self.default_park['address'],
        cb=self.default_park['cb']
    )

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
              name=self.default_park['name'],
              park_id=self.default_park['park_id'],
              borough=self.default_park['borough'],
              address=self.default_park['address'],
              cb=self.default_park['cb']
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


  # Test POST park EDIT page logged in
  def test_valid_park_edit_post(self):
    new_park = 'NYC Park'
    # Add park to database
    self.create_park(
        name=self.default_park['name'],
        park_id=self.default_park['park_id'],
        borough=self.default_park['borough'],
        address=self.default_park['address'],
        cb=self.default_park['cb']
    )

    with self.app as c:
      with c.session_transaction() as sess:
        sess['url'] = '/'

      self.login()
      response = self.app.post(
          '/parks/1/edit',
          data=dict(
              name=new_park,
              park_id=self.default_park['park_id'],
              borough=self.default_park['borough'],
              address=self.default_park['address'],
              cb=self.default_park['cb']
          ),
          follow_redirects=True
      )

    self.assertIn('"success": true', response.data)
    self.assertIn(new_park, response.data)
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


  # Test GET park DELETE page logged in
  def test_valid_park_delete_get(self):
    # Add park to database
    self.create_park(
        name=self.default_park['name'],
        park_id=self.default_park['park_id'],
        borough=self.default_park['borough'],
        address=self.default_park['address'],
        cb=self.default_park['cb']
    )

    with self.app as c:
      with c.session_transaction() as sess:
        sess['url'] = '/'

      self.login()
      response = self.app.get(
          '/parks/1/delete',
          follow_redirects=True
      )
      req = request.url

    self.assertIn('/parks/1/delete', req)
    self.assertIn('Are you sure you want to delete', response.data)
    self.assertIn(self.default_park['name'], response.data)
    self.assertEqual(response.status_code, 200)


  # Test POST park DELETE page logged in


  # Test GET park DELETE page not logged in
  def test_invalid_park_delete_get_not_logged_in(self):
    with self.app:
      response = self.app.get('/parks/1/delete', follow_redirects=True)
      req = request.url

    self.assertIn(b'/login', req)
    self.assertEqual(response.status_code, 200)


  # Test POST park DELETE page not logged in


if __name__ == "__main__":
  unittest.main()