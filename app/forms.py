from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TextAreaField, FieldList
from wtforms.validators import DataRequired
# from wtforms.fields.html5 import DateField


class Form_artist(FlaskForm):
  pName = StringField('Primary Name', validators=[DataRequired()])
  fName = StringField('First Name')
  email = StringField('Email', validators=[DataRequired()])
  phone = StringField('Phone')
  website = StringField('Website')
  artworks = FieldList(StringField('Artwork'), min_entries=1)
  # FUTURE: custom validation for artworks

class Form_artwork(FlaskForm):
  name = StringField('Name', validators=[DataRequired()])
  exhibitions = FieldList(StringField('Exhibition'))
  parks = FieldList(StringField('Park'))
  artists = FieldList(StringField('Artist'))


class Form_park(FlaskForm):
  name = StringField('Name', validators=[DataRequired()])
  borough = StringField('Borough', validators=[DataRequired()])
  address = StringField('Address', validators=[DataRequired()])
  cb = StringField('Community Board', validators=[DataRequired()])
  exhibitions = FieldList(StringField('Exhibition'))
  artworks = FieldList(StringField('Artwork'))

class Form_exhibition(FlaskForm):
  # Bio
  name = StringField('Name')
  start_date = DateField('Start Date', validators=[DataRequired()], format='%Y-%m-%d')
  end_date = DateField('End Date', validators=[DataRequired()])
  opening = DateField('Opening')
  comments = TextAreaField('Comments')

  # Install
  install_start = DateField('Install Start', validators=[DataRequired()])
  install_end = DateField('Install End')
  prm = StringField('PRM Review')
  approval = StringField('Borough Approval')
  walkthrough = StringField('Walk-Thru PRM')
  cb_presentation = StringField('CB Presentation')
  license_mailed = StringField('License Mailed')
  license_signed = StringField('License Signed')
  license_borough = StringField('License to Borough')
  bond = StringField('Bond Amount Received')
  coi = StringField('COI Received')
  coi_renewal = StringField('COI Renewal Date')
  signage_submit = StringField('Signage Submitted')
  signage_received = StringField('Signage Installed')
  press_draft = StringField('Draft Press Release')
  press_approved = StringField('Press Release Approved')
  web_text = StringField('Web Text Sent')
  work_images = StringField('Images of Installed Work')

  # De-Install
  deinstall_date = StringField('De-Install Due Date', validators=[DataRequired()])
  deinstall_check = StringField('De-Install Site Check')
  bond_return = StringField('Bond returned')
  press_clippings = StringField('Press Clippings Saved')

  # Related
  parks = FieldList(StringField('Park', min_entries=0))
  artworks = FieldList(StringField('Artwork', min_entries=0))
  organizations = FieldList(StringField('Organization', min_entries=0))

class Form_org(FlaskForm):
  name = StringField('Name', validators=[DataRequired()])
