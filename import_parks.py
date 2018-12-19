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

  # Start up database
  init_db()

  # Parse JSON file, add objects to database
  input = get_parks(json_file)

  # If park name is a duplicate, add park_id to make unique
  for i in input:
    # Determine borough
    i['Borough'] = determine_borough(i)

    # Determine borough
    i['Address'] = determine_address(i)

    # Determine community board(s)
    i['CB'] = get_site(i['Name'])

    # Update park name for items in duplicate list
    if i['Name'] in duplicate_list:
      i['Name'] = "{} {}".format(i['Prop_ID'], i['Name'])

    # Add updated park to database
    add_park({
      'Park_ID': i['Prop_ID'],
      'Name': i['Name'],
      'CB': i['CB'],
      'Borough': i['Borough'],
      'Address': i['Address']
    })


def get_parks(json_file):
  # Read JSON file
  with open(json_file, 'r') as r:
    # Store JSON object
    input = json.load(r)

  return input


def init_db():
  db.create_all()


def determine_address(obj):
  # Determine address
  if obj['Zip']:
    address = "{}, {} NY {}".format(obj['Location'], obj['Borough'], obj['Zip'])
  else:
    address = "{}, {} NY".format(obj['Location'], obj['Borough'])

  return address


def determine_borough(obj):
  if obj['Prop_ID'].startswith('X'):
    return 'Bronx'
  elif obj['Prop_ID'].startswith('B'):
    return 'Brooklyn'
  elif obj['Prop_ID'].startswith('M'):
    return 'Manhattan'
  elif obj['Prop_ID'].startswith('Q'):
    return 'Queens'
  elif obj['Prop_ID'].startswith('R'):
    return 'Staten Island'
  else:
    print "Borough Error: {}: {}".format(obj['Name'], obj['Prop_ID'])
    dump_errors("{}: Cannot determine borough.\n".format(obj['Name']))
    return None


def add_park(obj):
  with open('parks-dump.txt', 'a') as w:
    w.write(json.dumps(obj))
    w.write(',')

  # Add parks to database
  return
  try:
    new_park = Park(name=obj['Name'],
                    park_id=obj['Park_ID'],
                    address=obj['Address'],
                    borough=obj['Borough'],
                    cb=obj['CB'])
    db.session.add(new_park)
    db.session.commit()
  except Exception as e:
    dump_errors("{}: {}\n".format(obj['Name'], e))


def get_site(name):
  url_name = name.lower().replace(' ', '-')\
                         .replace('.', '')\
                         .replace(' ', '-')\
                         .replace('\'', "")
  r = requests.get('https://www.nycgovparks.org/parks/{}'.format(url_name))
  if r.status_code == 200:
    print "Site found: {}".format(name)
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


def find_cb(text):
  search = re.findall(r'<strong>Community Board:</strong>(.+?)<br/>', text, re.DOTALL)
  try:
    findings = search[0].lstrip().rstrip()
  except:
    findings = None

  return findings


def dump_errors(error):
  with open('errors_park.txt', 'a') as w:
    w.write(error)


if __name__ == '__main__':
  # Declare parks JSON file
  json_file = '/Users/michaelpurwin/Documents/workings/parks database/data/sort/DPR_Parks_R-03.json'

  import_parks(json_file)
