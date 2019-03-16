import unittest
from sqlalchemy.exc import IntegrityError
# from psycopg2 import IntegrityError

from base import BaseTests

from app import db
from app.parks_db import Org, Exhibition



class TestModelsOrg(BaseTests):

  default_org = dict(
      name='Fancy Org',
      phone='1234567890',
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


  # Test CREATE Org valid
  def test_valid_org_create(self):
    self.create_org(
        name=self.default_org['name'],
        phone=self.default_org['phone'],
        website=self.default_org['website']
    )

    org_object = Org.query.filter_by(name=self.default_org['name']).first()

    self.assertEqual(org_object.id, 1)
    self.assertEqual(org_object.name, self.default_org['name'])
    self.assertEqual(org_object.phone, self.default_org['phone'])
    self.assertEqual(org_object.website, self.default_org['website'])


  # Test CREATE Org empty fields valid
  def test_valid_org_create_empty(self):
    self.create_org(name=self.default_org['name'])

    org_object = Org.query.filter_by(name=self.default_org['name']).first()
    org_all = Org.query.filter_by(name=self.default_org['name']).all()

    print len(org_all)

    self.assertEqual(org_object.id, 1)
    self.assertEqual(org_object.name, self.default_org['name'])
    self.assertEqual(org_object.phone, '')
    self.assertEqual(org_object.website, '')


  # Test CREATE Org with no name value added
  def test_invalid_org_create_empty(self):
    self.create_org(name=False)

    self.assertRaises(AttributeError)


  # Test UPDATING Org
  def test_valid_org_update(self):
    org = self.create_org(
        name=self.default_org['name'],
        phone=self.default_org['phone'],
        website=self.default_org['website']
    )

    org.name = 'RoboCop Philanthropy'
    org.phone = '1234560987'
    org.website = 'www.partycanada.com'
    db.session.add(org)
    db.session.commit()

    org_object = org.query.filter_by(name='RoboCop Philanthropy').first()
    self.assertEqual(org_object.id, 1)
    self.assertEqual(org_object.name, 'RoboCop Philanthropy')
    self.assertEqual(org_object.phone, '1234560987')
    self.assertEqual(org_object.website, 'www.partycanada.com')


  # Test ADDING Exhibition to Org
  def test_valid_org_add_exhibition(self):
    org = self.create_org(
        name=self.default_org['name'],
        phone=self.default_org['phone'],
        website=self.default_org['website']
    )

    exhibition = Exhibition(name='Hip Exhibition')
    db.session.add(exhibition)
    db.session.commit()

    org.exhibitions.append(exhibition)
    db.session.add(org)
    db.session.commit()

    org_object = org.query.filter_by(name=self.default_org['name']).first()

    self.assertEqual(org_object.id, 1)
    self.assertEqual(org_object.name, self.default_org['name'])
    self.assertEqual(org_object.phone, self.default_org['phone'])
    self.assertEqual(org_object.website, self.default_org['website'])
    self.assertIn(exhibition, org.exhibitions)


  # Test ADDING Exhibition to Org twice
  def test_invalid_org_add_exhibition_twice(self):
    org = self.create_org(
        name=self.default_org['name'],
        phone=self.default_org['phone'],
        website=self.default_org['website']
    )

    exhibition = Exhibition(name='Hip Exhibition')
    db.session.add(exhibition)
    db.session.commit()

    org.exhibitions.append(exhibition)
    db.session.add(org)
    db.session.commit()

    with self.assertRaises(Exception) as cm:
      org.exhibitions.append(exhibition)
      db.session.add(org)

    self.assertEqual(IntegrityError, type(cm.exception))


if __name__ == '__main__':
  unittest.main()
