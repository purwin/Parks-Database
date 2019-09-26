import unittest
from flask import request

from app import db
from app.parks_db import Org
from base import BaseTests



class TestRoutesOrg(BaseTests):

  default_org = dict(
    name='Fancy Org',
    phone='123-456-7890',
    website='www.partyusa.com'
  )

  @staticmethod
  def create_org(**kwargs):
    """
    Static method to add org class object to database
    Takes the following string args: name, phone, website
    Adds class to Org database, commits session, and flushes to get id val
    Returns the created class instance
    """
    org = Org(**kwargs)
    db.session.add(org)
    db.session.commit()
    db.session.flush()

    return org


  # Test orgs page not logged in

  # Test orgs page logged in
  def test_valid_orgs_logged_in(self):
    with self.app as c:
      with c.session_transaction() as sess:
        sess['url'] = '/'

      self.login()
      response = self.app.get('/orgs', follow_redirects=True)
      req = request.url

    self.assertIn(b'/orgs', req)
    self.assertEqual(response.status_code, 200)


  # Test org page not logged in

  # Test org page logged in


  # Test org CREATE page not logged in

  # Test org CREATE page logged in


  # Test org EDIT page not logged in

  # Test org EDIT page logged in


  # Test org DELETE page not logged in

  # Test org DELETE page logged in