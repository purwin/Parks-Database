# -*- coding: utf-8 -*-

from datetime import datetime

from app import db
from app.parks_db import Exhibition
import add_org
import add_artwork
import add_park
import add_exh_art_park


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


def add_exhibition(match=True, **params):
  """
  Add dict argument to Exhibition database table

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
      "result": "Couldn't determine object name.",
      "warning": "",
      "data": params
    }

  name = params.get('name')

  exhibition = False

  # Check for existing ID
  if params.get('id'):
    exhibition = Exhibition.query.filter_by(id=id).first()
  # Or search for existing items if match option is set
  elif match == True:
    exhibition = Exhibition.query.filter_by(name=name).first()

  result = 'Found {} in the database. Updated exhibition with new data.'\
           .format(name)

  if not exhibition:
    exhibition = Exhibition()
    result = 'Added new exhibition: {}.'.format(name)

  # Define warnings string to return
  warnings = ""

  # Loop through passed key/value attributes, add to class object
  try:
    for key, value in params.iteritems():
      # Check for bad keys, skip and add to warning list
      if key not in exhibition_params:
        warnings += 'Unexpected {} attribute found. Skipping "{}" addition.\n'\
                    .format(key, value)

      # Add non-list key items to exhibition object
      elif key not in ['exh_art_park', 'orgs', 'artworks', 'parks']:
        # Check for date keys
        if key in ['start_date', 'end_date', 'opening', 'install_start',
                   'install_end', 'deinstall_date']:
          # Create a date object from string
          value = format_date(value)

        # FUTURE: Check if start date/end date is complete
        # FUTURE: Check if end date is after start date

        setattr(exhibition, key, value)

    db.session.add(exhibition)

    # Add any orgs to exhibitions.org
    if 'orgs' in params:
      orgs = params.get('orgs', None)
      # If exhibition.organizations is string, convert to list
      orgs = [orgs] if isinstance(orgs, str) else orgs
      for org in orgs or []:
        organization = add_org.add_org(name=org)

        if organization['success'] == True:
          if organization['org'] not in exhibition.organizations:
            exhibition.organizations.append(organization['org'])
            result += "\nAdded {} to the {} exhibition"\
                      .format(org, exhibition.name)


    # Add exh_art_park relationships
    if 'artworks' and 'parks' in params:
      # Flush session to get and use exhibition ID
      db.session.flush()

      artworks = filter(None, params.get('artworks', None))
      # If park.artworks is string, convert to list
      artworks = [artworks] if isinstance(artworks, str) else artworks

      parks = filter(None, params.get('parks', None))
      # If exhibition.parks is string, convert to list
      parks = [parks] if isinstance(parks, str)\
                                  else parks

      if len(parks) != len(artworks):
        warnings += 'There’s an uneven number of artworks and parks in '\
                    '{}. Skipping addition.\n'.format(name)
      else:

        for artwork, park in zip(artworks, parks):
          artwork_dict = add_artwork.add_artwork(name=artwork)
          artwork_id = artwork_dict['data']['id']

          park_dict = add_park.add_park(name=park)
          park_id = park_dict['data']['id']

          exh_art_park = add_exh_art_park.add_exh_art_park(
              exhibition_id=exhibition.id,
                 artwork_id=artwork_id,
                    park_id=park_id)

          if exh_art_park['success'] == True:
            result += "\nAdded {} @ {} to the {} exhibition"\
                      .format(exhibition.name, artwork, park)
            print "Added {} @ {} to the {} exhibition".format(exhibition.name, artwork, park)
          else:
            warnings += "{}\n".format(exh_art_park['result'])

    db.session.commit()
    db.session.flush()

    print "Add_exhibition: {}".format(result)

    return {
      "success": True,
      "result": result,
      "warning": warnings,
      "data": exhibition.serialize,
      "exhibition": exhibition
    }

  except Exception as e:
    db.session.rollback()
    print "Error: {}".format(e)

    return {
      "success": False,
      "result": "{}: {}".format(name, e),
      "warning": warnings,
      "data": params
    }


def format_date(date_text):
  for style in ('%Y-%m-%d', '%m.%d.%Y', '%m.%d.%y', '%m/%d/%Y', '%m/%d/%y'):
    try:
      # Determine style of date string
      date = datetime.strptime(date_text, style)
      # Return date object
      return date
    except ValueError:
      pass
  raise ValueError('Can\'t determine date format of {}!'.format(date_text))
