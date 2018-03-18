from sqlalchemy import create_engine, Column, ForeignKey, Integer, String, DateTime, Table
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
#	parks = relationship('Park', secondary='exhibition_park', backref='exhibitions', lazy='dynamic')
#	prmReview = Column(String(15))
#	boroughApproval = Column(String(15))
#	walkThrough = Column(String(15))
#	cbPresentation = Column(String(15))

exhibition_artwork = Table('exhibition_artwork', Base.metadata,
	Column('exhibition_id', Integer, ForeignKey('exhibition.id')),
	Column('artwork_id', Integer, ForeignKey('artwork.id'))
		)

class Park(Base):
	__tablename__ = 'park'
	id = Column(Integer, primary_key=True)
	name = Column(String(80))
	park_id = Column(String(6))
	borough = Column(String(15))
	address = Column(String(100))
	cb = Column(String(10))

Table('artwork_park', Base.metadata,
	Column('artwork_id', Integer, ForeignKey('artwork.id')),
	Column('park_id', Integer, ForeignKey('park.id'))
	)

class Artwork(Base):
	__tablename__ = 'artwork'
	id = Column(Integer, primary_key=True)
	name = Column(String(80))
	exhibitions = relationship('Exhibition', secondary='exhibition_artwork', backref='artworks', lazy='dynamic')
	creators = relationship('Artist', secondary='artist_artwork', backref='artworks', lazy='dynamic')
	parks = relationship('Park', secondary='artwork_park', backref='artworks', lazy='dynamic')

class Artist(Base):
	__tablename__ = 'artist'
	id = Column(Integer, primary_key=True)
	pName = Column(String(40))
	fName = Column(String(40))
	email = Column(String(80))
	phone = Column(String(12))
	website = Column(String(80))

artist_artwork = Table('artist_artwork', Base.metadata,
	Column('artwork_id', Integer, ForeignKey('artwork.id')),
	Column('artist_id', Integer, ForeignKey('artist.id'))
		)

engine = create_engine('sqlite:////Users/michaelpurwin/Documents/workings/parks database/___PARKS_DB/sqlite_parks_db.db')

Base.metadata.create_all(engine)