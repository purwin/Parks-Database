# -*- coding: utf-8 -*-

from app import db
from app.parks_db import Artist
import add_artwork


# List of acceptable keys for Artist objects
artist_params = [
  'id',
  'pName',
  'fName',
  'name',
  'email',
  'phone',
  'website',
  'artworks'
]


def add_artist(match=True, **params):
  """
  Add dict argument to Artwork database table

  Returns a dict with four attributes:
  - "success": boolean value
  - "data": added dict item
  - "result": string detailing database results
  - "warning": string detailing any unforseen issues
  """

  # Define name, pName, and fName based on recieved params
  name = get_artist_name(**params)

  # If required name parameter not included, return error
  if name == False:
    return {
      "success": False,
      "result": "Couldn't determine object name.",
      "warning": "",
      "data": params
    }

  print "IMPORT ARTIST!"
  artist = False

  # Check for existing ID
  if params.get('id'):
    artist = Artist.query.filter_by(id=id).first()
  # Or search for existing items if match option is set
  elif match == True:
    artist = Artist.query.filter_by(name=name['name']).first()

  result = u'Found {} in the database. '\
            'Updated artist with new data.'.format(name['name'])

  if not artist:
    artist = Artist()
    result = u'Added new artist: {}.'.format(name)

  # Define warnings string to return
  warnings = ""

  # Loop through passed key/value attributes, add to class object
  try:
    for key, value in params.iteritems():
      # Check for bad keys, skip and add to warning list
      if key not in artist_params:
        warnings += u'Unexpected {} attribute found. Skipping "{}" addition.\n'\
                    .format(key, value)
      # Add non-list key items to exhibition object
      # Skip name key item as that's created from artist.serialize
      elif key not in ['artworks', 'name']:
        setattr(artist, key, value)

    db.session.add(artist)

    # Loop through artwork.artists separately
    if 'artworks' in params:
      print "There's artworks in this!"
      artworks = params.get('artworks', None)
      # If artist.artworks is string, convert to list
      artworks = [artworks] if\
          (isinstance(artworks, str) or isinstance(artworks, unicode))\
          else artworks
      # Loop through list values if they exist, add to artwork
      for artwork in artworks or []:
        art = add_artwork.add_artwork(name=artwork)

        if art['success'] == True:
          if art['artwork'] not in artist.artworks:
            print u'{} art data not in artist.artworks'.format(
                art['data']['name'])
            artist.artworks.append(art['artwork'])
        else:
          warnings += art['result']

    db.session.commit()
    db.session.flush()

    print u"Add artist: {}".format(result)

    return {
      "success": True,
      "result": result,
      "warning": warnings,
      "data": artist.serialize,
      "artist": artist
    }

  except Exception as e:
    db.session.rollback()
    print "ERROR! {}".format(e)
    return {
      "success": False,
      "result": u"{}: {}".format(name, e),
      "warning": warnings,
      "data": params
    }


def get_artist_name(**params):
  # Return false if required parameters aren't present
  if 'name' not in params and 'pName' not in params:
    return False

  if 'pName' not in params:
    # Set pName to name if no spaces found
    pName = params.get('name').split(' ', 1)[1]\
        if ' ' in params.get('name', '') else params['name']
    # Define fName if spaces found in name
    fName = params.get('name').split(' ', 1)[0]\
        if ' ' in params.get('name', '') else None
    name = params.get('name', None)
  elif 'name' not in params:
    fName = params.get('fName', None)
    pName = params.get('pName', None)
    name = ''.join([fName, ' ', pName]) if fName else pName

  return {
     'name': params.get('name', name),
    'fName': params.get('fName', fName),
    'pName': params.get('pName', pName)
  }
