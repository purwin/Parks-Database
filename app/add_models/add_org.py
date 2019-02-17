# -*- coding: utf-8 -*-

from app import db
from app.parks_db import Org, Exhibition


# List of acceptable keys for Org objects
org_params = [
  'id',
  'name',
  'website',
  'phone',
  'exhibitions'
]


def add_org(match=False, **params):
  """
  Add dict argument to Org database table

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
      "error": "Couldn't determine object name.",
      "data": params
    }

  name = params.get('name')

  # Define org as false to check if object exists in database below
  org = False

  # Check for existing ID
  if params.get('id'):
    org = Org.query.filter_by(id=id).first()

  # Or search for existing items if match option is set
  elif match == True:
    org = Org.query.filter_by(name=name).first()

  result = 'Found {} in the database. Updated org with new data.'.format(name)

  # Create new class object if nothing found
  if not org:
    org = Org()
    result = 'Added new org: {}.'.format(name)

  # Define warnings string to return
  warnings = ""

  # Loop through passed key/value attributes, add to class object
  try:
    for key, value in params.iteritems():
      # Check for bad keys, add to warning list
      if key not in org_params:
        warnings += 'Unexpected {} attribute found. Skipping "{}" addition.'\
            .format(key, value)

      # Add non-list key items to exhibition object
      elif key not in ['exhibitions']:
        setattr(org, key, value)

    # # Add any exhibitions to exhibitions.exhibition
    # if 'exhibitions' in params:
    #   print "There's exhibitions in this!"
    #   exhibitions = params.get('exhibitions', None)
    #   exhibitions = [exhibitions] if isinstance(exhibitions, str) \
    #     else exhibitions

    #   # Loop through items in exhibitions list,
    #   # add each to object relationship
    #   for exh in exhibitions or []:
    #     exhibition = False
    #     # FUTURE: Call exhibition function
    #     exhibition = Exhibition.query.filter_by(name=exh).first()
    #     # Add new org to database if not found
    #     if not exhibition:
    #       exhibition = Exhibition(name=exh)
    #       db.session.add(exhibition)
    #     # Add exhibition relationship
    #     # if not in one-to-many relationship
    #     if exhibition not in org.exhibitions:
    #       org.exhibitions.append(exhibition)

    db.session.add(org)
    db.session.commit()
    return {
      "success": True,
      "warning": warnings,
      "response": result,
      "data": org.serialize,
      "org": org
    }

  except Exception as e:
    print "Error: {}: {}".format(name, e)
    return {
      "success": False,
      "error": "{}: {}".format(name, e),
      "warning": warnings,
      "data": params
    }
