from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from parks_db import *
import sys

app = Flask(__name__)
#app.config.from_pyfile('config.cfg')

engine = create_engine('sqlite:////Users/michaelpurwin/Documents/workings/parks database/parks_db/sqlite_parks_db.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/index')
@app.route('/home')
def home():
	todayItems = []
	activeExhibitions = []
	upcomingItems = []
	exhibitions = session.query(Exhibition).all()
	parks = session.query(Park).all()
	return render_template('home.html', exhibitions=exhibitions, parks=parks)

@app.route('/create', methods=['GET', 'POST'])
def create():
	if request.method == 'POST':
		if request.form['create_item'] == 'exhibition':
			newItem = Exhibition(name=request.form['exh_name'], startDate=request.form['exh_startDate'], endDate=request.form['exh_endDate'], installStart=request.form['exh_installStart'], installEnd=request.form['exh_installEnd'], deinstallDate=request.form['exh_deinstallDate'])
			session.add(newItem)
			session.flush()
			try:
				exh_art = request.form.getlist('exh_art')
				exh_park = request.form.getlist('exh_park')
				for x, y in zip(exh_art, exh_park):
					exh_rel = Exh_art_park(exhibition_id=newItem.id, artwork_id=x, park_id=y)
					session.add(exh_rel)
				for z in request.form.getlist('exh_org'):
					org = session.query(Org).filter_by(id=z).one()
					newItem.organizations.append(org)
			except:
				e = sys.exc_info()[0]
				print "error: {}".format(e)
		elif request.form['create_item'] == 'artwork':
			session.add(Artwork(name=request.form['art_name']))
		elif request.form['create_item'] == 'park':
			session.add(Park(name=request.form['park_name'], park_id=request.form['park_park_id'], borough=request.form['park_borough'], address=request.form['park_address'], cb=request.form['park_cb']))
		elif request.form['create_item'] == 'artist':
			session.add(Artist(pName=request.form['artist_pName'], fName=request.form['artist_fName'], email=request.form['artist_email'], phone=request.form['artist_phone'], website=request.form['artist_website']))
		elif request.form['create_item'] == 'organization':
			session.add(Org(name=request.form['org_name'], website=request.form['org_website'], phone=request.form['org_phone']))
		else: return redirect(url_for('home'))
		#session.add(newItem)
		session.commit()
		return redirect(url_for('home'))
	else:
		artworks = session.query(Artwork).all()
		parks = session.query(Park).all()
		orgs = session.query(Org).all()
		artists = session.query(Artist).all()
		return render_template('create.html', artworks=artworks, parks=parks, orgs=orgs, artists=artists)

@app.route('/createArtist', methods=['GET', 'POST'])
def createArtist():
	session.add(Artist(pName=request.form['artist_pName'], fName=request.form['artist_fName'], email=request.form['artist_email'], phone=request.form['artist_phone'], website=request.form['artist_website']))
	session.commit()
	session.flush()
	artists = session.query(Artist).all()
	return jsonify({'data': render_template('include/artist_list.html', artists=artists)})

@app.route('/createArt', methods=['GET', 'POST'])
def createArt():
	newArtwork = Artwork(name=request.form['art_name'])
	session.add(newArtwork)
	try:
		art_artist = request.form.getlist('art_artist')
		for x in art_artist:
			creator = session.query(Artist).filter_by(id=x).one()
			newArtwork.creators.append(creator)
		session.commit()
		session.flush()
		artworks = session.query(Artwork).all()
		parks = session.query(Park).all()
		return jsonify({'data': render_template('include/art_list.html', artworks=artworks, parks=parks)})
	except:
		e = sys.exc_info()[0]
		print "error: {}".format(e)

@app.route('/createOrg', methods=['POST'])
def createOrg():
	session.add(Org(name=request.form['org_name'], website=request.form['org_website'], phone=request.form['org_phone']))
	session.commit()
	session.flush()
	orgs = session.query(Org).all()
	return jsonify({'data': render_template('include/org_list.html', orgs=orgs)})

@app.route('/exhibitions')
def exhibitions():
	activeExhibitions = []
	activeDeinstalls = []
	upcomingExhibitions = []
	exhibitions = session.query(Exhibition).all()
	return render_template('exhibitions.html', exhibitions = exhibitions)

@app.route('/exhibitions/<int:exhibition_id>')
def exhibition(exhibition_id):
	exhibition = session.query(Exhibition).filter_by(id=exhibition_id).one()
	exhib = session.query(Exh_art_park).filter_by(exhibition_id=exhibition_id).all()
	return render_template('exhibition.html', exhibition = exhibition, exhib = exhib)

@app.route('/parks')
def parks():
	parks = session.query(Park).all()
	activeParks = []
	return render_template('parks.html', parks = parks)

@app.route('/parks/<int:park_id>')
def park(park_id):
	park = session.query(Park).filter_by(id=park_id).one()
	park_art = session.query(Exh_art_park).filter_by(park_id=park_id).all()
	return render_template('park.html', park = park, park_art = park_art)

@app.route('/artists')
def artists():
	artists = session.query(Artist).all()
	return render_template('artists.html', artists = artists)

@app.route('/artists/<int:artist_id>')
def artist(artist_id):
	artist = session.query(Artist).filter_by(id=artist_id).one()
	return render_template('artist.html', artist = artist)

@app.route('/artworks')
def artworks():
	artworks = session.query(Artwork).all()
	return render_template('artworks.html', artworks = artworks)

@app.route('/artworks/<int:artwork_id>')
def artwork(artwork_id):
	artwork = session.query(Artwork).filter_by(id=artwork_id).one()
	return render_template('artwork.html', artwork = artwork)

@app.route('/organizations')
def orgs():
	orgs = session.query(Org).all()
	return render_template('orgs.html', orgs=orgs)

@app.route('/organizations/<int:organization_id>')
def org(organization_id):
	org = session.query(Org).filter_by(id=organization_id).one()
	return render_template('org.html', org = org)


if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0', port=5000)