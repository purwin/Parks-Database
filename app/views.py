from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

from app import app, db
from parks_db import Exh_art_park, Exhibition, Park, Artwork, Artist, Org
from forms import Form_artist, Form_exhibition, Form_artwork, Form_park, Form_org

from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

import sys

@app.route('/home')
@app.route('/index')
@app.route('/')
def home():
  todayItems = []
  activeExhibitions = []
  upcomingItems = []
  exhibitions = Exhibition.query.all()
  parks = Park.query.all()
  return render_template('index.html', exhibitions=exhibitions, parks=parks)


@app.template_filter('date_format')
def date_format(value, format='%m/%d/%y'):
  return value.strftime(format)


# Route: Create database items
@app.route('/create', methods=['GET'])
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
  activeExhibitions = []
  activeDeinstalls = []
  upcomingExhibitions = []
  return render_template('exhibitions.html', exhibitions = exhibitions)


@app.route('/exhibitions/<int:exhibition_id>')
def exhibition(exhibition_id):
  exhibition = Exhibition.query.filter_by(id = exhibition_id).one()
  exhib = Exh_art_park.query.filter_by(exhibition_id = exhibition_id).all()
  exhibition = Exhibition.query.filter_by(id = exhibition_id).one()
  artworks = Artwork.query.all()
  parks = Park.query.all()
  form = Form_exhibition()
  return render_template('exhibition.html', exhibition = exhibition,
                         exhib = exhib, artworks = artworks, parks = parks,
                         form = form)


@app.route('/exhibitions/create', methods=['POST'])
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

    # Add exhibition to database
    db.session.add(exhibition)
    # Flush session to get and use exhibition ID
    db.session.flush()

    # Add artwork/park children to Exh_art_park table
    artworks = filter(None, form.artworks.data)
    parks = filter(None, form.parks.data)

    if len(artworks) == len(parks):
      try:
        for x, y in zip(artworks, parks):
          exh_art_park = Exh_art_park(exhibition_id = exhibition.id,
                                      artwork_id = x, park_id = y)
          db.session.add(exh_art_park)
      except Exception as e:
        raise e

    print "ORGS DATA: {}".format(form.orgs.data)
    # Add exhibition.orgs children
    orgs = filter(None, form.orgs.data)
    print "ORGS: {}".format(orgs)
    for item in list(set(orgs)):
      org = Org.query.filter_by(id = item).one()
      print "Adding {} to {}".format(org.name, exhibition.name)
      exhibition.organizations.append(org)

    db.session.commit()
    # Return success message, exhibition object via AJAX
    return jsonify({"success": True, "data": exhibition.serialize})
  else:
    # Return errors if form doesn't validate
    return jsonify({"success": False, "data": form.errors})


@app.route('/exhibitions/<int:exhibition_id>/edit', methods=['GET', 'POST'])
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

    try:
      # Clear artist artworks
      # artist.artworks = []
      # artist_art = request.form.getlist('artworks')
      # Remove any empty form items from artworks list
      # artist_art = filter(None, artist_art)
      # Add latest artworks to artist, removing duplicates
      # for x in list(set(artist_art)):
      #   artwork = Artwork.query.filter_by(id = x).one()
      #   artist.artworks.append(artwork)

      exhibition.artworks = []
      exhibition.parks = []

      parks = filter(None, form.parks.data)
      artworks = filter(None, form.artworks.data)
      for x, y in zip(artworks, parks):
        # add exhibition, art, park ref to database
        artwork = Artwork.query.filter_by(name = x).one()
        park = Park.query.filter_by(name = y).one()
        exh_rel = Exh_art_park(exhibition_id=exhibition.id, artwork_id=artwork.id, park_id=park.id)
        db.session.add(exh_rel)
    except Exception as e:
      # Return database exception(s)
      return jsonify({"success": False, "data": e})
    db.session.add(exhibition)
    db.session.commit()
    # Return success message, exhibition object via AJAX
    return jsonify({"success": True, "data": exhibition.serialize})
  else:
    # Return errors if form doesn't validate
    return jsonify({"success": False, "data": form.errors})


@app.route('/exhibitions/<int:exhibition_id>/delete', methods=['GET', 'POST'])
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
  activeParks = []
  return render_template('parks.html', parks = parks)


@app.route('/parks/<int:park_id>')
def park(park_id):
  park = Park.query.filter_by(id=park_id).one()
  exhibitions = Exhibition.query.all()
  artworks = Artwork.query.all()
  form = Form_park()
  form.borough.data = park.borough
  # for exhibition in form.exhibitions:
  #   form.exhibitions.append_entry(exhibition)
  # for artwork in form.artworks:
  #   form.artworks.append_entry(artwork)

  # park_exh = (db.session.query(Exh_art_park, Park)
  #   .filter(Exh_art_park.park_id == Park.id)
  #   .filter(Park.id == park_id)).all()
  park_exh = Exh_art_park.query.filter_by(park_id = park_id)
                               .all()
                               .order_by(exhibition_id)
  return render_template('park.html', park = park, exhibitions = exhibitions,
                         artworks = artworks, park_art = form = form)


@app.route('/parks/create', methods=['POST'])
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
      artwork.exhibitions = []
      artwork.artworks = []

      # Loop through arrays and add to database
      for x, y in zip(exhibitions, artworks):
        try:
          exhibition = Exhibition.query.filter_by(name = x).one()
          print "!!!EXHIBITION FOUND!: {}".format(exhibition.name)
          artwork = Artwork.query.filter_by(name = y).one()
          print "!!!ARTWORK FOUND!: {}".format(artwork.name)
          exh_rel = Exh_art_park(exhibition_id = exhibition.id,
                                 artwork_id = artwork.id,
                                 park_id = park.id)
          db.session.add(exh_rel)
      except Exception as e:
        db.session.rollback()
        # Return errors if error is raised
        return jsonify({"success": False, "data": str(e)})

    else:
      db.session.rollback()
      # Return error if exhibitions and artworks count is uneven
      return jsonify({"success": False,
                      "data": "There's an unequal number of exhibitions and\
                               artworks. This data needs to be complete."})

    # Update park data to database
    db.session.add(park)
    db.session.commit()
    # Return success message, park object via AJAX
    return jsonify({"success": True, "data": park.serialize})
  else:
    # Return errors if form doesn't validate
    return jsonify({"success": False, "data": form.errors})


@app.route('/parks/<int:park_id>/delete', methods=['GET', 'POST'])
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
  return render_template('artists.html', artists = artists)


@app.route('/artists/<int:artist_id>')
def artist(artist_id):
  artist = Artist.query.filter_by(id = artist_id).one()
  artworks = Artwork.query.all()
  exhibitions = Exhibition.query.all()
  parks = Park.query.all()
  artist_join = (db.session.query(Artist, Exh_art_park, Artwork, Park)
    .filter(Exh_art_park.artwork_id == Artwork.id)
    .filter(Artist.id == artist_id)).all()
  form = Form_artist()
  for artwork in artist.artworks:
    form.artworks.append_entry(artwork)
  # for i in artist_join:
  #   print "ARTIST: {}: {}".format(i.Artist.id, i.Artist.name)
  #   print "ARTWORK: {}: {}".format(i.Artwork.id, i.Artwork.name)
  #   print "EXH: {}: {}".format(i.Exh_art_park.exhibition_id, i.Exh_art_park.exhib.name)
  #   print "PARK: {}: {}".format(i.Park.id, i.Park.name)
  return render_template('artist.html', artist = artist, artworks = artworks,
                         exhibitions = exhibitions, parks = parks,
                         artist_join = artist_join, form = form)


@app.route('/artists/create', methods=['GET', 'POST'])
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
    try:
      # Clear artist artworks
      artist.artworks = []
      # Remove any empty form items from artworks list
      artist_art = filter(None, form.artworks.data)
      # Add latest artworks to artist, removing duplicates
      for x in list(set(artist_art)):
        artwork = Artwork.query.filter_by(id = x).one()
        artist.artworks.append(artwork)
    except Exception as e:
      raise e
    db.session.add(artist)
    db.session.commit()
    # Return success message, artist object via AJAX
    return jsonify({"success": True, "data": artist.serialize})
  else:
    # Return errors if form doesn't validate
    return jsonify({"success": False, "data": form.errors})


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
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
    try:
      # Update artist.artworks
      artist.artworks = []
      # Remove any empty form items from artworks list
      artworks = filter(None, form.artworks.data)
      # Add latest artworks to artist, removing duplicates
      for item in list(set(artworks)):
        artwork = Artwork.query.filter_by(id = item).one()
        print "Adding {} to {}".format(artwork.name, artist.name)
        artist.artworks.append(artwork)
    except Exception as e:
      raise e
    db.session.add(artist)
    db.session.commit()
    # Return success message, artist object via AJAX
    return jsonify({"success": True, "data": artist.serialize})
  else:
    # Return errors if form doesn't validate
    return jsonify({"success": False, "data": form.errors})


@app.route('/artists/<int:artist_id>/delete', methods=['GET', 'POST'])
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
  return render_template('artworks.html', artworks = artworks)


@app.route('/artworks/<int:artwork_id>')
def artwork(artwork_id):
  artwork = Artwork.query.filter_by(id=artwork_id).one()
  artists = Artist.query.all()
  exhibitions = Exhibition.query.all()
  parks = Park.query.all()
  form = Form_artwork()
  artwork_join = (db.session.query(Exh_art_park, Artwork)
    .filter(Exh_art_park.artwork_id == Artwork.id)
    .filter(Artwork.id == artwork_id)).all()
  return render_template('artwork.html', artwork = artwork, artists = artists,
                         exhibitions = exhibitions, parks = parks, form = form,
                         artwork_join = artwork_join)


@app.route('/artworks/create', methods=['POST'])
def artwork_create():
  form = Form_artwork()
  if form.validate_on_submit():
    # Create artwork
    artwork = Artwork()
    # Add form items
    artwork.name = form.name.data

    # Add artists to 1-to-many relationship
    try:
      artwork.artists = []
      artists = filter(None, form.artists.data)
      # Add artists to artwork, removing duplicates
      for item in list(set(artists)):
        artist = Artist.query.filter_by(id = item).one()
        print "Adding {} to {}".format(artist.name, artwork.name)
        artwork.artists.append(artist)
    except Exception as e:
      raise e
    # Return errors if error is raised
    return jsonify({"success": False, "data": e})

    db.session.add(artwork)
    db.session.commit()
    # Return success message, artwork object via AJAX
    return jsonify({"success": True, "data": artwork.serialize})
  else:
    # Return errors if form doesn't validate
    return jsonify({"success": False, "data": form.errors})


@app.route('/artworks/<int:artwork_id>/edit', methods=['POST'])
def artwork_edit(artwork_id):
  artwork = Artwork.query.filter_by(id=artwork_id).one()
  form = Form_artwork()
  if form.validate_on_submit():
    # Update artwork items
    artwork.name = form.name.data

    # Add artists to 1-to-many relationship
    artwork.artists = []
    artists = filter(None, form.artists.data)
    # Add artists to artwork, removing duplicates
    for item in list(set(artists)):
      try:
        artist = Artist.query.filter_by(name = item).one()
        print "Adding {} to {}".format(artist.name, artwork.name)
        artwork.artists.append(artist)
      except Exception as e:
        db.session.rollback()
        # Return database exception(s)
        return jsonify({"success": False,
                        "data": "{} is not a recognized artist. Feel free to\
                                 add them to the database!".format(item)})

    # Clear out empty data
    exhibitions = filter(None, form.exhibitions.data)
    parks = filter(None, form.parks.data)
    # Add artwork/park children to Exh_art_park table if numbers are equal
    if len(exhibitions) == len(parks):
      # Clear exhibitions/parks 1-to-many relationships
      artwork.exhibitions = []
      artwork.parks = []
      # Sort exhibitions data by key and add to temporary array
      # for key in sorted(exhibitions.iterkeys()):
        # exh_sorted.append(exhibitions[key])
        # Sort parks data by key and add to temporary array
      # for key in sorted(parks.iterkeys()):
        # park_sorted.append(parks[key])
      # Loop through sorted arrays and add to Exh_art_park table
      for x, y in zip(exhibitions, parks):
        try:
          exhibition = Exhibition.query.filter_by(name = x).one()
          print "!!!EXHIBITION FOUND!: {}".format(exhibition.name)
          park = Park.query.filter_by(name = y).one()
          print "!!!PARK FOUND!: {}".format(park.name)
          exh_rel = Exh_art_park(exhibition_id = exhibition.id,
                                 artwork_id = artwork.id,
                                 park_id = park.id)
          db.session.add(exh_rel)
      except Exception as e:
        db.session.rollback()
        # Return errors if error is raised
        return jsonify({"success": False, "data": str(e)})

    else:
      db.session.rollback()
      # Return error if exhibitions and parks count is uneven
      return jsonify({"success": False,
                      "data": "There's an unequal number of exhibitions and\
                               parks. This data needs to be complete."})

    db.session.add(artwork)
    db.session.commit()
    # Return success message, artwork object via AJAX
    return jsonify({"success": True, "data": artwork.serialize})
  else:
    # Return errors if form doesn't validate
    return jsonify({"success": False, "data": form.errors})


@app.route('/artworks/<int:artwork_id>/delete', methods=['GET', 'POST'])
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
  return render_template('orgs.html', orgs = orgs)


@app.route('/orgs/<int:org_id>')
def org(org_id):
  org = Org.query.filter_by(id=org_id).one()
  exhibitions = Exhibition.query.all()
  form = Form_org()
  for exh in org.exhibitions:
    form.exhibitions.append_entry(exh)
  return render_template('org.html', org = org, exhibitions = exhibitions,
                         form = form)


@app.route('/orgs/create', methods=['POST'])
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
    try:
      # Clear org exhibitions
      org.exhibitions = []
      # Get list of exhibitions, removing empty form items
      exhibitions = filter(None, form.exhibitions.data)
      # Add latest exhibitions to org, removing duplicates
      for item in list(set(exhibitions)):
        exhibition = Exhibition.query.filter_by(id = item).one()
        org.exhibitions.append(exhibition)
      # Add org to database
      db.session.add(org)
      db.session.commit()
      # Return success message, org object via AJAX
      return jsonify({"success": True, "data": org.serialize})

    except Exception as e:
      raise e
      # Return errors if error is raised
      return jsonify({"success": False, "data": e})

  else:
    # Return errors if form doesn't validate
    return jsonify({"success": False, "data": form.errors})


@app.route('/orgs/<int:org_id>/edit', methods=['POST'])
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
        db.session.add(org)
        db.session.commit()
        print "Added {} exhibition to {}".format(exhibition.name, org.name)
      except Exception as e:
        print "{} is not a known exhibition".format(item)
        # raise e
        # Return errors if error is raised
        return jsonify({"success": False, "data": e})

    # Return success message, org object via AJAX
    return jsonify({"success": True, "data": org.serialize})

  else:
    # Return errors if form doesn't validate
    return jsonify({"success": False, "data": form.errors})


@app.route('/orgs/<int:org_id>/delete', methods=['GET', 'POST'])
def org_delete(org_id):
  org = Org.query.filter_by(id=org_id).one()
  form = Form_org()
  if request.method == 'POST':
      db.session.delete(org)
      db.session.commit()
      return redirect(url_for('orgs'))
  else:
      return render_template('org_delete.html', org = org, form = form)