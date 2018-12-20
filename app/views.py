#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from flask import (
  Flask,
  render_template,
  request,
  redirect,
  url_for,
  jsonify,
  session
)
from flask_sqlalchemy import SQLAlchemy

from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.urls import url_parse

from flask_login import (
  LoginManager,
  UserMixin,
  login_user,
  login_required,
  logout_user,
  current_user
)

from app import app, db
from parks_db import Exh_art_park, Exhibition, Park, Artwork, Artist, Org
from forms import (
  Form_artist,
  Form_exhibition,
  Form_artwork,
  Form_park,
  Form_org,
  Form_user,
  Form_signup
)
from users import User

import sys
from datetime import datetime

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"
login_manager.login_view = 'login'



@login_manager.user_loader
def load_user(user_id):
  return User.query.get(user_id)

@app.template_filter('date_format')
def date_format(value, format='%m/%d/%y'):
  return value.strftime(format)

today = datetime.utcnow().strftime('%Y-%m-%d')

@app.route('/home')
@app.route('/index')
@app.route('/')
def home():
  active_exhibitions = Exhibition.query.filter(Exhibition.end_date > today)\
                                       .filter(Exhibition.start_date < today)\
                                       .order_by(Exhibition.end_date)\
                                       .all()
  upcoming_exhibitions = Exhibition.query.filter(Exhibition.start_date > today)\
                                         .order_by(Exhibition.start_date)\
                                         .limit(10)\
                                         .all()
  recent_exhibitions = Exhibition.query.filter(Exhibition.end_date <= today)\
                                         .order_by(Exhibition.end_date.desc())\
                                         .limit(10)\
                                         .all()
  exhibitions = Exhibition.query.all()
  session['url'] = request.path
  return render_template('index.html', exhibitions=exhibitions, parks=parks,
    active_exhibitions = active_exhibitions,
    upcoming_exhibitions = upcoming_exhibitions,
    recent_exhibitions = recent_exhibitions)


@app.route('/login', methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('home'))
  form = Form_user()
  if form.validate_on_submit():
    user = User.query.filter_by(username = form.username.data).one()
    if user:
      if check_password_hash(user.password, form.password.data):
        login_user(user, remember = form.remember.data)
        next = request.args.get('next')
        if not next or url_parse(next).netloc != '':
          next = session['url']
          return redirect(next)
      # FUTURE: Return error notice for invalid username/password

  return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
  logout_user()
  return 'You are now logged out!'


@app.route('/signup', methods=['GET', 'POST'])
def signup():
  form = Form_signup()

  if form.is_submitted():
    if form.validate():
      hashed_password = generate_password_hash(form.password.data, method='sha256')
      new_user = User(username=form.username.data, password=hashed_password)
      db.session.add(new_user)
      db.session.commit()
      return jsonify({"success": True, "data": {"Signup": "User created!"}})

    else:
      return jsonify({"success": False, "data": form.errors})

  return render_template('signup.html', form=form)



# Route: Create database items
@app.route('/create', methods=['GET'])
@login_required
def create():
  # Query object classes
  artists = Artist.query.all()
  artworks = Artwork.query.all()
  parks = Park.query.all()
  orgs = Org.query.all()

  # Define form classes
  form_artist = Form_artist()
  form_artwork = Form_artwork()
  form_park = Form_park()
  form_exhibition = Form_exhibition()
  form_org = Form_org()

  return render_template('create.html',
    artworks = artworks, parks = parks, orgs = orgs, artists = artists,
    form_artist = form_artist, form_artwork = form_artwork,
    form_park = form_park, form_exhibition = form_exhibition,
    form_org = form_org)


@app.route('/exhibitions')
def exhibitions():
  exhibitions = Exhibition.query.all()
  active_exhibitions = Exhibition.query.filter(Exhibition.end_date > today)\
                                       .filter(Exhibition.start_date < today)\
                                       .order_by(Exhibition.end_date)\
                                       .all()
  upcoming_exhibitions = Exhibition.query.filter(Exhibition.start_date > today)\
                                         .order_by(Exhibition.start_date)\
                                         .limit(10)\
                                         .all()
  recent_exhibitions = Exhibition.query.filter(Exhibition.end_date <= today)\
                                         .order_by(Exhibition.end_date.desc())\
                                         .limit(10)\
                                         .all()
  session['url'] = request.path
  return render_template('exhibitions.html', exhibitions = exhibitions,
    active_exhibitions = active_exhibitions,
    upcoming_exhibitions = upcoming_exhibitions,
    recent_exhibitions = recent_exhibitions)


@app.route('/exhibitions/<int:exhibition_id>')
def exhibition(exhibition_id):
  exhibition = Exhibition.query.filter_by(id = exhibition_id).one()
  artworks = Artwork.query.all()
  parks = Park.query.all()
  orgs = Org.query.all()
  exhib = Exh_art_park.query.filter_by(exhibition_id = exhibition_id).all()
  form = Form_exhibition()
  session['url'] = request.path
  return render_template('exhibition.html', exhibition = exhibition,
                         exhib = exhib, artworks = artworks, parks = parks,
                         orgs = orgs, form = form)


@app.route('/exhibitions/create', methods=['POST'])
@login_required
def exhibition_create():
  form = Form_exhibition()
  if form.validate_on_submit():
    # Update exhibition items
    exhibition = Exhibition()
    # Add form items

    print "Form data: {}".format(jsonify(form.data))

    # Bio
    exhibition.name = form.name.data
    exhibition.start_date = form.start_date.data
    exhibition.end_date = form.end_date.data
    exhibition.opening = form.opening.data
    exhibition.comments = form.comments.data

    # Install
    exhibition.install_start = form.install_start.data
    exhibition.install_end = form.install_end.data
    exhibition.prm = form.prm.data
    exhibition.approval = form.approval.data
    exhibition.walkthrough = form.walkthrough.data
    exhibition.cb_presentation = form.cb_presentation.data
    exhibition.license_mailed = form.license_mailed.data
    exhibition.license_signed = form.license_signed.data
    exhibition.license_borough = form.license_borough.data
    exhibition.bond = form.bond.data
    exhibition.coi = form.coi.data
    exhibition.coi_renewal = form.coi_renewal.data
    exhibition.signage_submit = form.signage_submit.data
    exhibition.signage_received = form.signage_received.data
    exhibition.press_draft = form.press_draft.data
    exhibition.press_approved = form.press_approved.data
    exhibition.web_text = form.web_text.data
    exhibition.work_images = form.work_images.data

    # De-Install
    exhibition.deinstall_date = form.deinstall_date.data
    exhibition.deinstall_check = form.deinstall_check.data
    exhibition.bond_return = form.bond_return.data
    exhibition.press_clippings = form.press_clippings.data

    # Get org child list data
    orgs = filter(None, form.orgs.data)

    for item in list(set(orgs)):
      try:
        org = Org.query.filter_by(name = item).one()
        exhibition.organizations.append(org)
        print "Added {} org to {}".format(org.name, exhibition.name)
      except Exception as e:
        db.session.rollback()
        return jsonify({
                        "success": False,
                        "data": {
                          "Organizations": "{} isn’t a recognized\
                                            organization. Add it to the\
                                            database!".format(item)}})

    # Add exhibition to database
    db.session.add(exhibition)
    # Flush session to get and use exhibition ID
    db.session.flush()

    # Get artworks/parks child list data
    artworks = filter(None, form.artworks.data)
    parks = filter(None, form.parks.data)

    # Add artwork/park children to Exh_art_park table if numbers are equal
    if len(parks) == len(artworks):
      for x, y in zip(artworks, parks):
        # Check if artwork is in database
        try:
          artwork = Artwork.query.filter_by(name = x).one()
          print "!!!ARTWORK FOUND!: {}".format(artwork.name)
        except Exception as e:
          db.session.rollback()
          # Return error if artwork not found
          return jsonify({
                          "success": False,
                          "data": {
                            "Artworks": "{} isn’t a recognized artwork. Add it\
                                         to the database!".format(x)}})
        # Check if park is in database
        try:
          park = Park.query.filter_by(name = y).one()
          print "!!!PARK FOUND!: {}".format(park.name)
        except Exception as e:
          db.session.rollback()
          # Return error if artwork not found
          return jsonify({
                          "success": False,
                          "data": {
                            "Artworks": "{} isn’t a recognized park. Add it to\
                                         the database!".format(y)}})
        # Add unique exhibition/artwork/park to database
        try:
          exh_rel = Exh_art_park(exhibition_id = exhibition.id,
                               artwork_id = artwork.id,
                               park_id = park.id)
          db.session.add(exh_rel)
        except Exception as e:
          db.session.rollback()
          # Return error if exhibition/artwork/park can't be added
          return jsonify({"success": False,
                          "data": {
                            "Artworks": str(e)}})
    # Return error if exhibitions and artworks count is uneven
    else:
      db.session.rollback()
      return jsonify({"success": False,
                      "data": {
                        "Artworks": "There’s an uneven number of artworks and\
                                     parks. This data needs to be complete."}})

    db.session.commit()
    # Return success message, exhibition object via AJAX
    return jsonify({"success": True, "data": exhibition.serialize})
  else:
    # Return errors if form doesn't validate
    return jsonify({"success": False, "data": form.errors})


@app.route('/exhibitions/<int:exhibition_id>/edit', methods=['GET', 'POST'])
@login_required
def exhibition_edit(exhibition_id):
  exhibition = Exhibition.query.filter_by(id=exhibition_id).one()
  form = Form_exhibition()
  if form.validate_on_submit():
    # Update exhibition items
    # Bio
    exhibition.name = form.name.data
    exhibition.start_date = form.start_date.data
    exhibition.end_date = form.end_date.data
    exhibition.opening = form.opening.data
    exhibition.comments = form.comments.data

    # Install
    exhibition.install_start = form.install_start.data
    exhibition.install_end = form.install_end.data
    exhibition.prm = form.prm.data
    exhibition.approval = form.approval.data
    exhibition.walkthrough = form.walkthrough.data
    exhibition.cb_presentation = form.cb_presentation.data
    exhibition.license_mailed = form.license_mailed.data
    exhibition.license_signed = form.license_signed.data
    exhibition.license_borough = form.license_borough.data
    exhibition.bond = form.bond.data
    exhibition.coi = form.coi.data
    exhibition.coi_renewal = form.coi_renewal.data
    exhibition.signage_submit = form.signage_submit.data
    exhibition.signage_received = form.signage_received.data
    exhibition.press_draft = form.press_draft.data
    exhibition.press_approved = form.press_approved.data
    exhibition.web_text = form.web_text.data
    exhibition.work_images = form.work_images.data

    # De-Install
    exhibition.deinstall_date = form.deinstall_date.data
    exhibition.deinstall_check = form.deinstall_check.data
    exhibition.bond_return = form.bond_return.data
    exhibition.press_clippings = form.press_clippings.data

    # Get org child list data
    orgs = filter(None, form.orgs.data)
    # Clear organizations 1-to-many relationships
    exhibition.organizations = []

    for item in list(set(orgs)):
      try:
        org = Org.query.filter_by(name = item).one()
        exhibition.organizations.append(org)
        print "Added {} org to {}".format(org.name, exhibition.name)
      except Exception as e:
        db.session.rollback()
        return jsonify({
                        "success": False,
                        "data": {
                          "Organizations": "{} isn’t a recognized\
                                            organization. Add it to the\
                                            database!".format(item)}})

    # Get artworks/parks child list data
    artworks = filter(None, form.artworks.data)
    parks = filter(None, form.parks.data)

    # Add artwork/park children to Exh_art_park table if numbers are equal
    if len(parks) == len(artworks):
      # Clear exhibitions/artworks 1-to-many relationships
      exhibition.artworks = []
      exhibition.parks = []

      for x, y in zip(artworks, parks):
        # Check if artwork is in database
        try:
          artwork = Artwork.query.filter_by(name = x).one()
          print "!!!ARTWORK FOUND!: {}".format(artwork.name)
        except Exception as e:
          db.session.rollback()
          # Return error if artwork not found
          return jsonify({
                          "success": False,
                          "data": {
                            "Artworks": "{} isn’t a recognized artwork. Add\
                                            it to the database!".format(x)}})
        # Check if park is in database
        try:
          park = Park.query.filter_by(name = y).one()
          print "!!!PARK FOUND!: {}".format(park.name)
        except Exception as e:
          db.session.rollback()
          # Return error if artwork not found
          return jsonify({
                          "success": False,
                          "data": {
                            "Artworks": "{} isn’t a recognized park. Add\
                                            it to the database!".format(y)}})
        # Add unique exhibition/artwork/park to database
        try:
          exh_rel = Exh_art_park(exhibition_id = exhibition.id,
                               artwork_id = artwork.id,
                               park_id = park.id)
          db.session.add(exh_rel)
        except Exception as e:
          db.session.rollback()
          # Return error if exhibition/artwork/park can't be added
          return jsonify({"success": False,
                          "data": {
                            "Artworks": str(e)}})
    # Return error if exhibitions and artworks count is uneven
    else:
      db.session.rollback()
      return jsonify({"success": False,
                      "data": {
                        "Artworks": "There’s an uneven number of\
                                        artworks and parks. This data\
                                         needs to be complete."}})

    # Add exhibition to database if we made it this far
    db.session.add(exhibition)
    db.session.commit()
    # Return success message, exhibition object via AJAX
    return jsonify({"success": True, "data": exhibition.serialize})
  else:
    # Return errors if form doesn't validate
    return jsonify({"success": False, "data": form.errors})


@app.route('/exhibitions/<int:exhibition_id>/delete', methods=['GET', 'POST'])
@login_required
def exhibition_delete(exhibition_id):
  exhibition = Exhibition.query.filter_by(id=exhibition_id).one()
  form = Form_exhibition()
  if request.method == 'POST':
      db.session.delete(exhibition)
      db.session.commit()
      return redirect(url_for('exhibitions'))
  else:
      return render_template('exhibition_delete.html', exhibition = exhibition,
                             form = form)


@app.route('/parks')
def parks():
  parks = Park.query.all()
  active_parks = db.session.query(Exh_art_park, Exhibition, Park)\
    .filter(Exh_art_park.exhibition_id == Exhibition.id)\
    .filter(Exh_art_park.park_id == Park.id)\
    .filter(Exhibition.end_date > today)\
    .filter(Exhibition.start_date < today)\
    .order_by(Park.name)\
    .all()
  session['url'] = request.path
  return render_template('parks.html', parks = parks,
    active_parks = active_parks)


@app.route('/parks/<int:park_id>')
def park(park_id):
  park = Park.query.filter_by(id=park_id).one()
  exhibitions = Exhibition.query.all()
  artworks = Artwork.query.all()
  form = Form_park()
  # Set default select item to current park borough
  form.borough.data = park.borough
  park_art = Exh_art_park.query.filter_by(park_id = park_id)\
                               .order_by(Exh_art_park.exhibition_id).all()
  session['url'] = request.path
  return render_template('park.html', park = park, exhibitions = exhibitions,
                         artworks = artworks, park_art = park_art, form = form)


@app.route('/parks/create', methods=['POST'])
@login_required
def park_create():
  form = Form_park()
  if form.validate_on_submit():
    # Create park
    park = Park()
    # Add form items
    park.name = form.name.data
    park.park_id = form.park_id.data
    park.borough = form.borough.data
    park.address = form.address.data
    park.cb = form.cb.data

    # Add park to database
    db.session.add(park)
    db.session.commit()
    # Return success message, park object via AJAX
    return jsonify({"success": True, "data": park.serialize})
  else:
    # Return errors if form doesn't validate
    return jsonify({"success": False, "data": form.errors})


@app.route('/parks/<int:park_id>/edit', methods=['POST'])
@login_required
def park_edit(park_id):
  park = Park.query.filter_by(id = park_id).one()
  form = Form_park()
  if form.validate_on_submit():
    # Update form items
    park.name = form.name.data
    park.park_id = form.park_id.data
    park.borough = form.borough.data
    park.address = form.address.data
    park.cb = form.cb.data

    # Get child list data
    exhibitions = filter(None, form.exhibitions.data)
    artworks = filter(None, form.artworks.data)
    # Add artwork/park children to Exh_art_park table if numbers are equal
    if len(exhibitions) == len(artworks):
      # Clear exhibitions/artworks 1-to-many relationships
      park.exhibitions = []
      park.artworks = []

      # Loop through arrays and add to database
      for x, y in zip(exhibitions, artworks):
        try:
          exhibition = Exhibition.query.filter_by(name = x).one()
          print "!!!EXHIBITION FOUND!: {}".format(exhibition.name)
        except Exception as e:
          db.session.rollback()
          # Return error if exhibition not found
          return jsonify({
                          "success": False,
                          "data": {
                            "Exhibitions": "{} isn’t a recognized exhibition.\
                                            Add it to the database!".format(y)}
                        })

        try:
          artwork = Artwork.query.filter_by(name = y).one()
          print "!!!ARTWORK FOUND!: {}".format(artwork.name)
        except Exception as e:
          db.session.rollback()
          # Return error if artwork not found
          return jsonify({
                          "success": False,
                          "data": {
                            "Exhibitions": "{} isn’t a recognized artwork. Add\
                                            it to the database!".format(y)}})

        try:
          exh_rel = Exh_art_park(exhibition_id = exhibition.id,
                                 artwork_id = artwork.id,
                                 park_id = park.id)
          db.session.add(exh_rel)
        except Exception as e:
          db.session.rollback()
          # Return error if exhibition/artwork/park can't be added to database
          return jsonify({"success": False,
                          "data": {
                            "Exhibitions": str(e)}})

    else:
      db.session.rollback()
      # Return error if exhibitions and artworks count is uneven
      return jsonify({"success": False,
                      "data": {
                        "Exhibitions": "There’s an uneven number of\
                                        exhibitions and artworks. This data\
                                         needs to be complete."}})

    # Update park data to database
    db.session.add(park)
    db.session.commit()
    # Return success message, park object via AJAX
    return jsonify({"success": True, "data": park.serialize})
  else:
    # Return errors if form doesn't validate
    return jsonify({"success": False, "data": form.errors})


@app.route('/parks/<int:park_id>/delete', methods=['GET', 'POST'])
@login_required
def park_delete(park_id):
  park = Park.query.filter_by(id=park_id).one()
  form = Form_park()
  if request.method == 'POST':
      db.session.delete(park)
      db.session.commit()
      return redirect(url_for('parks'))
  else:
      return render_template('park_delete.html', park = park, form = form)


@app.route('/artists')
def artists():
  artists = Artist.query.all()
  session['url'] = request.path
  return render_template('artists.html', artists = artists)


@app.route('/artists/<int:artist_id>')
def artist(artist_id):
  artist = Artist.query.filter_by(id = artist_id).one()
  artworks = Artwork.query.all()

  form = Form_artist()
  # artist_join = (db.session.query(Artist, Exh_art_park, Artwork, Park)
  #   .filter(Exh_art_park.artwork_id == Artwork.id)
  #   .filter(Artist.id == artist_id)).all()
  # for i in artist_join:
  #   print "ARTIST: {}: {}".format(i.Artist.id, i.Artist.name)
  #   print "ARTWORK: {}: {}".format(i.Artwork.id, i.Artwork.name)
  #   print "EXH: {}: {}".format(i.Exh_art_park.exhibition_id, i.Exh_art_park.exhib.name)
  #   print "PARK: {}: {}".format(i.Park.id, i.Park.name)
  session['url'] = request.path
  return render_template('artist.html', artist = artist, artworks = artworks,
                         form = form)


@app.route('/artists/create', methods=['GET', 'POST'])
@login_required
def artist_create():
  pass
  form = Form_artist()
  if form.validate_on_submit():
    # Create artist
    artist = Artist()
    # Add form items
    artist.pName = form.pName.data
    artist.fName = form.fName.data
    artist.email = form.email.data
    artist.phone = form.phone.data
    artist.website = form.website.data

    # Add artists to 1-to-many relationship
    # Clear artist.artworks
    artist.artworks = []
    # Get list of artworks, removing empty form items
    artworks = filter(None, form.artworks.data)
    # Add latest artworks to artist, removing duplicates
    try:
      # Add latest artworks to artist, removing duplicates
      for item in list(set(artworks)):
        artwork = Artwork.query.filter_by(name = item).one()
        artist.artworks.append(artwork)
        # Add artwork to database
        print "Added {} to {}".format(artwork.name, artist.name)
    except:
      db.session.rollback()
      return jsonify({
                      "success": False,
                      "data": {
                        "Artworks": "{} isn’t a recognized artwork. Add it to\
                                     the database!".format(item)}})

    # Add artist to database
    db.session.add(artist)
    db.session.commit()
    # Return success message, artist object via AJAX
    return jsonify({"success": True, "data": artist.serialize})
  else:
    # Return errors if form doesn't validate
    return jsonify({"success": False, "data": form.errors})


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
@login_required
def artist_edit(artist_id):
  artist = Artist.query.filter_by(id=artist_id).one()
  form = Form_artist()

  if form.validate_on_submit():
    # Update artist items
    artist.pName = form.pName.data
    artist.fName = form.fName.data
    artist.email = form.email.data
    artist.phone = form.phone.data
    artist.website = form.website.data

    # Add artworks to 1-to-many relationship
    # Clear artist.artworks
    artist.artworks = []
    # Get list of artworks, removing empty form items
    artworks = filter(None, form.artworks.data)
    # Add latest artworks to artist, removing duplicates
    try:
      # Add latest artworks to artist, removing duplicates
      for item in list(set(artworks)):
        artwork = Artwork.query.filter_by(name = item).one()
        artist.artworks.append(artwork)
        # Add artwork to database
        print "Added {} to {}".format(artwork.name, artist.name)
    except:
      db.session.rollback()
      return jsonify({
                      "success": False,
                      "data": {
                        "Artworks": "{} isn’t a recognized artwork. Add it to\
                                          the database!".format(item)}})

    db.session.add(artist)
    db.session.commit()
    # Return success message, artist object via AJAX
    return jsonify({"success": True, "data": artist.serialize})
  else:
    # Return errors if form doesn't validate
    return jsonify({"success": False, "data": form.errors})


@app.route('/artists/<int:artist_id>/delete', methods=['GET', 'POST'])
@login_required
def artist_delete(artist_id):
  artist = Artist.query.filter_by(id=artist_id).one()
  form = Form_artist()
  if request.method == 'POST':
      db.session.delete(artist)
      db.session.commit()
      return redirect(url_for('artists'))
  else:
      return render_template('artist_delete.html', artist = artist, form = form)


@app.route('/artworks')
def artworks():
  artworks = Artwork.query.all()
  active_artworks = db.session.query(Exh_art_park, Exhibition, Artwork)\
      .filter(Exh_art_park.exhibition_id == Exhibition.id)\
      .filter(Exh_art_park.artwork_id == Artwork.id)\
      .filter(Exhibition.end_date > today)\
      .filter(Exhibition.start_date < today)\
      .order_by(Exhibition.name)\
      .order_by(Artwork.name)\
      .all()
  session['url'] = request.path
  return render_template('artworks.html', artworks = artworks,
    active_artworks = active_artworks)


@app.route('/artworks/<int:artwork_id>')
def artwork(artwork_id):
  artwork = Artwork.query.filter_by(id=artwork_id).one()
  artists = Artist.query.all()
  exhibitions = Exhibition.query.all()
  parks = Park.query.all()
  form = Form_artwork()
  art_exhib = Exh_art_park.query.filter_by(artwork_id = artwork_id).all()
  # artwork_join = (db.session.query(Exh_art_park, Artwork)
  #   .filter(Exh_art_park.artwork_id == Artwork.id)
  #   .filter(Artwork.id == artwork_id)).all()
  session['url'] = request.path
  return render_template('artwork.html', artwork = artwork, artists = artists,
                         exhibitions = exhibitions, parks = parks,
                         art_exhib = art_exhib, form = form)


@app.route('/artworks/create', methods=['POST'])
@login_required
def artwork_create():
  form = Form_artwork()
  if form.validate_on_submit():
    # Create artwork
    artwork = Artwork()
    # Add form items
    artwork.name = form.name.data

    # Add artists to 1-to-many relationship
    # Get artists child list data, remove empty data
    artists = filter(None, form.artists.data)
    # Add artists to artwork, removing duplicates
    for item in list(set(artists)):
      try:
        artist = Artist.query.filter_by(name = item).one()
        artwork.artists.append(artist)
        print "Added {} to {}".format(artist.name, artwork.name)
        # Add artwork to database
      except:
        db.session.rollback()
        # Return database exception(s)
        return jsonify({
                        "success": False,
                        "data": {
                          "Artists": "{} isn’t a recognized artist. Add them\
                                      to the database!".format(item)}})

    db.session.add(artwork)
    db.session.commit()
    # Return success message, artwork object via AJAX
    return jsonify({"success": True, "data": artwork.serialize})
  else:
    # Return errors if form doesn't validate
    return jsonify({"success": False, "data": form.errors})


@app.route('/artworks/<int:artwork_id>/edit', methods=['POST'])
@login_required
def artwork_edit(artwork_id):
  artwork = Artwork.query.filter_by(id=artwork_id).one()
  form = Form_artwork()
  if form.validate_on_submit():
    # Update artwork items
    artwork.name = form.name.data

    # Add artists to 1-to-many relationship
    artwork.artists = []
    # Get artists child list data, remove empty data
    artists = filter(None, form.artists.data)
    # Add artists to artwork, removing duplicates
    for item in list(set(artists)):
      try:
        artist = Artist.query.filter_by(name = item).one()
        artwork.artists.append(artist)
        print "Added {} to {}".format(artist.name, artwork.name)
        # Add artwork to database
      except Exception as e:
        db.session.rollback()
        # Return database exception(s)
        return jsonify({
                        "success": False,
                        "data": {
                          "Artists": "{} isn’t a recognized artist. Add them\
                                      to the database!".format(item)}})

    # Get artworks/parks child list data
    exhibitions = filter(None, form.exhibitions.data)
    parks = filter(None, form.parks.data)

    # Add exhibition/park children to Exh_art_park table if numbers are equal
    if len(parks) == len(exhibitions):
      # Clear exhibitions/parks 1-to-many relationships
      artwork.exhibitions = []
      artwork.parks = []

      for x, y in zip(exhibitions, parks):
        # Check if exhibition is in database
        try:
          exhibition = Exhibition.query.filter_by(name = x).one()
          print "!!!EXHIBITION FOUND!: {}".format(exhibition.name)
        except Exception as e:
          db.session.rollback()
          # Return error if exhibition not found
          return jsonify({
                          "success": False,
                          "data": {
                            "Exhibitions": "{} isn’t a recognized exhibition.\
                                            Add it to the database!".format(x)}})
        # Check if park is in database
        try:
          park = Park.query.filter_by(name = y).one()
          print "!!!PARK FOUND!: {}".format(park.name)
        except Exception as e:
          db.session.rollback()
          # Return error if artwork not found
          return jsonify({
                          "success": False,
                          "data": {
                            "Exhibitions": "{} isn’t a recognized park. Add\
                                            it to the database!".format(y)}})
        # Add unique exhibition/artwork/park to database
        try:
          exh_rel = Exh_art_park(exhibition_id = exhibition.id,
                                 artwork_id = artwork.id,
                                 park_id = park.id)
          db.session.add(exh_rel)
        except Exception as e:
          db.session.rollback()
          # Return error if exhibition/artwork/park can't be added
          return jsonify({"success": False,
                          "data": {
                            "Exhibitions": str(e)}})
    # Return error if exhibitions and artworks count is uneven
    else:
      db.session.rollback()
      return jsonify({"success": False,
                      "data": {
                        "Exhibitions": "There’s an uneven number of exhibitions\
                                        and parks. This data needs to be\
                                        complete."}})

    # Add artwork and commit database records if we've made it this far
    db.session.add(artwork)
    db.session.commit()
    # Return success message, artwork object via AJAX
    return jsonify({"success": True, "data": artwork.serialize})
  else:
    # Return errors if form doesn't validate
    return jsonify({"success": False, "data": form.errors})


@app.route('/artworks/<int:artwork_id>/delete', methods=['GET', 'POST'])
@login_required
def artwork_delete(artwork_id):
  artwork = Artwork.query.filter_by(id=artwork_id).one()
  form = Form_artwork()
  if request.method == 'POST':
      db.session.delete(artwork)
      db.session.commit()
      return redirect(url_for('artworks'))
  else:
      return render_template('artwork_delete.html', artwork = artwork,
                             form = form)


@app.route('/orgs')
def orgs():
  orgs = Org.query.all()
  session['url'] = request.path
  return render_template('orgs.html', orgs = orgs)


@app.route('/orgs/<int:org_id>')
def org(org_id):
  org = Org.query.filter_by(id=org_id).one()
  exhibitions = Exhibition.query.all()
  form = Form_org()
  for exh in org.exhibitions:
    form.exhibitions.append_entry(exh)
  session['url'] = request.path
  return render_template('org.html', org = org, exhibitions = exhibitions,
                         form = form)


@app.route('/orgs/create', methods=['POST'])
@login_required
def org_create():
  form = Form_org()

  if form.validate_on_submit():
    # Create organization
    org = Org()
    # Add form items
    org.name = form.name.data
    org.phone = form.phone.data
    org.website = form.website.data

    # Add exhibitions to 1-to-many relationship
    # Get list of exhibitions, removing empty form items
    exhibitions = filter(None, form.exhibitions.data)
    # Add latest exhibitions to org, removing duplicates
    for item in list(set(exhibitions)):
      try:
        exhibition = Exhibition.query.filter_by(name = item).one()
        org.exhibitions.append(exhibition)
        # Add org to database
        print "Added {} exhibition to {}".format(exhibition.name, org.name)
      except:
        db.session.rollback()
        return jsonify({
                        "success": False,
                        "data": {
                          "Exhibitions": "{} isn’t a recognized\
                                            exhibition. Add it to the\
                                            database!".format(item)}})
    # Add org to database
    db.session.add(org)
    db.session.commit()
    # Return success message, org object via AJAX
    return jsonify({"success": True, "data": org.serialize})

  else:
    # Return errors if form doesn't validate
    return jsonify({"success": False, "data": form.errors})


@app.route('/orgs/<int:org_id>/edit', methods=['POST'])
@login_required
def org_edit(org_id):
  org = Org.query.filter_by(id=org_id).one()
  form = Form_org()

  if form.validate_on_submit():
    # Update org items
    org.name = form.name.data
    org.phone = form.phone.data
    org.website = form.website.data

    # Add exhibitions to 1-to-many relationship
    # Clear org exhibitions
    org.exhibitions = []
    # Get list of exhibitions, removing empty form items
    exhibitions = filter(None, form.exhibitions.data)
    # Add latest exhibitions to org, removing duplicates
    for item in list(set(exhibitions)):
      try:
        exhibition = Exhibition.query.filter_by(name = item).one()
        org.exhibitions.append(exhibition)
        # Add org to database
        print "Added {} exhibition to {}".format(exhibition.name, org.name)
      except:
        db.session.rollback()
        return jsonify({
                        "success": False,
                        "data": {
                          "Exhibitions": "{} isn’t a recognized\
                                            exhibition. Add it to the\
                                            database!".format(item)}})

    db.session.add(org)
    db.session.commit()
    # Return success message, org object via AJAX
    return jsonify({"success": True, "data": org.serialize})

  else:
    # Return errors if form doesn't validate
    return jsonify({"success": False, "data": form.errors})


@app.route('/orgs/<int:org_id>/delete', methods=['GET', 'POST'])
@login_required
def org_delete(org_id):
  org = Org.query.filter_by(id=org_id).one()
  form = Form_org()
  if request.method == 'POST':
      db.session.delete(org)
      db.session.commit()
      return redirect(url_for('orgs'))
  else:
      return render_template('org_delete.html', org = org, form = form)
