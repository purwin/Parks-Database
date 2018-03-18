from sqlalchemy import create_engine, Column, ForeignKey, Integer, String, DateTime, Table, UniqueConstraint, ForeignKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Exhibition(Base):
	__tablename__ = 'exhibition'
	id = Column(Integer, primary_key=True)
	name = Column(String(80))
	startDate = Column(String(20))
	endDate = Column(String(20))
	installStart = Column(String(20))
	installEnd = Column(String(20))
	deinstallDate = Column(String(20))
	parks = relationship('Park', secondary='exhibition_artwork_park')
	artworks = relationship('Artwork', secondary='exhibition_artwork_park')
	events = relationship('Event', backref='exhibition')
	organizations = relationship('Org', secondary='exh_org', backref='exhibitions', lazy='dynamic')

	def __repr__(self):
		return '<Exhibition:{}>'.format(self.name)

class Park(Base):
	__tablename__ = 'park'
	id = Column(Integer, primary_key=True)
	name = Column(String(80))
	park_id = Column(String(6))
	borough = Column(String(15))
	address = Column(String(100))
	cb = Column(String(10))
	exhibitions = relationship('Exhibition', secondary='exhibition_artwork_park')
	artworks = relationship('Artwork', secondary='exhibition_artwork_park')

	def __repr__(self):
		return '<Park:{}>'.format(self.name)

class Artwork(Base):
	__tablename__ = 'artwork'
	id = Column(Integer, primary_key=True)
	name = Column(String(80))
	exhibitions = relationship('Exhibition', secondary='exhibition_artwork_park')
	parks = relationship('Park', secondary='exhibition_artwork_park')
	creators = relationship('Artist', secondary='artist_artwork', backref='artworks', lazy='dynamic')

	def __repr__(self):
		return '<Artwork:{}>'.format(self.name)

#triple join table
class Exh_art_park(Base):
	__tablename__ = 'exhibition_artwork_park'
	exhibition_id = Column(Integer, ForeignKey('exhibition.id'), primary_key=True)
	artwork_id = Column(Integer, ForeignKey('artwork.id'), primary_key=True)
	park_id = Column(Integer, ForeignKey('park.id'), primary_key=True)

	UniqueConstraint('exhibition_id', 'artwork_id')
	exhib = relationship('Exhibition')
	artw = relationship('Artwork')
	nycpark = relationship('Park')

	def __repr__(self):
		return "<Exh_art_park (%s)>"

class Artist(Base):
	__tablename__ = 'artist'
	id = Column(Integer, primary_key=True)
	pName = Column(String(40))
	fName = Column(String(40))
	email = Column(String(80))
	phone = Column(String(12))
	website = Column(String(80))

	def __repr__(self):
		return '<Artist:{} {}>'.format(self.fName, self.pName)

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

artist_artwork = Table('artist_artwork', Base.metadata,
	Column('artwork_id', Integer, ForeignKey('artwork.id')),
	Column('artist_id', Integer, ForeignKey('artist.id'))
	)

class Org(Base):
	__tablename__ = 'organization'
	id = Column(Integer, primary_key=True)
	name = Column(String(40))
	website = Column(String(40))
	phone = Column(String(12))

exh_org = Table('exh_org', Base.metadata,
	Column('exhibition_id', Integer, ForeignKey('exhibition.id')),
	Column('organization_id', Integer, ForeignKey('organization.id'))
	)

class Event(Base):
	__tablename__ = 'event'
	id = Column(Integer, primary_key=True)
	name = Column(String(40))
	exhibition_id = Column(Integer, ForeignKey('exhibition.id'))
	date = Column(String(20))
	time = Column(String(20))
	location = Column(String(80))

	def __repr__(self):
		return '<Event:{}>'.format(self.name)


# engine = create_engine('sqlite:////Users/michaelpurwin/Documents/workings/parks database/___PARKS_DB/sqlite_parks_db.db')

# Base.metadata.create_all(engine)


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


#potential query examps

#query(...).select_from(Exhibition_artwork_park).join((Exhibition, Exhibition_artwork_park.exhibition_id==Exhibition.id))
# -or- exhib = session.query(Exhibition_artwork_park).filter(Exhibition_artwork_park.exhib_id == '#').all()
#for e in exhib:
#print artwork_id.name
#print park_id.name

#equals: query.filter(User.name == 'leela')
#not equals: query.filter(User.name != 'leela')
#like: query.filter(User.name.like('%leela%'))
#is not null: filter(User.name != None)
#and: filter(User.name == 'leela', User.fullname == 'leela dharan')
#another and: filter(User.name == 'leela').filter(User.fullname == 'leela dharan')
#or: (from sqlalchemy import or_) filter(or_(User.name == 'leela', User.name == 'akshay'))

#another way to add something to a row thing
#bob = Author(name='Bob')
#dune = Book(title='Dune')
#moby_dick = Book(title='Moby Dick')
#bob.books = [dune, moby_dick]