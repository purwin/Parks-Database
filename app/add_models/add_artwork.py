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
      "result": "Couldn't determine object name.",
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

  result = 'Found {} in the database. Updated artwork with new data.'\
           .format(name)

  if not artwork:
    artwork = Artwork()
    result = 'Added new artwork: {}.'.format(name)

  # Define warnings string to return
  warnings = ""

  # Loop through passed key/value attributes, add to class object
  try:
    for key, value in params.iteritems():
      # Check for bad keys, skip and add to warning list
      if key not in artwork_params:
        warnings += 'Unexpected {} attribute found. Skipping "{}" addition.\n'\
                    .format(key, value)
      # Add non-list key items to exhibition object
      elif key not in ['exh_art_park', 'artists', 'exhibitions', 'parks']:
        setattr(artwork, key, value)

    db.session.add(artwork)

    # Loop through artwork.artists separately
    if 'artists' in params:
      artists = params.get('artists', None)
      # If artwork.artists is string, convert to list
      artists = [artists] if isinstance(artists, str) else artists

      # Loop through list values if they exist, add to artwork
      for artist in artists or []:
        person = add_artist.add_artist(name=artist)

        if person['success'] == True:
          if person['artist'] not in artwork.artists:
            print 'Adding {} artist to {}'.format(person['data']['name'], artwork.name)
            artwork.artists.append(person['artist'])
        else:
          warnings += person['result']

    # # Add exh_art_park relationships
    if 'exhibitions' and 'parks' in params:
    #   # Flush session to get and use artwork ID
      db.session.flush()

      exhibitions = filter(None, params.get('exhibitions', None))
    #   # If artwork.exhibitions is string, convert to list
      exhibitions = [exhibitions] if isinstance(exhibitions, str)\
                                  else exhibitions

      parks = filter(None, params.get('parks', None))
    #   # If artwork.parks is string, convert to list
      parks = [parks] if isinstance(parks, str) else parks

      if len(exhibitions) != len(parks):
        warnings += 'There’s an uneven number of exhibitions and parks in '\
                    '{}. Skipping addition.\n'.format(name)
      else:
        for exhibition, park in zip(exhibitions, parks):
          park_dict = add_park.add_park(name=park)
          park_id = park_dict['data']['id']

          exhibition_dict = add_exhibition.add_exhibition(name=exhibition)
          exhibition_id = exhibition_dict['data']['id']

          exh_art_park = add_exh_art_park.add_exh_art_park(
              exhibition_id=exhibition_id,
                    park_id=park_id,
                 artwork_id=artwork.id)

          if exh_art_park['success'] == True:
            result += "\nAdded {} @ {} to the {} exhibition"\
                      .format(exhibition, park, artwork.name)
          else:
            warnings += "\n{}".format(exh_art_park['result'])

    db.session.commit()
    db.session.flush()

    print "Add_artwork: {}".format(result)

    return {
      "success": True,
      "result": result,
      "warning": warnings,
      "data": artwork.serialize,
      "artwork": artwork
    }

  except Exception as e:
    db.session.rollback()
    return {
      "success": False,
      "result": "{}: {}".format(name, e),
      "warning": warnings,
      "data": params
    }