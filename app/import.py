# from app import app, db
# from parks_db import Exh_art_park, Exhibition, Park, Artwork, Artist, Org

import pandas as pd




# def import_park(**data):
#   pass
#   if not data.id:
#     park = Park()
#   else:
#     park = Park.query.filter_by(id = data.id).one()

#   park.name = data.name
#   park.park_id = data.park_id
#   park.borough = data.borough
#   park.address = data.address
#   park.cb = data.cb
#   # Add park to database
#   db.session.add(park)
#   db.session.commit()






def main(csv_file):
  file = pd.read_csv(csv_file)
  file.drop(file.columns[file.columns.str.contains('unnamed', case=False)],
    axis=1, inplace=True)
  file_headers = file.columns.values
  row_1 = file[1:5]
  for index, row in row_1.iterrows():
    d = {}
    for col in file_headers:
      d[col] = row[col]
    print d

if __name__ == '__main__':
  main('/Users/michaelpurwin/Documents/workings/parks database/data/CURRENT_Public-Art-Chronology_1.30.2017.csv')