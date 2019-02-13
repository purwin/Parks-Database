from datetime import datetime

from app import db
from parks_db import Exhibition, Org
# from add_models import add_org


# List of acceptable keys for Exhibition objects
exhibition_params = [
  'name',
  'start_date',
  'end_date',
  'opening',
  'comments',
  'install_start',
  'install_end',
  'prm',
  'approval',
  'walkthrough',
  'cb_presentation',
  'license_mailed',
  'license_signed',
  'license_borough',
  'bond',
  'coi',
  'coi_renewal',
  'signage_submit',
  'signage_received',
  'press_draft',
  'press_approved',
  'web_text',
  'work_images',
  'deinstall_date',
  'deinstall_check',
  'bond_return',
  'press_clippings',
  'parks',
  'artworks',
  'orgs',
  'exh_art_park'
]


def add_exhibition(match=False, **params):
  """
  Add object argument to Exhibition database 
  Returns an object with two attributes: success boolean and the added object
  """

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
      # Check for bad keys in object
      if key not in exhibition_params:
        return "Error: {}: Unexpected {} attribute found.".format(params.get('name'), key)
      # Add non-arry key items to exhibition object
      if key not in ['exh_art_park', 'orgs', 'artworks', 'parks']:
        setattr(exhibition, key, value)

      # FUTURE: Add conditional for start/end dates
      # FUTURE: Check if start date/end date is complete
      # FUTURE: Check if end date is after start date

    # FUTURE: Add exh_art_park relationships

    # Add any orgs to exhibitions.org
    if 'orgs' in params:
      print "There's orgs in {}!".format(params.get('name'))
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


def format_date(date_text):
  for formatting in ('%Y-%m-%d', '%m.%d.%Y', '%m.%d.%y', '%m/%d/%Y', '%m/%d/%y'):
    try:
      # Determine formatting of date string
      date = datetime.strptime(date_text, formatting)
      # Return date text to match wtforms formatting
      return date.strftime('%Y-%m-%d')
    except ValueError:
      pass
  raise ValueError('Can\'t determine date format!')