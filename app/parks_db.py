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
	db.Column('organization_id', db.Integer, db.ForeignKey('org.id'))
)


class Exhibition(db.Model):
	# __tablename__ = 'exhibition'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80))
	startDate = db.Column(db.String(20))
	endDate = db.Column(db.String(20))
	installStart = db.Column(db.String(20))
	installEnd = db.Column(db.String(20))
	deinstallDate = db.Column(db.String(20))
	parks = db.relationship('Park',
													secondary='exh_art_park',
													backref=db.backref('exhibition')
	)
	artworks = db.relationship('Artwork',
														 secondary='exh_art_park',
														 backref=db.backref('exhibition')
	)
	events = db.relationship('Event', backref='exhibition')
	organizations = db.relationship('Org',
																	secondary=exh_org,
																	backref=db.backref('exhibition',
																										 lazy='dynamic'
																										)
	)
	prm = db.Column(db.String(10))

	def __repr__(self):
		return "<Exhibition: (%s)>"


class Park(db.Model):
	# __tablename__ = 'park'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80))
	park_id = db.Column(db.String(6))
	borough = db.Column(db.String(15))
	address = db.Column(db.String(100))
	cb = db.Column(db.String(10))
	exhibitions = db.relationship('Exhibition',
																secondary='exh_art_park',
																backref=db.backref('park')
	)
	artworks = db.relationship('Artwork',
														 secondary='exh_art_park',
														 backref=db.backref('park')
	)

	def __repr__(self):
		return "<Park: (%s)>"


class Artwork(db.Model):
	# __tablename__ = 'artwork'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80))
	exhibitions = db.relationship('Exhibition',
																secondary='exh_art_park',
																backref=db.backref('artwork')
	)
	parks = db.relationship('Park',
													secondary='exh_art_park',
													backref=db.backref('artwork')
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
			'name': self.name,
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
# 	db.Column('exhibition_id', db.Integer, db.ForeignKey('exhibition.id'), primary_key=True),
# 	db.Column('artwork_id', db.Integer, db.ForeignKey('artwork.id'), primary_key=True),
# 	db.Column('park_id', db.Integer, db.ForeignKey('park.id'), primary_key=True)
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
	def full_name(self):
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


# potential query examps

#query(...).select_from(Exhibition_artwork_park).join((Exhibition, Exhibition_artwork_park.exhibition_id==Exhibition.id))
# -or- exhib = session.query(Exhibition_artwork_park).filter(Exhibition_artwork_park.exhib_id == '#').all()
# for e in exhib:
# print artwork_id.name
# print park_id.name

# equals: query.filter(User.name == 'leela')
# not equals: query.filter(User.name != 'leela')
# like: query.filter(User.name.like('%leela%'))
# is not null: filter(User.name != None)
# and: filter(User.name == 'leela', User.fullname == 'leela dharan')
# another and: filter(User.name == 'leela').filter(User.fullname == 'leela dharan')
# or: (from sqlalchemy import or_) filter(or_(User.name == 'leela', User.name == 'akshay'))

# another way to add something to a row thing
#bob = Author(name='Bob')
#dune = Book(title='Dune')
#moby_dick = Book(title='Moby Dick')
#bob.books = [dune, moby_dick]
