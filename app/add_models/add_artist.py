from app import db
from app.parks_db import Artist, Artwork


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

  print "IMPORT ARTIST!"
  artist = False
  name = "{} {}".format(params.get('fName'), params.get('pName'))\
    if params.get('fName') else params.get('pName')

  # Check for existing ID
  if params.get('id'):
    artist = Artist.query.filter_by(id=id).first()
  # Or search for existing items if match option is set
  elif match == True:
    artist = Artist.query.filter_by(pName=params['pName'])\
                         .filter_by(fName=params['fName']).first()

  action = 'Found {} in the database.\
            Updated artist with new data.'.format(name)

  if not artist:
    artist = Artist()
    action = 'Added new artist: {}.'.format(name)

  # Loop through passed key/value attributes, add to class object
  try:
    for key, value in params.iteritems():
      if key not in['artworks']:
        setattr(artist, key, value)

    # Loop through artist.artworks separately
    if 'artworks' in params:
      print "There's artworks in this!"
      artworks = params.get('artworks', None)
      # If artist.artworks is string, convert to list
      artworks = [artworks] if isinstance(artworks, str) else artworks
      # Loop through list values if they exist, add to artwork
      for artwork in artworks or []:
        art = False
        # FUTURE: Call artwork function
        art = Artwork.query.filter_by(name=artwork).first()
        if not art:
          art = Artwork(name=artwork)
          db.session.add(art)
        if art not in artist.artworks:
          artist.artworks.append(art)

    db.session.add(artist)
    db.session.commit()
    print "Success: {}".format(action)
    return "Success: {}".format(action)
  except Exception as e:
    print "Error: {}: {}".format(name, e)
    return "Error: {}: {}".format(name, e)