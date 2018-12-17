import json

# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker

# import db
# from app import db

# import parks_db
# from parks_db import Park


def get_parks(json_file):
  # db.create_all()
  # Read json file
  with open(json_file, 'r') as r:
    # Store json object
    input = json.load(r)

  parks_list = []

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


if __name__ == '__main__':
  # Declare parks json file
  json_file = '/Users/michaelpurwin/Documents/workings/parks database/data/DPR_Parks_001.json'

  init_parks(json_file)