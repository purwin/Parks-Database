from flask import Flask, render_template
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

#install flask-migrate: pip install flask-migrate
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

Base = declarative_base()


class Exhibition(Base):
	__tablename__ = 'exhibiton'
	id = Column(Integer, primary_key=True)
	name = Column(String(150))
	notes = Column(Text)
	startDate = Column(Date)
	endDate = Column(Date)
	openingDate = Column(Date)
	artworks = relationship('Artwork', secondary=exhibition_artwork)

	@property
	def serialize(self):

		return {
			'name': self.name,
			'description': self.description,
			'id': self.id,
			'price': self.price,
			'course': self.course,
		}

exhibition_artwork = Table('exhibition_artwork', Base.metadata,
	Column('exhibition_id', Integer, ForeignKey('exhibition.id')),
	Column('artwork_id', Integer, ForeignKey('artwork.id'))
		)

class Park(Base):
	__tablename__ = 'park'
	id = Column(Integer, primary_key=True)
	name = Column(String(80))
	park_id = Column(Integer, unique=True)

class Artwork(Base):
	__tablename__ = 'artwork'
	id = Column(Integer, primary_key=True)
	name = Column(String(80))
	exhibitions = relationsip('Exhibition', secondary=exhibition_artwork)
	rel_artists = relationship('Artist', secondary=artist_artwork, backref=backref('creators', lazy='dynamic'))

class Artist(Base):
	__tablename__ = 'artist'
	id = Column(Integer, primary_key=True)
	pName = Column(String(40))
	fName = Column(String(40))

artist_artwork = Table('artist_artwork', Base.metadata,
	Column('artwork_id', Integer, ForeignKey('artwork.id')),
	Column('artist_id', Integer, ForeignKey('artist.id'))
		)

class Organization(Base):
	__tablename__ = 'organization'
	id = Column(Integer, primary_key=True)
	name = Column(String(80))
	website = Column(String(80))
	organizer = relationship('Organizer')

class Organizer(Base):
	__tablename__ = 'organizer'
	id = Column(Integer, primary_key=True)
	pName = Column(String(80))
	fName = Column(String(80))
	email = Column(String(80))
	phone = Column(String(80))
	organization_id = Column(Integer, ForeignKey('organization.id'))
	organization = relationship(Organization)

class Event(Base):
	__tablename__ = 'event'
	id = Column(Integer, primary_key=True)
	name = Column(String(80))
	type = Column(String(80))
	location = Column(String(80))
	#date
	#time
	exhibition_id = Column(Integer, ForeignKey('exhibition.id'))
	#org
	#organizer
	#attachments

class Employee(Base):
	__tablename__ = 'employee'
	id = Column(Integer, primary_key=True)
	name = Column(String(40))
	username = Column(String(40), unique=True)
	password = Column(String(40))
	email = Column(String(40))

	def __repr__(self):
		return '<User %r>' % self.username


engine = create_engine('sqlite:///parks.db')

Base.metadata.create_all(engine)
