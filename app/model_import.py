from app import db
from parks_db import Exh_art_park, Exhibition, Park, Artwork, Artist, Org

import pandas as pd


def import_park(match=False, **params):
  print "PARK!"
  park = False
  # Check for existing ID
  if params.get('id'):
    park = Park.query.filter_by(id=id).first()
  # Or search for existing items if match option is set
  elif match == True:
    park = Park.query.filter_by(name=params['name']).first()

  action = 'Found {} in the database.\
            Updated park with new data.'.format(params.get('name'))

  if not park:
    park = Park()
    action = 'Added new park {} to the databse.'.format(params.get('name'))

  # Loop through passed key/value attributes, add to class object
  try:
    for key, value in params.iteritems():
      if key not in ['exh_art_park', 'exhibitions', 'artworks']:
        setattr(park, key, value)

    # FUTURE: Add exh_art_park relationships
    db.session.add(park)
    db.session.commit()
    print "Success: {}".format(action)
    return "Success: {}".format(action)
  except Exception as e:
    print "Error: {}: {}".format(params.get('name'), e)
    return "Error: {}: {}".format(params.get('name'), e)


def import_artist(match=False, **params):
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
    action = 'Added new artist {} to the databse.'.format(name)

  # Loop through passed key/value attributes, add to class object
  try:
    for key, value in params.iteritems():
      if key not in['artworks']:
        setattr(artist, key, value)

    # Loop through artist.artworks separately
    if 'artworks' in params:
      print "There's artworks in this!"
      for art in params.get('artworks', None):
        # FUTURE: Call artwork function
        artwork = Artwork.query.filter_by(name=art).first()
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


def import_artwork(match=False, **params):
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
    action = 'Added new artwork {} to the databse.'.format(params.get('name'))

  # Loop through passed key/value attributes, add to class object
  try:
    for key, value in params.iteritems():
      if key not in ['exh_art_park', 'exhibitions', 'parks']:
        setattr(artwork, key, value)

    # FUTURE: Add exh_art_park relationships
    db.session.add(artwork)
    db.session.commit()
    print "Success: {}".format(action)
    return "Success: {}".format(action)
  except Exception as e:
    print "Error: {}: {}".format(params.get('name'), e)
    return "Error: {}: {}".format(params.get('name'), e)


def import_exhibition(match=False, **params):
  print "EXHIBITION!"
  exhibition = False
  # Check for existing ID
  if params.get('id'):
    exhibition = Exhibition.query.filter_by(id=id).first()
  # Or search for existing items if match option is set
  elif match == True:
    exhibition = Exhibition.query.filter_by(name=params['name']).first()

  action = 'Found {} in the database.\
            Updated exhibition with new data.'.format(params.get('name'))

  if not exhibition:
    exhibition = Exhibition()
    action = 'Added new exhibition {} to the databse.'.format(params.get('name'))

  # Loop through passed key/value attributes, add to class object
  try:
    for key, value in params.iteritems():
      if key not in ['exh_art_park', 'orgs', 'artworks', 'parks']:
        setattr(exhibition, key, value)

    # FUTURE: Add exh_art_park relationships

    # Add any orgs to exhibitions.org
    if 'orgs' in params:
      print "There's orgs in this!"
      for organization in params.get('orgs', None):
        # FUTURE: Call org function
        org = Artwork.query.filter_by(name=organization).first()
        # Add new org to database if not found
        if not org:
          org = Org(name=organization)
          db.session.add(org)
        # Add org relationship if not in one-to-many relationship
        if org not in exhibition.orgs:
          exhibition.orgs.append(org)

    db.session.add(exhibition)
    db.session.commit()
    print "Success: {}".format(action)
    return "Success: {}".format(action)
  except Exception as e:
    print "Error: {}: {}".format(params.get('name'), e)
    return "Error: {}: {}".format(params.get('name'), e)


def import_org(match=False,**params):
  print "ORG!"
  org = False
  # Check for existing ID
  if params.get('id'):
    org = Org.query.filter_by(id=id).first()
  # Or search for existing items if match option is set
  elif match == True:
    org = Org.query.filter_by(name=params['name']).first()

  action = 'Found {} in the database.\
            Updated org with new data.'.format(params.get('name'))

  if not org:
    org = Org()
    action = 'Added new org {} to the databse.'.format(params.get('name'))

  # Loop through passed key/value attributes, add to class object
  try:
    for key, value in params.iteritems():
      if key not in ['exhibitions']:
        setattr(org, key, value)

    # Add any exhibitions to exhibitions.exhibition
    if 'exhibitions' in params:
      print "There's exhibitions in this!"
      for exh in params.get('exhibitions', None):
        # FUTURE: Call exhibition function
        exhibition = Artwork.query.filter_by(name=exh).first()
        # Add new org to database if not found
        if not exhibition:
          exhibition = Exhibition(name=exh)
          db.session.add(exhibition)
        # Add exhibition relationship if not in one-to-many relationship
        if exhibition not in org.exhibitions:
          org.exhibitions.append(exhibition)

    db.session.add(org)
    db.session.commit()
    print "Success: {}".format(action)
    return "Success: {}".format(action)
  except Exception as e:
    print "Error: {}: {}".format(params.get('name'), e)
    return "Error: {}: {}".format(params.get('name'), e)


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