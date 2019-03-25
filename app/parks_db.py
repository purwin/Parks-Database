from app import db
from sqlalchemy.ext.hybrid import hybrid_property


artist_artwork = db.Table(
  'artist_artwork',
  db.Column('artwork_id', db.Integer, db.ForeignKey('artwork.id')),
  db.Column('artist_id', db.Integer, db.ForeignKey('artist.id')),
  db.UniqueConstraint(
      'artwork_id',
      'artist_id',
      name='UC_artist_id_artwork_id'
  )
)


exh_org = db.Table(
  'exh_org',
  db.Column('exhibition_id', db.Integer, db.ForeignKey('exhibition.id')),
  db.Column('organization_id', db.Integer, db.ForeignKey('org.id')),
  db.UniqueConstraint(
      'exhibition_id',
      'organization_id',
      name='UC_exhibition_id_organization_id'
  )
)


class Exhibition(db.Model):
  # Bio
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80), default='', nullable=False)
  start_date = db.Column(db.Date())
  end_date = db.Column(db.Date())
  opening = db.Column(db.Date())
  comments = db.Column(db.String(), default='')

  # Install
  install_start = db.Column(db.Date())
  install_end = db.Column(db.Date())
  prm = db.Column(db.String(5), default='')
  approval = db.Column(db.String(5), default='')
  walkthrough = db.Column(db.String(10), default='')
  cb_presentation = db.Column(db.String(10), default='')
  license_mailed = db.Column(db.String(5), default='')
  license_signed = db.Column(db.String(5), default='')
  license_borough = db.Column(db.String(5), default='')
  bond = db.Column(db.String(10), default='')
  coi = db.Column(db.String(10), default='')
  coi_renewal = db.Column(db.String(10), default='')
  signage_submit = db.Column(db.String(5), default='')
  signage_received = db.Column(db.String(5), default='')
  press_draft = db.Column(db.String(5), default='')
  press_approved = db.Column(db.String(), default='')
  web_text = db.Column(db.String(5), default='')
  work_images = db.Column(db.String(5), default='')

  # De-Install
  deinstall_date = db.Column(db.Date())
  deinstall_check = db.Column(db.String(5), default='')
  bond_return = db.Column(db.String(5), default='')
  press_clippings = db.Column(db.String(5), default='')

  # Related
  parks = db.relationship(
      'Park',
      secondary='exh_art_park',
      backref=db.backref('exhibitions'),
      viewonly=True
  )
  artworks = db.relationship(
      'Artwork',
      secondary='exh_art_park',
      backref=db.backref('exhibitions')
  )
  organizations = db.relationship(
      'Org',
      secondary=exh_org,
      backref=db.backref('exhibitions', lazy='dynamic')
  )

  def __repr__(self):
    return "<Exhibition: (%s)>"

  @property
  def serialize(self):

    return {
      'id': self.id,
      'name': self.name,
      'start_date': self.start_date,
      'end_date': self.end_date,
      'opening': self.opening,
      'comments': self.comments,
      'install_start': self.install_start,
      'install_end': self.install_end,
      'prm': self.prm,
      'approval': self.approval,
      'walkthrough': self.walkthrough,
      'cb_presentation': self.cb_presentation,
      'license_mailed': self.license_mailed,
      'license_signed': self.license_signed,
      'license_borough': self.license_borough,
      'bond': self.bond,
      'coi': self.coi,
      'coi_renewal': self.coi_renewal,
      'signage_submit': self.signage_submit,
      'signage_received': self.signage_received,
      'press_draft': self.press_draft,
      'press_approved': self.press_approved,
      'web_text': self.web_text,
      'work_images': self.work_images,
      'deinstall_date': self.deinstall_date,
      'deinstall_check': self.deinstall_check,
      'bond_return': self.bond_return,
      'press_clippings': self.press_clippings
    }


class Park(db.Model):
  __searchable__ = ['name']
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80), nullable=False)
  park_id = db.Column(db.String(8), default='')
  borough = db.Column(db.String(15), default='')
  address = db.Column(db.String(200), default='')
  cb = db.Column(db.String(40), default='')

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
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80), nullable=False)
  parks = db.relationship(
      'Park',
      secondary='exh_art_park',
      backref=db.backref('artworks')
  )
  artists = db.relationship(
      'Artist',
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
  exhibition_id = db.Column(
      db.Integer,
      db.ForeignKey('exhibition.id'),
      primary_key=True
  )
  artwork_id = db.Column(
      db.Integer,
      db.ForeignKey('artwork.id'),
      primary_key=True
  )
  park_id = db.Column(
      db.Integer,
      db.ForeignKey('park.id'),
      primary_key=True
  )

  # db.UniqueConstraint('exhibition_id', 'artwork_id')
  exhib = db.relationship('Exhibition')
  artw = db.relationship('Artwork')
  nycpark = db.relationship('Park')

  def __repr__(self):
    return "<Exh_art_park (%s)>"


class Artist(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  pName = db.Column(db.String(40), nullable=False)
  fName = db.Column(db.String(40), default='')
  email = db.Column(db.String(80), default='')
  phone = db.Column(db.String(12), default='')
  website = db.Column(db.String(80), default='')

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
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(40), nullable=False)
  website = db.Column(db.String(40), default='')
  phone = db.Column(db.String(12), default='')

  @property
  def serialize(self):

    return {
      'id': self.id,
      'name': self.name,
      'phone': self.phone,
      'website': self.website
    }


def init_db():
  db.create_all()


if __name__ == '__main__':
  init_db()
