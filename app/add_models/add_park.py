from app import db
from parks_db import Park

# List of acceptable keys for Park objects
park_params = [
  'id',
  'name',
  'park_id',
  'borough',
  'address',
  'cb',
  'exh_art_park'
]

def add_park(match=False, **params):
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
    action = 'Added new park: {}.'.format(params.get('name'))

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