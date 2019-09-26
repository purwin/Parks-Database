import unittest
from flask import request
from datetime import date, datetime

from app import db
from app.parks_db import Exhibition
from base import BaseTests


def format_date(date_text):
    if not date_text:
        return None

    for style in ('%Y-%m-%d', '%m.%d.%Y', '%m.%d.%y', '%m/%d/%Y', '%m/%d/%y'):
        try:
            # Determine style of date string
            date = datetime.strptime(str(date_text), style)
            # Return date object
            return date

        except ValueError:
            pass
    raise ValueError('Can\'t determine date format of {}!'.format(date_text))



class TestRoutesExhibition(BaseTests):

  default_exhibition = dict(
      name='Swanky Exhibition',
      start_date=format_date('2019-01-01'),
      end_date=format_date('2019-06-01'),
      opening=format_date('2019-01-01'),
      comments='',
      install_start=format_date('2018-12-28'),
      install_end=format_date('2019-01-01'),
      prm='',
      approval='',
      walkthrough='',
      cb_presentation='',
      license_mailed='',
      license_signed='',
      license_borough='',
      bond='',
      coi='',
      coi_renewal='',
      signage_submit='',
      signage_received='',
      press_draft='',
      press_approved='',
      web_text='',
      work_images='',
      deinstall_date=format_date('2019-06-05'),
      deinstall_check='',
      bond_return='',
      press_clippings=''
  )


  @staticmethod
  def create_exhibition(**kwargs):
    """
    Static method to add exhibition class object to database
    Takes the following string args: name, start_date, end_date, opening, comments, install_start, install_end, prm, approval, walkthrough, cb_presentation, license_mailed, license_signed, license_borough, bond, coi, coi_renewal, signage_submit, signage_received, press_draft, press_approved, web_text, work_images, deinstall_date, deinstall_check, bond_return, press_clippings
    Adds class to exhibition database, commits session, and flushes to get id val
    Returns the created class instance
    """
    exhibition = Exhibition(**kwargs)
    db.session.add(exhibition)
    db.session.commit()
    db.session.flush()

    return exhibition


  # Test exhibitions page logged in
  def test_valid_exhibitions_logged_in(self):
    with self.app as c:
      with c.session_transaction() as sess:
        sess['url'] = '/'

      self.login()
      response = self.app.get('/exhibitions', follow_redirects=True)
      req = request.url

    self.assertIn(b'/exhibitions', req)
    self.assertEqual(response.status_code, 200)


  # Test exhibitions page not logged in
  def test_invalid_exhibitions_not_logged_in(self):
    with self.app:
      response = self.app.get('/exhibitions', follow_redirects=True)
      req = request.url

    self.assertIn(b'/login', req)
    self.assertEqual(response.status_code, 200)


  # Test exhibition page logged in
  def test_valid_exhibition_logged_in(self):
    exhibition = self.default_exhibition
    # Add exhibition to database
    self.create_exhibition(**exhibition)

    with self.app as c:
      with c.session_transaction() as sess:
        sess['url'] = '/'

      self.login()
      response = self.app.get('/exhibitions/1', follow_redirects=True)
      req = request.url

    self.assertIn(b'/exhibitions/1', req)
    self.assertEqual(response.status_code, 200)


  # Test exhibition page not logged in
  def test_invalid_exhibition_not_logged_in(self):
    exhibition = self.default_exhibition
    # Add exhibition to database
    self.create_exhibition(**exhibition)

    with self.app:
      response = self.app.get('/orgs/1', follow_redirects=True)
      req = request.url

    self.assertIn(b'/login', req)
    self.assertEqual(response.status_code, 200)

  
  # Test exhibition page with no exhibitions
  def test_invalid_exhibition_no_exhibitions(self):
    with self.app as c:
      with c.session_transaction() as sess:
        sess['url'] = '/'

      self.login()
      response = self.app.get('/exhibitions/1', follow_redirects=True)
      req = request.url

    self.assertIn(b'/exhibitions/1', req)
    self.assertEqual(response.status_code, 404)


  # Test exhibition CREATE page not logged in

  # Test exhibition CREATE page logged in


  # Test exhibition EDIT page not logged in

  # Test exhibition EDIT page logged in


  # Test exhibition DELETE page not logged in

  # Test exhibition DELETE page logged in