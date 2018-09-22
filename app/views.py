from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

from app import app, db
from parks_db import Exh_art_park, Exhibition, Park, Artwork, Artist, Org

import sys

@app.route('/')
@app.route('/index')
@app.route('/home')
def home():
  todayItems = []
  activeExhibitions = []
  upcomingItems = []
  exhibitions = Exhibition.query.all()
  parks = Park.query.all()
  return render_template('home.html', exhibitions=exhibitions, parks=parks)


# Route: Create database items
@app.route('/create', methods=['GET', 'POST'])
def create():
  if request.method == 'POST':

    # Create exhibition
    if request.form['create_item'] == 'exhibition':
      newItem = Exhibition(name=request.form['exh_name'], startDate=request.form['exh_startDate'], endDate=request.form['exh_endDate'], installStart=request.form['exh_installStart'], installEnd=request.form['exh_installEnd'], deinstallDate=request.form['exh_deinstallDate'])
      db.session.add(newItem)
      db.session.flush()
      try:
        exh_art = request.form.getlist('exh_art')
        # Remove any empty items from artwork list
        exh_art = filter(None, exh_art)
        exh_park = request.form.getlist('exh_park')
        # Remove any empty items from park list
        exh_park = filter(None, exh_park)
        for x, y in zip(exh_art, exh_park):
          # add exhibition, art, park ref to database
          exh_rel = Exh_art_park(exhibition_id=newItem.id, artwork_id=x, park_id=y)
          db.session.add(exh_rel)

        exh_org = request.form.getlist('exh_org')
        # Remove any empty items from org list
        exh_org = filter(None, exh_org)
        for z in exh_org:
          # add org to exhibition
          org = Org.query.filter_by(id=z).one()
          newItem.organizations.append(org)

      except:
        e = sys.exc_info()[0]
        print "error: {}".format(e)

    # Create artwork
    elif request.form['create_item'] == 'artwork':
      db.session.add(Artwork(name=request.form['art_name']))

    # Create park
    elif request.form['create_item'] == 'park':
      db.session.add(Park(name=request.form['park_name'], park_id=request.form['park_park_id'], borough=request.form['park_borough'], address=request.form['park_address'], cb=request.form['park_cb']))

    # Create artist
    elif request.form['create_item'] == 'artist':
      db.session.add(Artist(pName=request.form['artist_pName'], fName=request.form['artist_fName'], email=request.form['artist_email'], phone=request.form['artist_phone'], website=request.form['artist_website']))

    # Create organization
    elif request.form['create_item'] == 'organization':
      db.session.add(Org(name=request.form['org_name'], website=request.form['org_website'], phone=request.form['org_phone']))

    # Create event

    else: return redirect(url_for('home'))
    db.session.commit()
    return redirect(url_for('home'))

  else:
    artworks = Artwork.query.all()
    parks = Park.query.all()
    orgs = Org.query.all()
    artists = Artist.query.all()
    return render_template('create.html', artworks=artworks, parks=parks, orgs=orgs, artists=artists)


# Route: Create Artist via AJAX request
@app.route('/createArtist', methods=['GET', 'POST'])
def createArtist():
  if request.method == 'POST':
    db.session.add(Artist(pName=request.form['artist_pName'], fName=request.form['artist_fName'], email=request.form['artist_email'], phone=request.form['artist_phone'], website=request.form['artist_website']))
    db.session.commit()
    db.session.flush()
    artists = Artist.query.all()
    return jsonify({'data': render_template('include/artist_list.html', artists=artists)})


# Route: Create Artwork via AJAX request
@app.route('/createArt', methods=['GET', 'POST'])
def createArt():
  if request.method == 'POST':
    # Create new artwork
    newArtwork = Artwork(name=request.form['art_name'])
    db.session.add(newArtwork)
    try:
      art_artist = request.form.getlist('art_artist')
      # Remove any empty items from list
      art_artist = filter(None, art_artist)
      print "Adding these artist IDs to {}: {}".format(newArtwork.name, art_artist)
      for x in art_artist:
        creator = Artist.query.filter_by(id=x).one()
        newArtwork.artists.append(creator)
      db.session.commit()
      db.session.flush()
      artworks = Artwork.query.all()
      parks = Park.query.all()
      return jsonify({'data': render_template('include/art_list.html', artworks=artworks, parks=parks)})
    except:
      e = sys.exc_info()[0]
      print "error: {}".format(e)


# Route: Create Org via AJAX request
@app.route('/createOrg', methods=['POST'])
def createOrg():
  if request.method == 'POST':
    db.session.add(Org(name=request.form['org_name'], website=request.form['org_website'], phone=request.form['org_phone']))
    db.session.commit()
    db.session.flush()
    orgs = Org.query.all()
    return jsonify({'data': render_template('include/org_list.html', orgs=orgs)})


@app.route('/exhibitions')
def exhibitions():
  exhibitions = Exhibition.query.all()
  activeExhibitions = []
  activeDeinstalls = []
  upcomingExhibitions = []
  return render_template('exhibitions.html', exhibitions = exhibitions)


@app.route('/exhibitions/<int:exhibition_id>')
def exhibition(exhibition_id):
  exhibition = Exhibition.query.filter_by(id = exhibition_id).one()
  exhib = Exh_art_park.query.filter_by(exhibition_id = exhibition_id).all()
  return render_template('exhibition.html', exhibition = exhibition, exhib = exhib)


@app.route('/parks')
def parks():
  parks = Park.query.all()
  activeParks = []
  return render_template('parks.html', parks = parks)


@app.route('/parks/<int:park_id>')
def park(park_id):
  park = Park.query.filter_by(id=park_id).one()
  park_art = Exh_art_park.query.filter_by(park_id = park_id).all()
  return render_template('park.html', park = park, park_art = park_art)


@app.route('/artists')
def artists():
  artists = Artist.query.all()
  return render_template('artists.html', artists = artists)


@app.route('/artists/<int:artist_id>')
def artist(artist_id):
  artist = Artist.query.filter_by(id = artist_id).one()
  artworks = Artwork.query.all()
  return render_template('artist.html', artist = artist, artworks = artworks)


@app.route('/artists/<int:artist_id>/edit', methods=['GET', 'POST'])
def artist_edit(artist_id):
  artist = Artist.query.filter_by(id=artist_id).one()
  if request.method == 'POST':
    # Update artist items
    artist.pName = request.form['pName']
    artist.fName = request.form['fName']
    artist.email = request.form['email']
    artist.phone = request.form['phone']
    artist.website = request.form['website']
    try:
      # Clear artist artworks
      artist.artworks = []
      artist_art = request.form.getlist('artworks')
      # Remove any empty form items from artworks list
      artist_art = filter(None, artist_art)
      # Add latest artworks to artist, removing duplicates
      for x in list(set(artist_art)):
        artwork = Artwork.query.filter_by(id = x).one()
        artist.artworks.append(artwork)
    except Exception as e:
      raise e
    db.session.add(artist)
    db.session.commit()
  # Return message/error via AJAX?
  return redirect(url_for('artist', artist_id = artist.id))


@app.route('/artworks')
def artworks():
  artworks = Artwork.query.all()
  return render_template('artworks.html', artworks = artworks)


@app.route('/artworks/<int:artwork_id>')
def artwork(artwork_id):
  artwork = Artwork.query.filter_by(id=artwork_id).one()
  return render_template('artwork.html', artwork = artwork)


@app.route('/organizations')
def orgs():
  orgs = Org.query.all()
  return render_template('orgs.html', orgs = orgs)


@app.route('/organizations/<int:organization_id>')
def org(organization_id):
  org = Org.query.filter_by(id=organization_id).one()
  return render_template('org.html', org = org)