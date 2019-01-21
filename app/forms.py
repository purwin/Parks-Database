from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed

from wtforms import (
  StringField,
  TextAreaField,
  FieldList,
  SelectField,
  PasswordField,
  BooleanField,
  HiddenField
)
from wtforms.validators import (
  DataRequired,
  Optional,
  Email,
  ValidationError,
  AnyOf
)
from wtforms.fields.html5 import DateField, TelField, EmailField

from users import User


class Form_artist(FlaskForm):
  pName = StringField('Primary/Last Name', validators=[DataRequired()])
  fName = StringField('First Name')
  email = EmailField('Email', validators=[Email()])
  phone = TelField('Phone')
  website = StringField('Website')

  # Related
  artworks = FieldList(StringField('Artwork'), min_entries=1)
  # FUTURE: custom validation for artworks


class Form_artwork(FlaskForm):
  name = StringField('Name', validators=[DataRequired()])

  # Related
  exhibitions = FieldList(StringField('Exhibition'))
  parks = FieldList(StringField('Park'))
  artists = FieldList(StringField('Artist'))


class Form_park(FlaskForm):
  name = StringField('Name', validators=[DataRequired()])
  park_id = StringField('Park ID No.', validators=[DataRequired()])
  borough = SelectField('Borough',
                        choices=[('Bronx', 'Bronx'),
                                 ('Brooklyn', 'Brooklyn'),
                                 ('Manhattan', 'Manhattan'),
                                 ('Queens', 'Queens'),
                                 ('Staten Island', 'Staten Island')],
                        validators=[DataRequired()])
  address = StringField('Address')
  cb = StringField('Community Board', validators=[DataRequired()])

  # Related
  exhibitions = FieldList(StringField('Exhibition'))
  artworks = FieldList(StringField('Artwork'))


class Form_exhibition(FlaskForm):
  # Bio
  name = StringField('Name')
  start_date = DateField('Start Date', validators=[DataRequired()], format='%Y-%m-%d')
  end_date = DateField('End Date', validators=[DataRequired()], format='%Y-%m-%d')
  opening = DateField('Opening', validators=[Optional()])
  comments = TextAreaField('Comments')

  # Install
  install_start = DateField('Install Start', validators=[DataRequired()], format='%Y-%m-%d')
  install_end = DateField('Install End', validators=[Optional()])
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
  deinstall_date = DateField('De-Install Due Date', validators=[DataRequired()], format='%Y-%m-%d')
  deinstall_check = DateField('De-Install Site Check', format='%Y-%m-%d', validators=[Optional()])
  bond_return = StringField('Bond returned')
  press_clippings = StringField('Press Clippings Saved')

  # Related
  parks = FieldList(StringField('Park'))
  artworks = FieldList(StringField('Artwork'))
  orgs = FieldList(StringField('Organization'))


class Form_org(FlaskForm):
  name = StringField('Name', validators=[DataRequired()])
  website = StringField('Website')
  phone = TelField('Phone')

  # Related
  exhibitions = FieldList(StringField('Exhibition'))


class Form_user(FlaskForm):
  username = StringField('Username', validators=[DataRequired()])
  password = PasswordField('Password', validators=[DataRequired()])
  remember = BooleanField('Remember')

  def validate_username(self, username):
    user = User.query.filter_by(username=username.data).first()
    if user is None:
      raise ValidationError('User not found!')


class Form_signup(FlaskForm):
  username = StringField('Username', validators=[DataRequired()])
  password = PasswordField('Password', validators=[DataRequired()])
  remember = BooleanField('Remember')

  def validate_username(self, username):
    user = User.query.filter_by(username=username.data).first()
    if user is not None:
      raise ValidationError('Please use a different username.')


class Form_search(FlaskForm):
  class_object = HiddenField('Class Object', validators=[DataRequired(),
    AnyOf(['Park', 'Exhibition', 'Artwork', 'Artist', 'Org'])])
  search = StringField('Search', validators=[DataRequired()])


class Form_import_file(FlaskForm):
  file = FileField(validators=[FileRequired(), FileAllowed(['csv'], 'Please choose a CSV file!')])


class FreeSelectField(SelectField):
    """
    Attempt to make an open ended select multiple field that can accept dynamic
    choices added by the browser.
    """
    def pre_validate(self, form):
        pass


class Form_import_data(FlaskForm):
  file = FileField(validators=[FileRequired(), FileAllowed(['csv'], 'Please choose a CSV file!')])
  class_object = SelectField('Import Type',
                        choices=[('', 'Choose an Object Type'),
                                 ('exhibition', 'Exhibitions'),
                                 ('artwork', 'Artworks'),
                                 ('park', 'Parks'),
                                 ('artist', 'Artists'),
                                 ('org', 'Orgs')],
                        validators=[DataRequired()])
  match_existing = BooleanField('Match Existing Items in the Database')
  keys = FieldList(FreeSelectField('Key'))
  values = FieldList(FreeSelectField('Value'))
