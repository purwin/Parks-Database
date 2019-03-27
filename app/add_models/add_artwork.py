# -*- coding: utf-8 -*-

from app import db
from app.parks_db import Artwork
import add_artist
import add_park
import add_exhibition
import add_exh_art_park


# List of acceptable keys for Artwork objects
artwork_params = [
  'id',
  'name',
  'artists',
  'exh_art_park',
  'parks',
  'exhibitions'
]


def add_artwork(match=True, **params):
  """
  Add dict argument to Artwork database table

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
      "result": "Error: Couldn't determine object name.",
      "warning": "",
      "data": params
    }
  else:
    name = params.get('name')

  artwork = False
  # Check for existing ID
  if params.get('id'):
    artwork = Artwork.query.filter_by(id=id).first()
  # Or search for existing items if match option is set
  elif match == True:
    artwork = Artwork.query.filter_by(name=name).first()

  result = u'Found {} in the database. Updated artwork with new data.'\
           .format(name)

  if not artwork:
    artwork = Artwork()
    result = u'Added new artwork: {}.'.format(name)

  # Define warnings string to return
  warnings = u""

  # Loop through passed key/value attributes, add to class object
  try:
    for key, value in params.iteritems():
      # Check for bad keys, skip and add to warning list
      if key not in artwork_params:
        warnings += u'Unexpected {} attribute found. Skipping "{}" addition.\n'\
                    .format(key, value)
      # Add non-list key items to exhibition object
      elif key not in ['exh_art_park', 'artists', 'exhibitions', 'parks']:
        setattr(artwork, key, value)

    db.session.add(artwork)

    # Loop through artwork.artists separately
    if 'artists' in params:
      # Filter empty items out of 'artists' parameter, strip whitespace
      artists = filter(None, params.get('artists', None)).strip()
      # If artwork.artists is string, convert to list
      artists = [artists] if\
          (isinstance(artists, str) or isinstance(artists, unicode))\
          else artists

      # Loop through list values if they exist, add to artwork
      for artist in artists or []:
        person = add_artist.add_artist(name=artist)

        if person['success'] == True:
          if person['artist'] not in artwork.artists:
            artwork.artists.append(person['artist'])
        else:
          warnings += u'{}\n'.format(person['result'])

    # Add exh_art_park relationships
    if 'exhibitions' and 'parks' in params:
      parks = params.get('parks', None)

      # If artwork.parks is string, convert to list
      # while filtering out empty values
      parks = filter(None, [parks]) if\
          (isinstance(parks, str) or isinstance(parks, unicode))\
          else filter(None, parks)

      exhibitions = params.get('exhibitions', None)

      # If artwork.exhibitions is string, convert to list
      # while filtering out empty values
      exhibitions = filter(None, [exhibitions]) if\
          (isinstance(exhibitions, str) or isinstance(exhibitions, unicode))\
          else filter(None, exhibitions)

      # If empty value found or list lengths are unequal, throw warning
      if (not parks or not exhibitions) or (len(parks) != len(exhibitions)):
        warnings += u'There’s an uneven number of exhibitions and parks in '\
                     '{}. Skipping addition.\n'.format(name)

      # Otherwise, add artworks and parks
      else:
        # Flush session to get and use artwork ID
        db.session.flush()

        for exhibition, park in zip(exhibitions, parks):
          park_dict = add_park.add_park(name=park)
          park_id = park_dict['data']['id']

          exhibition_dict = add_exhibition.add_exhibition(name=exhibition)
          exhibition_id = exhibition_dict['data']['id']

          exh_art_park = add_exh_art_park.add_exh_art_park(
              exhibition_id=exhibition_id,
              park_id=park_id,
              artwork_id=artwork.id
          )

          if exh_art_park['success'] == True:
            result += u"\nAdded {} @ {} to the {} exhibition"\
                      .format(exhibition, park, artwork.name)
          else:
            warnings += u"{}\n".format(exh_art_park['result'])

    db.session.commit()
    db.session.flush()

    return {
      "success": True,
      "result": result,
      "warning": warnings,
      "data": artwork.serialize,
      "artwork": artwork
    }

  except Exception as e:
    db.session.rollback()

    print u'Error: {}: {}'.format(name, e)

    return {
      "success": False,
      "result": u'Error: {}: {}'.format(name, e),
      "warning": warnings,
      "data": params
    }