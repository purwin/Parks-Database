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


def add_artist(match=False, **params):
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
      "data": params
    }
  else:
    name = params.get('name')


  print "IMPORT ARTIST!"
  artist = False
  name = "{} {}".format(params.get('fName'), params.get('pName'))\
    if params.get('fName') else params.get('pName')

  # Check for existing ID
  if params.get('id'):
    artist = Artist.query.filter_by(id=id).first()
  # Or search for existing items if match option is set
  elif match == True:
    if params.get('pName') and params.get('fName'):
      artist = Artist.query.filter_by(pName=params['pName'])\
                           .filter_by(fName=params['fName']).first()
    elif params.get('name'):
      artist = Artist.query.filter_by(name=params.get('name')).first()

  result = 'Found {} in the database.\
            Updated artist with new data.'.format(name)

  if not artist:
    artist = Artist()
    result = 'Added new artist: {}.'.format(name)

  # Define warnings string to return
  warnings = ""

  # Loop through passed key/value attributes, add to class object
  try:
    for key, value in params.iteritems():
      if key not in['artworks']:
        setattr(artist, key, value)

    db.session.add(artist)


    # Loop through artist.artworks separately
    # if 'artworks' in params:
    #   print "There's artworks in this!"
    #   artworks = params.get('artworks', None)
    #   # If artist.artworks is string, convert to list
    #   artworks = [artworks] if isinstance(artworks, str) else artworks
    #   # Loop through list values if they exist, add to artwork
    #   for artwork in artworks or []:
    #     art = add_artwork.add_artwork(name=artwork)

    #     if art['success'] == True:
    #       pass
    #     # art = False
    #     # FUTURE: Call artwork function
    #     # art = Artwork.query.filter_by(name=artwork).first()
    #     # if not art:
    #       # art = Artwork(name=artwork)
    #       # db.session.add(art)
    #     if art not in artist.artworks:
    #       artist.artworks.append(art)

    db.session.commit()
    db.session.flush()

    # print "Park: {}: {}".format(name, result)

    return {
      "success": True,
      "result": result,
      "warning": warnings,
      "data": park.serialize
    }

  except Exception as e:
    db.session.rollback()
    print "ERROR! {}".format(e)
    return {
      "success": False,
      "result": "{}: {}".format(name, e),
      "warning": warnings,
      "data": params
    }


def get_artist_name(**params):
  if 'name' not in params:
    return False

  else:
    pName = ('pName' in params and params['pName']) or params.get('name').split(' ', 1)[0]
    fName = ('fName' in params and (params['fName'] and params['pName'])) or params.get('name').split(' ', 1)[1]

  # if params.get('pName'):
  #   pName = params.get('pName')
  #   if params.get('fName'):
  #     fName = params.get('pName')
  #   else:
  #     fName = ''

  return {
     'name': params.get('name'),
    'fName': fName,
    'pName': pName
  }