import json

# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker

# import db
# from app import db

# import parks_db
# from parks_db import Park


def init_parks(json_file):
  pass
  # db.create_all()
  # read json file
  with open(json_file, 'r') as r:
    # Store json object
    input = json.load(r)




if __name__ == '__main__':
  # Declare parks json file
  json_file = '/Users/michaelpurwin/Documents/workings/parks database/data/DPR_Parks_001.json'

  init_parks(json_file)