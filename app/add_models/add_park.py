# -*- coding: utf-8 -*-

from app import db
from app.parks_db import Park
import add_artwork
import add_exhibition
import add_exh_art_park


# List of acceptable keys for Park objects
park_params = [
  'id',
  'name',
  'park_id',
  'borough',
  'address',
  'cb',
  'exh_art_park',
  'exhibitions',
  'artworks'
]


def add_park(match=True, **params):
  """
  Add dict argument to Park database table

  Returns a dict with four attributes:
  - "success": boolean value
  - "data": added dict item
  - "result": string detailing database results
  - "warning": string detailing any unforseen issues
  """

  # If required name parameter not included, return error
  if not params.get('name'):
    return {
      "success": False,
      "result": "Couldn't determine object name.",
      "warning": "",
      "data": params
    }
  else:
    name = params.get('name')

  park = False
  # If ID included, search for existing park
  if params.get('id'):
    park = Park.query.filter_by(id=id).first()

  # Or search for existing items if match option is set
  elif match == True:
    park = Park.query.filter_by(name=name).first()

  result = 'Found {} in the database. Updated park with new data.'\
           .format(name)

  # Create new class object if nothing found

  if not park:
    park = Park()
    result = 'Added new park: {}.'.format(name)

  # Define warnings string to return
  warnings = u''

  # Loop through passed key/value attributes, add to class object
  try:
    for key, value in params.iteritems():
      # Check for bad keys, skip and add to warning list
      if key not in park_params:
        warnings += 'Unexpected {} attribute found. Skipping "{}" addition.\n'\
                    .format(key, value)
      # Add non-list key items to exhibition object
      elif key not in ['exh_art_park', 'exhibitions', 'artworks']:
        setattr(park, key, value)

    db.session.add(park)

    # Add exh_art_park relationships
    if 'exhibitions' and 'artworks' in params:
      exhibitions = params.get('exhibitions', None)

      # If park.exhibitions is string, convert to list
      # while filtering out empty values
      exhibitions = filter(None, [exhibitions]) if\
          (isinstance(exhibitions, str) or isinstance(exhibitions, unicode))\
          else filter(None, exhibitions)

      artworks = params.get('artworks', None)

      # If park.artworks is string, convert to list
      # while filtering out empty values
      artworks = filter(None, [artworks]) if\
          (isinstance(artworks, str) or isinstance(artworks, unicode))\
          else filter(None, artworks)

      # If empty value found or list lengths are unequal, throw warning
      if (not exhibitions or not artworks) or (len(exhibitions) != len(artworks)):
        warnings += u'There’s an uneven number of artworks and exhibitions in '\
                     '{}. Skipping addition.\n'.format(name)

      # Otherwise, add artworks and parks
      else:
        # Flush session to get and use exhibition ID
        db.session.flush()

        # FUTURE: have this code placed in exh_art_park file
        # park_list = []

        # for artwork in artworks:
          # park_list.append(park.name)

        for exhibition, artwork in zip(exhibitions, artworks):
          artwork_dict = add_artwork.add_artwork(name=artwork)
          artwork_id = artwork_dict['data']['id']

          exhibition_dict = add_exhibition.add_exhibition(name=exhibition)
          exhibition_id = exhibition_dict['data']['id']

          exh_art_park = add_exh_art_park.add_exh_art_park(
              exhibition_id=exhibition_id,
              artwork_id=artwork_id,
              park_id=park.id
          )

          if exh_art_park['success'] == True:
            result += u'\nAdded {} @ {} to the {} exhibition'\
                      .format(exhibition, artwork, park.name)
          else:
            warnings += u'{}\n'.format(exh_art_park['result'])

    db.session.commit()
    db.session.flush()

    return {
      "success": True,
      "result": result,
      "warning": warnings,
      "data": park.serialize
    }

  except Exception as e:
    db.session.rollback()

    print u'Error: {}: {}'.format(name, e)

    return {
      "success": False,
      "result": u'{}: {}'.format(name, e),
      "warning": warnings,
      "data": params
    }