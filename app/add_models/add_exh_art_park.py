# -*- coding: utf-8 -*-

from app import db
from app.parks_db import Exh_art_park
import add_artwork
import add_exhibition
import add_park


def add_exh_art_park(exhibition_id, artwork_id, park_id):
  """
  Add dict argument to Artwork database table

  Returns a dict with four attributes:
  - "success": boolean value
  - "data": added dict item
  - "result": string detailing database results
  - "warning": string detailing any unforseen issues
  """
  # Search for existing relationship in exh_art_park table
  exh_art_park = Exh_art_park.query.filter_by(exhibition_id=exhibition_id)\
                             .filter_by(artwork_id=artwork_id)\
                             .filter_by(park_id=park_id).first()

  success = True
  result = "Exh_art_park: Already exists Exh {} > Art {} > Park {}\n"\
      .format(exhibition_id, artwork_id, park_id)

  print "Exh_art_park: Already exists Exh {} > Art {} > Park {}\n"\
      .format(exhibition_id, artwork_id, park_id)


  if not exh_art_park:
    # Add relationship if nothing found
    try:
      exh_rel = Exh_art_park(exhibition_id=exhibition_id, artwork_id=artwork_id,
          park_id=park_id)

      db.session.add(exh_rel)
      db.session.commit()

      result = "Exh_art_park: Added Exh {} > Art {} > Park {}\n"\
          .format(exhibition_id, artwork_id, park_id)

    except Exception as e:
      print "Exh_art_park error: {}".format(e)

      success = False
      result = "Exh_art_park: Error: {}".format(e)

  return {
    "success": success,
    "result": result
  }



def parse_exh_art_park(parks_list, artworks_list, exhibitions_list):
  pass

  for exhibition, artwork, park in \
      zip(exhibitions_list, artworks_list, parks_list):
    artwork_dict = add_artwork.add_artwork({'name': artwork})
    print "Art dict: {}".format(artwork_dict)
    artwork_id = artwork_dict.data.id
    print "Art ID: {}".format(artwork_id)

    exhibition_dict = add_exhibition.add_exhibition({'name': exhibition})
    print "Exhibition dict: {}".format(exhibition_dict)
    exhibition_id = exhibition_dict.data.id
    print "Exhibition ID: {}".format(exhibition_id)


    exh_art_park = add_exh_art_park(
        exhibition_id=exhibition_id,
           artwork_id=artwork_id,
              park_id=park.id)