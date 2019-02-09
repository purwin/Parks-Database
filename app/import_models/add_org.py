from app import db
from parks_db import Exh_art_park, Exhibition, Park, Artwork, Artist, Org


def add_org(match=False, **params):
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
    action = 'Added new org: {}.'.format(params.get('name'))

  # Loop through passed key/value attributes, add to class object
  try:
    for key, value in params.iteritems():
      if key not in ['exhibitions']:
        setattr(org, key, value)

    # Add any exhibitions to exhibitions.exhibition
    if 'exhibitions' in params:
      print "There's exhibitions in this!"
      exhibitions = params.get('exhibitions', None)
      exhibitions = [exhibitions] if isinstance(exhibitions, str)
                                  else exhibitions
      for exh in exhibitions or []:
        exhibition = False
        # FUTURE: Call exhibition function
        exhibition = Exhibition.query.filter_by(name=exh).first()
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