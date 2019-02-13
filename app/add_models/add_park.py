from flask import jsonify

from app import db
from app.parks_db import Park


# List of acceptable keys for Park objects
park_params = [
  'id',
  'name',
  'park_id',
  'borough',
  'address',
  'cb',
  'exh_art_park',
  'exhibitions',
  'artworks'
]


def add_park(match=False, **params):
  """
  Add object argument to Park database 
  Returns an object with two attributes: success boolean and the added object
  """

  # print "PARK! {}".format(params)

  # If required name parameter not included, return error
  if not params.get('name'):
    return jsonify({
      "success": False,
      "error": "Couldn't determine object name.",
      "data": params})
  else:
    name = params.get('name')

  # If ID included, search for existing park
  if params.get('id'):
    park = Park.query.filter_by(id=id).first()
    # print "{}: Found ID".format(name)
    action = 'Found {} in the database. Updated park with new '\
         'data.'.format(name)

    # print "PARK: {}".format(park.name)

  # Or search for existing items if match option is set
  elif match == True:
    park = Park.query.filter_by(name=name).first()
    # print "{}: Found park by name".format(name)
    action = 'Found {} in the database. Updated park with new '\
         'data.'.format(name)

  # Create new class object if nothing found
  else:
    park = Park()
    # print "{} doesn't exist in database. Creating new park.".format(name)
    action = 'Added new park: {}.'.format(name)

  # print "PARK: {}".format(park.name)

  # Define warnings array to return
  warnings = []

  # Loop through passed key/value attributes, add to class object
  try:
    for key, value in params.iteritems():
      # Check for bad keys, skip and add to warning list
      if key not in park_params:
        # print "{} key doesn't match park attributes".format(name)
        warnings.append('Unexpected {} attribute found. Skipping "{}" '\
                'addition.'.format(key, value))
      # Add non-list key items to exhibition object
      elif key not in ['exh_art_park', 'exhibitions', 'artworks']:
        # print "Adding {} attribute: {}".format(key, value)
        setattr(park, key, value)

      # FUTURE: Add exh_art_park relationships

    db.session.add(park)
    db.session.commit()
    # print "Success: {}".format(action)
    return {
      "success": True,
      "warning": warnings,
      "result": action,
      "data": park.serialize
    }

  except Exception as e:
    # print "Error: {}: {}".format(name, e)
    return {
      "success": False,
      "result": "{}: {}".format(name, e),
      "warning": warnings,
      "data": params
    }
