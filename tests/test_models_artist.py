import unittest

from base import BaseTests

from app import db
from app.parks_db import Artist


class TestModelsArtist(BaseTests):

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


  # Test CREATE artist valid
  def test_valid_artist_create(self):
    self.create_artist(
        pName=self.default_artist['pName'],
        fName=self.default_artist['fName'],
        email=self.default_artist['email'],
        phone=self.default_artist['phone'],
        website=self.default_artist['website']
    )

    artist_object = Artist.query.filter_by(
        pName=self.default_artist['pName']
    ).first()
    self.assertEqual(artist_object.id, 1)
    self.assertEqual(artist_object.pName, self.default_artist['pName'])
    self.assertEqual(artist_object.fName, self.default_artist['fName'])
    self.assertEqual(
        artist_object.name, '{} {}'.format(
            self.default_artist['fName'], self.default_artist['pName']
        )
    )
    self.assertEqual(artist_object.email, self.default_artist['email'])
    self.assertEqual(artist_object.phone, self.default_artist['phone'])
    self.assertEqual(artist_object.website, self.default_artist['website'])


  # Test CREATE artist valid
  def test_valid_artist_create_name(self):
    self.create_artist(pName=self.default_artist['pName'])

    artist_object = Artist.query.filter_by(
        pName=self.default_artist['pName']
    ).first()

    self.assertEqual(artist_object.id, 1)
    self.assertEqual(artist_object.pName, self.default_artist['pName'])
    self.assertIsNone(artist_object.fName)
    self.assertEqual(artist_object.name, self.default_artist['pName'])
    self.assertEqual(artist_object.email, '')
    self.assertEqual(artist_object.phone, '')
    self.assertEqual(artist_object.website, '')


  # Test CREATE artist with no name value added
  def test_invalid_artist_create_empty(self):
    self.create_artist(pName=False)

    self.assertRaises(AttributeError)


  # Test UPDATING artist
  def test_valid_artist_update(self):
    artist = self.create_artist(
        pName=self.default_artist['pName'],
        fName=self.default_artist['fName'],
        email=self.default_artist['email'],
        phone=self.default_artist['phone'],
        website=self.default_artist['website']
    )

    artist.email = 'cool_person2@website.com'
    db.session.add(artist)
    db.session.commit()

    artist_object = Artist.query.filter_by(
        pName=self.default_artist['pName']
    ).first()
    self.assertEqual(artist_object.id, 1)
    self.assertEqual(artist_object.pName, self.default_artist['pName'])
    self.assertEqual(artist_object.fName, self.default_artist['fName'])
    self.assertEqual(
        artist_object.name, '{} {}'.format(
            self.default_artist['fName'],
            self.default_artist['pName']
        )
    )
    self.assertEqual(artist_object.email, 'cool_person2@website.com')
    self.assertEqual(artist_object.phone, self.default_artist['phone'])
    self.assertEqual(artist_object.website, self.default_artist['website'])


  # Test DELETING artist
  def test_valid_artist_delete(self):
    artist = self.create_artist(
        pName=self.default_artist['pName'],
        fName=self.default_artist['fName'],
        email=self.default_artist['email'],
        phone=self.default_artist['phone'],
        website=self.default_artist['website']
    )

    artist_object = Artist.query.filter_by(
        pName=self.default_artist['pName']
    ).first()
    self.assertEqual(artist_object.pName, self.default_artist['pName'])

    db.session.delete(artist)
    db.session.commit()

    artist_object = Artist.query.filter_by(
        pName=self.default_artist['pName']
    ).first()
    self.assertIsNone(artist_object)


  # Test Artist.serialize
  def test_valid_artist_serialize(self):
    self.create_artist(
        pName=self.default_artist['pName'],
        fName=self.default_artist['fName'],
        email=self.default_artist['email'],
        phone=self.default_artist['phone'],
        website=self.default_artist['website']
    )

    artist_object = Artist.query.filter_by(
        pName=self.default_artist['pName']
    ).first()
    self.assertEqual(
        artist_object.serialize,
        {
          'id': 1,
          'pName': self.default_artist['pName'],
          'fName': self.default_artist['fName'],
          'name': '{} {}'.format(
              self.default_artist['fName'],
              self.default_artist['pName']
          ),
          'email': self.default_artist['email'],
          'phone': self.default_artist['phone'],
          'website': self.default_artist['website']
        }
    )


if __name__ == '__main__':
  unittest.main()