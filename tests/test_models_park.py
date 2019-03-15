import unittest

from base import BaseTests

from app import db
from app.parks_db import Park


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


  # Test CREATE park valid
  def test_valid_park_create(self):
    # print self.default_park
    self.create_park(
      name='NY Park',
      park_id='W450',
      borough='Queens',
      address='30 Broadway',
      cb='04'
  )

    park_object = Park.query.filter_by(name='NY Park').first()
    self.assertEqual(park_object.id, 1)
    self.assertEqual(park_object.name, self.default_park['name'])
    self.assertEqual(park_object.park_id, self.default_park['park_id'])
    self.assertEqual(park_object.borough, self.default_park['borough'])
    self.assertEqual(park_object.address, self.default_park['address'])
    self.assertEqual(park_object.cb, self.default_park['cb'])



if __name__ == '__main__':
  unittest.main()
