from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class form_artist(FlaskForm):
  pName = StringField('Primary Name', validators=[DataRequired()])
  fName = StringField('First Name')
  email = StringField('Email', validators=[DataRequired()])
  phone = StringField('Phone')
  website = StringField('Website')
  artworks = StringField('Artworks')