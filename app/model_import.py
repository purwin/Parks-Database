from app import app, db
from parks_db import Exh_art_park, Exhibition, Park, Artwork, Artist, Org

import pandas as pd




# def import_park(**data):
#   pass
#   if not data.id:
#     park = Park()
#   else:
#     park = Park.query.filter_by(id = data.id).one()

#   park.name = data.name
#   park.park_id = data.park_id
#   park.borough = data.borough
#   park.address = data.address
#   park.cb = data.cb
#   # Add park to database
#   db.session.add(park)
#   db.session.commit()

def import_park(**params):
  print "PARK!"
  for key, value in params.items():
    print "{} equals {}".format(key, value)


def import_artist(match=False, **params):
  print "IMPORT ARTIST!"
  artist = False
  name = "{} {}".format(params.get('fName'), params.get('pName'))\
    if params.get('fName') else params.get('pName')

  # Check for existing ID
  if params.get('id'):
    artist = Artist.query.filter_by(id = id).first()
  # Or search for existing items if match option is set
  elif match == True:
    artist = Artist.query.filter_by(pName=params['pName'])\
                         .filter_by(fName=params['fName']).first()

  action = 'Found {} in the database.\
            Updated artist with new data.'.format(name)

  if not artist:
    artist = Artist()
    action = 'Added new artist {} to the databse.'.format(name)

  # Loop through passed key/value attributes, add to class object
  try:
    for key, value in params.iteritems():
      if key != 'artworks':
        setattr(artist, key, value)

    # Loop through artist.artworks separately
    if 'artworks' in params:
      print "There's artworks in this!"
      for art in params.get('artworks', None):
        # FUTURE: Call artwork function
        artwork = Artwork.query.filter_by(name = art).first()
        if not artwork:
          artwork = Artwork(name=art)
          db.session.add(artwork)
        if artwork not in artist.artworks:
          artist.artworks.append(artwork)

    db.session.add(artist)
    db.session.commit()
    print "Success: {}".format(action)
    return "Success: {}".format(action)
  except Exception as e:
    print "Error: {}: {}".format(name, e)
    return "Error: {}: {}".format(name, e)


def import_artwork(**params):
  print "ARTWORK!"
  # Check for existing ID
  id = params.get('id')
  print id
  name = "{} {}".format(params.get('fName'), params.get('pName')) if params.get('fName') else params.get('pName')
  print name
  for key, value in params.items():
    print "{} equals {}".format(key, value)


def import_exhibition(**params):
  print "EXHIBITION!"
  for key, value in params.items():
    print "{} equals {}".format(key, value)


def import_org(**params):
  print "ORG!"
  for key, value in params.items():
    print "{} equals {}".format(key, value)


def object_table(arg):
  set_obj = {
    'exhibition': import_exhibition,
    'artwork': import_artwork,
    'park': import_park,
    'artist': import_artist,
    'org': import_org
  }
  return set_obj[arg.lower()]


def import_csv(csv_data, obj, cols, vals, match=False):
  # Remove empty rows
  csv_data = csv_data.replace('', pd.np.nan).dropna(how='all')
  # Replace nan values with empty string
  csv_data = csv_data.replace(pd.np.nan, "")
  # Get Object type, store function value
  model_object = object_table(obj)
  # Set result log
  results = []

  # Loop through file rows
  for index, row in csv_data.iterrows():
    kwargs = {}
    for col, val in zip(cols, vals):
      # Store val item as key, value of row item as value
      kwargs[val] = row[col].strip()
    # Call relevant function with key/value items
    print kwargs
    result = model_object(match=match, **kwargs)
    results.append(result)

  return results



def main(csv_file):
  temp_obj = 'park'
  cols = ['Location', 'Borough']
  vals = ['park_name', 'borough']

  import_csv(csv_file = csv_file, obj = temp_obj, cols = cols, vals = vals)

  # file = pd.read_csv(csv_file)
  # file.drop(file.columns[file.columns.str.contains('unnamed', case=False)],
  #   axis=1, inplace=True)
  # file_headers = file.columns.values
  # print file_headers

  # row_1 = file[1:5]
  # for index, row in row_1.iterrows():
  #   d = {}
  #   for col in file_headers:
  #     d[col] = row[col]
  #   print d

if __name__ == '__main__':
  main('/Users/michaelpurwin/Documents/workings/parks database/data/CURRENT_Public-Art-Chronology_1.30.2017.csv')