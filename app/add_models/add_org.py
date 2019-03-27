# -*- coding: utf-8 -*-

from app import db
from app.parks_db import Org
import add_exhibition


# List of acceptable keys for Org objects
org_params = [
  'id',
  'name',
  'website',
  'phone',
  'exhibitions'
]


def add_org(match=True, **params):
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
      "result": "Error: Couldn't determine object name.",
      "warning": "",
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

  result = u'Found {} in the database. Updated org with new data.'.format(name)

  # Create new class object if nothing found
  if not org:
    org = Org()
    result = u'Added new org: {}.'.format(name)

  # Define warnings string to return
  warnings = u''

  # Loop through passed key/value attributes, add to class object
  try:
    for key, value in params.iteritems():
      # Check for bad keys, add to warning list
      if key not in org_params:
        warnings += u'Unexpected {} attribute found. Skipping "{}" addition.'\
            .format(key, value)

      # Add non-list key items to exhibition object
      elif key not in ['exhibitions']:
        setattr(org, key, value)

    db.session.add(org)

    # Add any exhibitions to org.exhibitions
    if 'exhibitions' in params:
      exhibitions = params.get('exhibitions', None)

      # If org.exhibitions is string, convert to list
      # while filtering out empty values
      exhibitions = filter(None, [exhibitions]) if\
          (isinstance(exhibitions, str) or isinstance(exhibitions, unicode))\
          else filter(None, exhibitions)

      # Loop through items in exhibitions list,
      # add each to object relationship
      for exhibition in exhibitions or []:
        exh = add_exhibition.add_exhibition(name=exhibition)

        if exh['success'] == True:
          if exh['exhibition'] not in org.exhibitions:
            org.exhibitions.append(exh['exhibition'])

    db.session.commit()
    db.session.flush()

    return {
      "success": True,
      "result": result,
      "warning": warnings,
      "data": org.serialize,
      "org": org
    }

  except Exception as e:
    db.session.rollback()

    print u'Error: {}: {}'.format(name, e)

    return {
      "success": False,
      "result": u'Error: {}: {}'.format(name, e),
      "warning": warnings,
      "data": params
    }
