import unittest

from base import BaseTests

from app import db
from app.parks_db import Artwork



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


  # Test CREATE artwork valid
  def test_valid_artwork_create(self):
    self.create_artwork(
        name=self.default_artwork['name']
    )

    artwork_object = Artwork.query.filter_by(
        name=self.default_artwork['name']
    ).first()
    self.assertEqual(artwork_object.id, 1)
    self.assertEqual(artwork_object.name, self.default_artwork['name'])


  # Test CREATE artwork with no name value added
  def test_invalid_artwork_create_empty(self):
    self.create_artwork(name=False)

    self.assertRaises(AttributeError)


  # Test UPDATING artwork
  def test_valid_artwork_update(self):
    artwork = self.create_artwork(
        name=self.default_artwork['name']
    )

    artwork.name = 'Fancier Artwork'
    db.session.add(artwork)
    db.session.commit()

    artwork_object = Artwork.query.filter_by(name='Fancier Artwork').first()
    self.assertEqual(artwork_object.id, 1)
    self.assertEqual(artwork_object.name, 'Fancier Artwork')


  # Test DELETING artwork
  def test_valid_artwork_delete(self):
    artwork = self.create_artwork(
        name=self.default_artwork['name']
    )

    artwork_object = Artwork.query.filter_by(
        name=self.default_artwork['name']
    ).first()
    self.assertEqual(artwork_object.name, self.default_artwork['name'])

    db.session.delete(artwork)
    db.session.commit()

    artwork_object = Artwork.query.filter_by(
        name=self.default_artwork['name']
    ).first()
    self.assertIsNone(artwork_object)


  # Test Artwork.serialize
  def test_valid_artwork_serialize(self):
    self.create_artwork(
        name=self.default_artwork['name']
    )

    artwork_object = Artwork.query.filter_by(
        name=self.default_artwork['name']
    ).first()
    self.assertEqual(
        artwork_object.serialize,
        {
          'id': 1,
          'name': self.default_artwork['name']
        }
    )


  # FUTURE: Add checking for artwork.artists


if __name__ == '__main__':
  unittest.main()