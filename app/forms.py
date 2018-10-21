from flask_wtf import FlaskForm
from wtforms import StringField, FieldList
from wtforms.validators import DataRequired


class form_artist(FlaskForm):
  pName = StringField('Primary Name', validators=[DataRequired()])
  fName = StringField('First Name')
  email = StringField('Email', validators=[DataRequired()])
  phone = StringField('Phone')
  website = StringField('Website')
  artworks = FieldList(StringField('Artworks'), min_entries=0)


class form_artwork(FlaskForm):
  pass


class form_park(FlaskForm):
  pass


class form_exhibition(FlaskForm):
  name = StringField('Name')
  startDate = StringField('Start Date')
  endDate = StringField('End Date')
  installStart = StringField('Install Start')
  installEnd = StringField('Install End')
  deinstallDate = StringField('De-Install Due Date')
  prm = StringField('PRM Review')

  # parks = FieldList(StringField('Parks', min_entries=0))
  # artworks = FieldList(StringField('Artworks', min_entries=0))
  # organizations = FieldList(StringField('Organizations', min_entries=0))

class form_org(FlaskForm):
  pass