from app import app, db
from parks_db import Exh_art_park, Exhibition, Park, Artwork, Artist, Org



def import_park(**data):
  pass
  if not data.id:
    park = Park()
  else:
    park = Park.query.filter_by(id = data.id).one()

  park.name = data.name
  park.park_id = data.park_id
  park.borough = data.borough
  park.address = data.address
  park.cb = data.cb
  # Add park to database
  db.session.add(park)
  db.session.commit()
