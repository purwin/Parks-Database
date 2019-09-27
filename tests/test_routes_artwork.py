import unittest
from flask import request

from app import db
from app.parks_db import Artwork
from base import BaseTests



class TestRoutesArtwork(BaseTests):

  default_artwork = dict(
      name='Fancy Artwork'
  )

  @staticmethod
  def create_artwork(**kwargs):
    """
    Static method to add artwork class object to database
    Takes the following string arg: name
    Adds class to Artwork database, commits session, and flushes to get id val
    Returns the created class instance
    """
    artwork = Artwork(**kwargs)
    db.session.add(artwork)
    db.session.commit()
    db.session.flush()

    return artwork


  # Test artworks page not logged in
  def test_invalid_artworks_not_logged_in(self):
    with self.app:
      response = self.app.get('/artworks', follow_redirects=True)
      req = request.url

    self.assertIn(b'/login', req)
    self.assertEqual(response.status_code, 200)


  # Test artworks page logged in
  def test_valid_artworks_logged_in(self):
    with self.app as c:
      with c.session_transaction() as sess:
        sess['url'] = '/'

      self.login()
      response = self.app.get('/artworks', follow_redirects=True)
      req = request.url

    self.assertIn(b'/artworks', req)
    self.assertEqual(response.status_code, 200)


  # Test artwork page not logged in
  def test_invalid_artwork_not_logged_in(self):
    artwork = self.default_artwork
    # Add artwork to database
    self.create_artwork(**artwork)

    with self.app:
      response = self.app.get('/artworks/1', follow_redirects=True)
      req = request.url

    self.assertIn(b'/login', req)
    self.assertEqual(response.status_code, 200)


  # Test artwork page logged in
  def test_valid_artwork_logged_in(self):
    artwork = self.default_artwork
    # Add artwork to database
    self.create_artwork(**artwork)

    with self.app as c:
      with c.session_transaction() as sess:
        sess['url'] = '/'

      self.login()
      response = self.app.get('/artworks/1', follow_redirects=True)
      req = request.url

    self.assertIn(b'/artworks/1', req)
    self.assertEqual(response.status_code, 200)


 # Test artwork page with no artworks
  def test_invalid_artwork_no_artworks(self):
    with self.app as c:
      with c.session_transaction() as sess:
        sess['url'] = '/'

      self.login()
      response = self.app.get('/artworks/1', follow_redirects=True)
      req = request.url

    self.assertIn(b'/artworks/1', req)
    self.assertEqual(response.status_code, 404)


  # Test GET artwork CREATE page
  def test_invalid_artwork_create_get(self):
    with self.app:
      response = self.app.get('/artworks/create', follow_redirects=True)

    self.assertIn('Method Not Allowed', response.data)
    self.assertEqual(response.status_code, 405)


  # Test artwork CREATE page logged in
  def test_valid_artwork_create_post(self):
    artwork = self.default_artwork
    with self.app as c:
      with c.session_transaction() as sess:
        sess['url'] = '/'

      self.login()
      response = self.app.post(
          '/artworks/create',
          data=artwork,
          follow_redirects=True
      )

    self.assertIn('"success": true', response.data)
    self.assertEqual(response.status_code, 200)


  # Test artwork CREATE page not logged in
  def test_invalid_artwork_create_post(self):
    artwork = self.default_artwork
    with self.app as c:
      response = self.app.post(
          '/artworks/create',
          data=artwork,
          follow_redirects=True
      )
      req = request.url

    self.assertIn(b'/login', req)
    self.assertEqual(response.status_code, 200)


  # Test artwork EDIT page not logged in

  # Test artwork EDIT page logged in


  # Test artwork DELETE page not logged in

  # Test artwork DELETE page logged in