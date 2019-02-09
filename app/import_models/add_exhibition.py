from app import db
from parks_db import Exh_art_park, Exhibition, Park, Artwork, Artist, Org


def add_exhibition(match=False, **params):
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
    action = 'Added new exhibition: {}.'.format(params.get('name'))

  # Loop through passed key/value attributes, add to class object
  try:
    for key, value in params.iteritems():
      if key not in ['exh_art_park', 'orgs', 'artworks', 'parks']:
        setattr(exhibition, key, value)

    # FUTURE: Add exh_art_park relationships

    # Add any orgs to exhibitions.org
    if 'orgs' in params:
      print "There's orgs in this!"
      orgs = params.get('orgs', None)
      # If exhibition.orgs is string, convert to list
      orgs = [orgs] if isinstance(orgs, str) else orgs
      for org in orgs or []:
        organization = False
        # FUTURE: Call org function
        organization = Org.query.filter_by(name=org).first()
        # Add new org to database if not found
        if not org:
          organization = Org(name=org)
          db.session.add(org)
        # Add org relationship if not in one-to-many relationship
        if organization not in exhibition.orgs:
          exhibition.orgs.append(organization)

    db.session.add(exhibition)
    db.session.commit()
    print "Success: {}".format(action)
    return "Success: {}".format(action)
  except Exception as e:
    print "Error: {}: {}".format(params.get('name'), e)
    return "Error: {}: {}".format(params.get('name'), e)