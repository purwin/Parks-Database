from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from parks_db import *

engine = create_engine('sqlite:////Users/michaelpurwin/Documents/workings/parks database/___PARKS_DB/sqlite_parks_db.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


dean = session.query(Artist).filter_by(id=1).one()
other = session.query(Artist).filter_by(id=2).one()
cool = session.query(Artwork).filter_by(id=2).one()
art1 = session.query(Exhibition).filter_by(id=1).one()
exhib1 = session.query(Exh_art_park).filter_by(exhibition_id=1).all()
park1 = session.query(Park).filter_by(id=1).one()
try1 = Ex_artwork_park()


exhib = session.query(Exh_art_park).filter(exhibition_id=1).all()

for x in exhib:
	print '%s at %s from %s to %s' % (x.artw.name, x.nycpark.name, x.exhib.startDate, x.exhib.endDate)

for x in exhib:
	print x.artw.creators.all()

for x in exhib1:
	for y in x.artw.creators:
		print y


#get details on an exhibition, like .artworks, .parks, etc.
r = session.query(Exhibition).filter(Exhibition.id == Exhibition_artwork_park.exhibition_id).\
    filter(Exhibition_artwork_park.artwork_id == Artwork.id).\
    filter(Exhibition_artwork_park.artwork_id == Park.id).\
    filter(Exhibition.id == ... )

r = session.query(Exhibition_artwork_park).filter(Exhibition.id == Exhibition_artwork_park.exhibition_id).\
    filter(Exhibition_artwork_park.artwork_id == Artwork.id).\
    filter(Exhibition_artwork_park.artwork_id == Park.id).\
    filter(Exhibition_artwork_park.exhibition_id == 1 ).\
    filter(Exhibition_artwork_park.artwork_id == 1 )

g = session.query(Artwork, Exhibition, Park, Exhibition_artwork_park).filter(Artwork.id == Exhibition_artwork_park.artwork_id).\
	filter(Exhibition.id == Exhibition_artwork_park.exhibition_id).\
	filter(Park.id == Exhibition_artwork_park.park_id).\
	filter(Exhibition.id == 1)

g = session.query(Artwork, Exhibition, Park, Exhibition_artwork_park).filter(Artwork.id == Exhibition_artwork_park.artwork_id).\
    filter(Exhibition.id == Exhibition_artwork_park.exhibition_id).\
    filter(Park.id == Exhibition_artwork_park.park_id).\
    filter(Exhibition.id == 1).first()

#triple join table
class Exhibition_artwork_park(Base):
	__tablename__ = 'exhibition_artwork_park'
	exhibition_id = Column(Integer, ForeignKey('exhibition.id'), primary_key=True)
	artwork_id = Column(Integer, ForeignKey('artwork.id'), primary_key=True)
	park_id = Column(Integer, ForeignKey('park.id'))

	UniqueConstraint('exhibition_id', 'artwork_id')
	relationship('Exhibition', uselist=False, backref='exh_art_park', lazy='dynamic')
	relationship('Artwork', uselist=False, backref='exh_art_park', lazy='dynamic')
	relationship('Park', uselist=False, backref='exh_art_park', lazy='dynamic')

	def __repr__(self):
		return "<Exh_art_park({})>".format(self.id)

		


class Artwork_park(Base):
	__tablename__ = 'artwork_park'
	id = Column(Integer, primary_key=True)
	Column('artwork_id', Integer, ForeignKey('artwork.id'))
	Column('park_id', Integer, ForeignKey('park.id'))

class Exhibition_artwork(Base):
	__tablename__ = 'exhibition_artwork'
	id = Column(Integer, primary_key=True)
	Column('exhibition_id', Integer, ForeignKey('exhibition.id'))
	Column('artwork_id', Integer, ForeignKey('artwork.id'))

Table('exh_art_park', Base.metadata,
	Column('artwork_park_id', Integer, ForeignKey('artwork_park.id'), primary_key=True)
	Column('exhibition_artwork_id', Integer, ForeignKey('exhibition_artwork.id'), primary_key=True)
	)



	def __init__(self, exhibition, artwork, park):
		self.exhibition_id = exhibition.id
		self.artwork_id = artwork.id
		self.park_id = park.id

'''
Table('exhibition_artwork_park', Base.metadata,
	exhibition_id = Column(Integer, ForeignKey('exhibition.id'), primary_key=True),
	artwork_id = Column(Integer, ForeignKey('artwork.id'), primary_key=True),
	park_id = Column(Integer, ForeignKey('park.id'), primary_key=True),

	UniqueConstraint('exhibition_id', 'artwork_id', 'park_id')

	#relationship('Exhibition', uselist=False, backref='ex_art_parks', lazy='dynamic')
    #relationship('Artwork', uselist=False, backref='ex_art_parks', lazy='dynamic')
    #relationship('Park', uselist=False, backref='ex_art_parks', lazy='dynamic')
)
'''