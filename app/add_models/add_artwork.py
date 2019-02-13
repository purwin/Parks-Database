from app import db
from app.parks_db import Artwork, Artist


# List of acceptable keys for Artwork objects
artwork_params = [
  'id',
  'name',
  'artists',
  'exh_art_park',
  'parks',
  'exhibitions'
]


def add_artwork(match=False, **params):
  """
  Add object argument to Artwork database 
  Returns an object with two attributes: success boolean and the added object
  """

  print "ARTWORK!"
  artwork = False
  # Check for existing ID
  if params.get('id'):
    artwork = Artwork.query.filter_by(id=id).first()
  # Or search for existing items if match option is set
  elif match == True:
    artwork = Artwork.query.filter_by(name=params['name']).first()

  action = 'Found {} in the database.\
            Updated artwork with new data.'.format(params.get('name'))

  if not artwork:
    artwork = Artwork()
    action = 'Added new artwork: {}.'.format(params.get('name'))

  # Loop through passed key/value attributes, add to class object
  try:
    for key, value in params.iteritems():
      if key not in ['exh_art_park', 'artists', 'exhibitions', 'parks']:
        setattr(artwork, key, value)

    # FUTURE: Update to first_name, last_name
    # Loop through artwork.artists separately
    if 'artists' in params:
      print "{} has artists!".format(params.get('name'))
      artists = params.get('artists', None)
      # FUTURE: Search for 
      # If artwork.artists is string, convert to object with split first/last names
      if isinstance(artists, str):
        artists = [{
                'pName': artists.split(' ', 1)[0],
                'fName': artists.split(' ', 1)[1]
        }]
      # Loop through list values if they exist, add to artwork
      for artist in artists or []:
        person = False
        # FUTURE: Call artist function
        person = Artist.query.filter_by(pName=artist['pName'])\
                             .filter_by(fName=artist['fName']).first()
        if not person:
          person = Artist(pName=artist['pName'], fName=artist['fName'])
          db.session.add(person)
        if person not in artwork.artists:
          artwork.artists.append(person)

    # FUTURE: Add exh_art_park relationships
    db.session.add(artwork)
    db.session.commit()
    print "Success: {}".format(action)
    return "Success: {}".format(action)
  except Exception as e:
    print "Error: {}: {}".format(params.get('name'), e)
    return "Error: {}: {}".format(params.get('name'), e)