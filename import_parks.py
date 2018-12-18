#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import json
import requests
# from bs4 import BeautifulSoup
import re

# import current database
from app import db

# import Park class
from app.parks_db import Park



def import_parks(json_file):
  # Start up database
  init_db()

  # Parse JSON file, add objects to database
  get_parks(json_file)


def get_parks(json_file):
  # Read JSON file
  with open(json_file, 'r') as r:
    # Store JSON object
    input = json.load(r)

  # List of parks with duplicate names
  duplicate_list = ['Park', 'GREENSTREET', 'Lafayette Playground',
                    'St. Mary\'s Park', 'Kelly Park', 'Spring Creek Park',
                    'La Guardia Playground', 'Flatbush Malls', 'Greenstreet',
                    'Dimattina Playground', 'Brooklyn Heights Promenade',
                    'Triangle', 'Classon Playground', 'Bushwick Playground',
                    'Spring Creek Park', 'Jackie Robinson Park',
                    'Columbus Park', 'Park Avenue Malls', 'Grand Army Plaza',
                    'Riverside Park', 'Broadway Malls', 'Harlem River Park',
                    'Battery Park City', 'East River Esplanade',
                    'Highland Park', 'Sitting Area', 'Rockaway Beach',
                    'Kissena Corridor Park', 'Hillside Park', 'Sitting Area',
                    'Hart Playground', 'Veteran\'s Square', 'Veterans Park',
                    'Great Kills Park', 'Carlton Park', 'Meredith Woods',
                    'Aqueduct Walk', 'Railroad Park', 'St. Mary\'s Park',
                    'Martin Luther King Triangle', 'Bridge Park',
                    'Belmont Playground', 'Highbridge Park',
                    'Parkside Playground', 'Fox Playground', 'Rainey Park',
                    'Washington Park']

  # If park name is a duplicate, add park_id to make unique
  for i in input:
    if i['Name'] in duplicate_list:
      add_park({
        'Park_ID': i['Prop_ID'],
        'Name': "{} {}".format(i['Prop_ID'], i['Name']),
        'Zip': i['Zip'],
        'Location': i['Location']
      })
    else:
      add_park({
        'Park_ID': i['Prop_ID'],
        'Name': i['Name'],
        'Zip': i['Zip'],
        'Location': i['Location']
      })


def init_db():
  db.create_all()


def determine_borough(obj):
  if obj['Park_ID'].startswith('X'):
    return 'Bronx'
  elif obj['Park_ID'].startswith('B'):
    return 'Brooklyn'
  elif obj['Park_ID'].startswith('M'):
    return 'Manhattan'
  elif obj['Park_ID'].startswith('Q'):
    return 'Queens'
  elif obj['Park_ID'].startswith('R'):
    return 'Staten Island'
  else:
    print "ERROR: {}".format(obj)
    dump_errors("{}: Cannot determine borough.\n".format(obj['Name']))
    return None


def add_park(obj):
  # Determine borough
  borough = determine_borough(obj)

  # Determine address
  if obj['Zip']:
    address = "{}, {} NY {}".format(obj['Location'], borough, obj['Zip'])
  else:
    address = "{}, {} NY".format(obj['Location'], borough)

  # Determine community board(s)
  obj['CB'] = get_site(obj['Name'])

  print json.dumps(obj)

  # Add parks to database
  return
  try:
    new_park = Park(name=obj['Name'],
                    park_id=obj['Park_ID'],
                    address=address,
                    borough=borough,
                    cb=obj['CB'])
    db.session.add(new_park)
    db.session.commit()
  except Exception as e:
    dump_errors("{}: {}\n".format(obj['Name'], e))


def get_site(name):
  r = requests.get('https://www.nycgovparks.org/parks/{}'.format(name.lower().replace(' ', '-')))
  if r.status_code == 200:
    print "Site found: {}".format(name)
    # print r.text
    # get_cb(r.text)
    cb = find_cb(r.text)
    if not cb:
      dump_errors("{}: Unable to find community board\n".format(name))
      return None
    else:
      print "CB Found: {}".format(cb)
      return cb
  else:
    dump_errors("{}: Unable to connect to Parks site\n".format(name))
    return None


# def get_cb(html):
#   pass
#   page = BeautifulSoup(html, 'html.parser')
#   details = page.find_all(id = 'park_more_details')
#   find_cb(details[0])
#   print str(details[0])


def find_cb(text):
  search = re.findall(r'<strong>Community Board:</strong>(.+?)<br/>', text, re.DOTALL)
  # print "CB Found: {}".format(search[0].lstrip().rstrip())
  return search[0].lstrip().rstrip()


def dump_errors(error):
  with open('errors_park.txt', 'a') as w:
    w.write(error)


if __name__ == '__main__':
  # Declare parks JSON file
  json_file = '/Users/michaelpurwin/Documents/workings/parks database/data/DPR_Parks_002.json'

  import_parks(json_file)
