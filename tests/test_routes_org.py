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
  def test_invalid_orgs_not_logged_in(self):
    with self.app:
      response = self.app.get('/orgs', follow_redirects=True)
      req = request.url

    self.assertIn(b'/login', req)
    self.assertEqual(response.status_code, 200)


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
  def test_invalid_org_not_logged_in(self):
    org = self.default_org
    # Add org to database
    self.create_org(**org)

    with self.app:
      response = self.app.get('/orgs/1', follow_redirects=True)
      req = request.url

    self.assertIn(b'/login', req)
    self.assertEqual(response.status_code, 200)


  # Test org page logged in
  def test_valid_org_logged_in(self):
    org = self.default_org
    # Add org to database
    self.create_org(**org)

    with self.app as c:
      with c.session_transaction() as sess:
        sess['url'] = '/'

      self.login()
      response = self.app.get('/orgs/1', follow_redirects=True)
      req = request.url

    self.assertIn(b'/orgs/1', req)
    self.assertEqual(response.status_code, 200)


  # Test org page with no orgs
  def test_invalid_org_no_orgs(self):
    with self.app as c:
      with c.session_transaction() as sess:
        sess['url'] = '/'

      self.login()
      response = self.app.get('/orgs/1', follow_redirects=True)
      req = request.url

    self.assertIn(b'/orgs/1', req)
    self.assertEqual(response.status_code, 404)


  # Test GET org CREATE page
  def test_invalid_org_create_get(self):
    with self.app:
      response = self.app.get('/orgs/create', follow_redirects=True)

    self.assertIn('Method Not Allowed', response.data)
    self.assertEqual(response.status_code, 405)


  # Test org CREATE page logged in
  def test_valid_org_create_post(self):
    org = self.default_org
    with self.app as c:
      with c.session_transaction() as sess:
        sess['url'] = '/'

      self.login()
      response = self.app.post(
          '/orgs/create',
          data=org,
          follow_redirects=True
      )

    self.assertIn('"success": true', response.data)
    self.assertEqual(response.status_code, 200)


  # Test org CREATE page not logged in
  def test_invalid_org_create_post(self):
    org = self.default_org
    with self.app as c:
      response = self.app.post(
          '/orgs/create',
          data=org,
          follow_redirects=True
      )
      req = request.url

    self.assertIn(b'/login', req)
    self.assertEqual(response.status_code, 200)


  # Test POST org EDIT page logged in
  def test_valid_org_edit_post(self):
    org = self.default_org
    new_org = 'Fancier Org'
    # Add org to database
    self.create_org(**org)

    with self.app as c:
      with c.session_transaction() as sess:
        sess['url'] = '/'

      self.login()
      response = self.app.post(
          '/orgs/1/edit',
          data=dict(
              name=new_org,
              phone=org['phone'],
              website=org['website']
          ),
          follow_redirects=True
      )

    self.assertIn('"success": true', response.data)
    self.assertIn(new_org, response.data)
    self.assertEqual(response.status_code, 200)


  # Test POST org EDIT page not logged in


  # Test org DELETE page not logged in

  # Test org DELETE page logged in