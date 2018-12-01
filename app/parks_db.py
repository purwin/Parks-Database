from app import db
from sqlalchemy.ext.hybrid import hybrid_property
# from sqlalchemy import UniqueConstraint, ForeignKeyConstraint


artist_artwork = db.Table(
  'artist_artwork',
  db.Column('artwork_id', db.Integer, db.ForeignKey('artwork.id')),
  db.Column('artist_id', db.Integer, db.ForeignKey('artist.id')),
  db.UniqueConstraint('artwork_id', 'artist_id', name='UC_artist_id_artwork_id')
)


exh_org = db.Table(
  'exh_org',
  db.Column('exhibition_id', db.Integer, db.ForeignKey('exhibition.id')),
  db.Column('organization_id', db.Integer, db.ForeignKey('org.id')),
  db.UniqueConstraint('exhibition_id', 'organization_id', name='UC_exhibition_id_organization_id')
)


class Exhibition(db.Model):
  # __tablename__ = 'exhibition'
  # Bio
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80))
  start_date = db.Column(db.Date())
  end_date = db.Column(db.Date())
  opening = db.Column(db.Date())
  comments = db.Column(db.String())

  # Install
  install_start = db.Column(db.Date())
  install_end = db.Column(db.Date())
  prm = db.Column(db.String(5))
  approval = db.Column(db.String(5))
  walkthrough = db.Column(db.String(10))
  cb_presentation = db.Column(db.String(10))
  license_mailed = db.Column(db.String(5))
  license_signed = db.Column(db.String(5))
  license_borough = db.Column(db.String(5))
  bond = db.Column(db.String(10))
  coi = db.Column(db.String(10))
  coi_renewal = db.Column(db.String(10))
  signage_submit = db.Column(db.String(5))
  signage_received = db.Column(db.String(5))
  press_draft = db.Column(db.String(5))
  press_approved = db.Column(db.String())
  web_text = db.Column(db.String(5))
  work_images = db.Column(db.String(5))

  # De-Install
  deinstall_date = db.Column(db.Date())
  deinstall_check = db.Column(db.String(5))
  bond_return = db.Column(db.String(5))
  press_clippings = db.Column(db.String(5))

  # Related
  parks = db.relationship('Park',
                          secondary='exh_art_park',
                          backref=db.backref('exhibitions')
  )
  artworks = db.relationship('Artwork',
                             secondary='exh_art_park',
                             backref=db.backref('exhibitions')
  )
  events = db.relationship('Event', backref='exhibitions')
  organizations = db.relationship('Org',
                                  secondary=exh_org,
                                  backref=db.backref('exhibitions',
                                                     lazy='dynamic'
                                                    )
  )

  def __repr__(self):
    return "<Exhibition: (%s)>"

  @property
  def serialize(self):

    return {
      'id': self.id,
      'name': self.name
    }


class Park(db.Model):
  # __tablename__ = 'park'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80))
  park_id = db.Column(db.String(6))
  borough = db.Column(db.String(15))
  address = db.Column(db.String(100))
  cb = db.Column(db.String(10))

  def __repr__(self):
    return "<Park: (%s)>"

  @property
  def serialize(self):

    return {
      'id': self.id,
      'name': self.name,
      'park_id': self.park_id,
      'borough': self.borough,
      'address': self.address,
      'cb': self.cb
    }


class Artwork(db.Model):
  # __tablename__ = 'artwork'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80))
  parks = db.relationship('Park',
                          secondary='exh_art_park',
                          backref=db.backref('artworks')
  )
  artists = db.relationship('Artist',
                             secondary='artist_artwork',
                             backref=db.backref('artworks', lazy='dynamic')
  )

  def __repr__(self):
      return '<Artwork:{}>'.format(self.name)

  @property
  def serialize(self):
    return {
      'id': self.id,
      'name': self.name
    }


class Exh_art_park(db.Model):
  # __tablename__ = 'exh_art_park'
  # id = db.Column(db.Integer, primary_key=True)
  exhibition_id = db.Column(db.Integer,
                            db.ForeignKey('exhibition.id'),
                            primary_key=True
  )
  artwork_id = db.Column(db.Integer,
                         db.ForeignKey('artwork.id'),
                         primary_key=True
  )
  park_id = db.Column(db.Integer,
                      db.ForeignKey('park.id'),
                      primary_key=True
  )

  # db.UniqueConstraint('exhibition_id', 'artwork_id')
  exhib = db.relationship('Exhibition')
  artw = db.relationship('Artwork')
  nycpark = db.relationship('Park')

  def __repr__(self):
    return "<Exh_art_park (%s)>"

# Exh_art_park = db.Table('exhibition_artwork_park',
#   db.Column('exhibition_id', db.Integer, db.ForeignKey('exhibition.id'), primary_key=True),
#   db.Column('artwork_id', db.Integer, db.ForeignKey('artwork.id'), primary_key=True),
#   db.Column('park_id', db.Integer, db.ForeignKey('park.id'), primary_key=True)
# )


class Artist(db.Model):
  # __tablename__ = 'artist'
  id = db.Column(db.Integer, primary_key=True)
  pName = db.Column(db.String(40))
  fName = db.Column(db.String(40))
  email = db.Column(db.String(80))
  phone = db.Column(db.String(12))
  website = db.Column(db.String(80))

  @hybrid_property
  def name(self):
      if self.fName is not None:
          return self.fName + " " + self.pName
      else:
          return self.pName

  def __repr__(self):
    return "<Artist: (%s)>"

  @property
  def serialize(self):
    return {
      'id': self.id,
      'pName': self.pName,
      'fName': self.fName,
      'name': self.name,
      'email': self.email,
      'phone': self.phone,
      'website': self.website
    }


class Org(db.Model):
  # __tablename__ = 'org'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(40))
  website = db.Column(db.String(40))
  phone = db.Column(db.String(12))

  @property
  def serialize(self):

    return {
      'id': self.id,
      'name': self.name,
      'phone': self.phone,
      'website': self.website
    }


class Event(db.Model):
  # __tablename__ = 'event'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(40))
  exhibition_id = db.Column(db.Integer, db.ForeignKey('exhibition.id'))
  date = db.Column(db.String(20))
  time = db.Column(db.String(20))
  location = db.Column(db.String(80))

  def __repr__(self):
    return "<Event: (%s)>"


def init_db():
  db.create_all()


if __name__ == '__main__':
  init_db()



'''

exhib = session.query(Exh_art_park).filter(exhibition_id=#).all()

for x in exhib:
  print '%s at %s from %s to %s' % (x.artw.name, x.nycpark.name, x.exhib.startDate, x.exhib.endDate)

for x in exhib:
  print x.artw.creators.all()

for x in exhib:
  for y in x.artw.creators:
    print y


'''
