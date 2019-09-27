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

  # Test artist page logged in


  # Test artist CREATE page not logged in

  # Test artist CREATE page logged in


  # Test artist EDIT page not logged in

  # Test artist EDIT page logged in


  # Test artist DELETE page not logged in

  # Test artist DELETE page logged in