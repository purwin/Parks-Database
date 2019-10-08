import unittest
from flask import request

from app import db
from app.parks_db import Artist
from base import BaseTests



class TestRoutesArtist(BaseTests):

  default_artist = dict(
      pName='Person',
      fName='Cool',
      email='cool_person@website.com',
      phone='555-345-5678',
      website='www.party.com'
  )

  @staticmethod
  def create_artist(**kwargs):
    """
    Static method to add artist class object to database
    Takes the following string args: pName, fName, email, phone, website
    Adds class to Artist database, commits session, and flushes to get id val
    Returns the created class instance
    """
    artist = Artist(**kwargs)
    db.session.add(artist)
    db.session.commit()
    db.session.flush()

    return artist


  # Test artists page not logged in
  def test_invalid_artists_not_logged_in(self):
    with self.app:
      response = self.app.get('/artists', follow_redirects=True)
      req = request.url

    self.assertIn(b'/login', req)
    self.assertEqual(response.status_code, 200)


  # Test artists page logged in
  def test_valid_artists_logged_in(self):
    with self.app as c:
      with c.session_transaction() as sess:
        sess['url'] = '/'

      self.login()
      response = self.app.get('/artists', follow_redirects=True)
      req = request.url

    self.assertIn(b'/artists', req)
    self.assertEqual(response.status_code, 200)


  # Test artist page not logged in
  def test_invalid_artist_not_logged_in(self):
    artist = self.default_artist
    # Add artist to database
    self.create_artist(**artist)

    with self.app:
      response = self.app.get('/artists/1', follow_redirects=True)
      req = request.url

    self.assertIn(b'/login', req)
    self.assertEqual(response.status_code, 200)


  # Test artist page logged in
  def test_valid_artist_logged_in(self):
    artist = self.default_artist
    # Add artist to database
    self.create_artist(**artist)

    with self.app as c:
      with c.session_transaction() as sess:
        sess['url'] = '/'

      self.login()
      response = self.app.get('/artists/1', follow_redirects=True)
      req = request.url

    self.assertIn(b'/artists/1', req)
    self.assertEqual(response.status_code, 200)


  # Test artist page with no artists
  def test_invalid_artist_no_artists(self):
    with self.app as c:
      with c.session_transaction() as sess:
        sess['url'] = '/'

      self.login()
      response = self.app.get('/artists/1', follow_redirects=True)
      req = request.url

    self.assertIn(b'/artists/1', req)
    self.assertEqual(response.status_code, 404)


  # Test GET artist CREATE page
  def test_invalid_artist_create_get(self):
    with self.app:
      response = self.app.get('/artists/create', follow_redirects=True)

    self.assertIn('Method Not Allowed', response.data)
    self.assertEqual(response.status_code, 405)


  # Test artist CREATE page logged in
  def test_valid_artist_create_post(self):
    artist = self.default_artist
    with self.app as c:
      with c.session_transaction() as sess:
        sess['url'] = '/'

      self.login()
      response = self.app.post(
          '/artists/create',
          data=artist,
          follow_redirects=True
      )

    self.assertIn('"success": true', response.data)
    self.assertEqual(response.status_code, 200)


  # Test artist CREATE page not logged in
  def test_invalid_artist_create_post(self):
    artist = self.default_artist
    with self.app as c:
      response = self.app.post(
          '/artists/create',
          data=artist,
          follow_redirects=True
      )
      req = request.url

    self.assertIn(b'/login', req)
    self.assertEqual(response.status_code, 200)


  # Test POST artist EDIT page logged in
  def test_valid_artist_edit_post(self):
    artist = self.default_artist
    new_artist_fName = 'Cooler'
    # Add artist to database
    self.create_artist(**artist)

    with self.app as c:
      with c.session_transaction() as sess:
        sess['url'] = '/'

      self.login()
      response = self.app.post(
          '/artists/1/edit',
          data=dict(
              fName=new_artist_fName,
              pName=artist['pName'],
              email=artist['email'],
              phone=artist['phone'],
              website=artist['website']
          ),
          follow_redirects=True
      )

    self.assertIn('"success": true', response.data)
    self.assertIn(new_artist_fName, response.data)
    self.assertEqual(response.status_code, 200)


  # Test POST artist EDIT page not logged in
  def test_invalid_artist_edit_post(self):
    artist = self.default_artist
    new_artist_fName = 'Cooler'
    # Add artist to database
    self.create_artist(**artist)

    with self.app as c:
      response = self.app.post(
          '/artists/1/edit',
          data=dict(
              fName=new_artist_fName,
              pName=artist['pName'],
              email=artist['email'],
              phone=artist['phone'],
              website=artist['website']
          ),
          follow_redirects=True
      )
      req = request.url

    self.assertIn(b'/login', req)
    self.assertEqual(response.status_code, 200)


  # Test artist DELETE page logged in
  def test_valid_artist_delete_post(self):
    artist = self.default_artist
    # Add artist to database
    self.create_artist(**artist)

    with self.app as c:
      with c.session_transaction() as sess:
        sess['url'] = '/'

      self.login()
      response = self.app.post(
          '/artists/1/delete',
          follow_redirects=True
      )
      req = request.url

      retry = self.app.get(
          '/artists/1',
          follow_redirects=True
      )

    self.assertIn('/artists', req)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(retry.status_code, 404)


  # Test artist DELETE page not logged in
  def test_invalid_artist_delete_post(self):
    artist = self.default_artist
    # Add artist to database
    self.create_artist(**artist)

    with self.app as c:
      response = self.app.post(
          '/artists/1/delete',
          follow_redirects=True
      )
      req = request.url

    self.assertIn(b'/login', req)
    self.assertEqual(response.status_code, 200)