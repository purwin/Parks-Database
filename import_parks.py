#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import json

# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker

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
  # db.create_all()
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

  # for i in input:
  #   print i
  #   return
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


def add_park(obj):
  # Determine borough
  if obj['Park_ID'].startswith('X'):
    borough = 'Bronx'
  elif obj['Park_ID'].startswith('B'):
    borough = 'Brooklyn'
  elif obj['Park_ID'].startswith('M'):
    borough = 'Manhattan'
  elif obj['Park_ID'].startswith('Q'):
    borough = 'Queens'
  elif obj['Park_ID'].startswith('R'):
    borough = 'Staten Island'
  else:
    print "ERROR: {}".format(obj)
    dump_errors(obj)

  # Determine address
  if obj['Zip']:
    address = "{}, {} NY {}".format(obj['Location'], borough, obj['Zip'])
  else:
    address = "{}, {} NY".format(obj['Location'], borough)

  return
  new_park = Park(name=obj['Name'],
                  park_id=obj['Park_ID'],
                  address=address,
                  borough=borough)
  db.session.add(new_park)
  db.session.commit()


def dump_errors(obj):
  with open('errors_park.txt', 'a') as w:
    json.dump(obj, w)


if __name__ == '__main__':
  # Declare parks JSON file
  json_file = '/Users/michaelpurwin/Documents/workings/parks database/data/DPR_Parks_001.json'

  get_parks(json_file)