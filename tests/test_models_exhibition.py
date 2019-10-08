import unittest
from datetime import date, datetime

from base import BaseTests

from app import db
from app.parks_db import Exhibition, Park


def format_date(date_text):
    if not date_text:
        return None

    for style in ('%Y-%m-%d', '%m.%d.%Y', '%m.%d.%y', '%m/%d/%Y', '%m/%d/%y'):
        try:
            # Determine style of date string
            date = datetime.strptime(str(date_text), style)
            # Return date object
            return date

        except ValueError:
            pass
    raise ValueError('Can\'t determine date format of {}!'.format(date_text))


class TestModelsExhibition(BaseTests):

  default_exhibition = dict(
      name='Swanky Exhibition',
      start_date=format_date('2019-01-01'),
      end_date=format_date('2019-06-01'),
      opening=format_date('2019-01-01'),
      comments='',
      install_start=format_date('2018-12-28'),
      install_end=format_date('2019-01-01'),
      prm='',
      approval='',
      walkthrough='',
      cb_presentation='',
      license_mailed='',
      license_signed='',
      license_borough='',
      bond='',
      coi='',
      coi_renewal='',
      signage_submit='',
      signage_received='',
      press_draft='',
      press_approved='',
      web_text='',
      work_images='',
      deinstall_date=format_date('2019-06-05'),
      deinstall_check='',
      bond_return='',
      press_clippings=''
  )

  @staticmethod
  def create_exhibition(**kwargs):
    """
    Static method to add exhibition class object to database
    Takes the following string args: name, start_date, end_date, opening,
        comments, install_start, install_end, prm, approval, walkthrough,
        cb_presentation, license_mailed, license_signed, license_borough, bond,
        coi, coi_renewal, signage_submit, signage_received, press_draft,
        press_approved, web_text, work_images, deinstall_date, deinstall_check,
        bond_return, press_clippings
    Adds class to Exhibition database, commits session, and flushes to get id val
    Returns the created class instance
    """
    exhibition = Exhibition(**kwargs)
    db.session.add(exhibition)
    db.session.commit()
    db.session.flush()

    return exhibition


  @staticmethod
  def datetime_to_date(datetime_obj):
      return datetime.date(datetime_obj)


  # Test CREATE exhibition valid
  def test_valid_exhibition_create(self):
    temp_exhibition = self.default_exhibition

    self.create_exhibition(**temp_exhibition)

    exhibition_object = Exhibition.query.filter_by(
        name=self.default_exhibition['name']
    ).first()

    self.assertEqual(exhibition_object.id, 1)
    self.assertEqual(exhibition_object.name, self.default_exhibition['name'])
    self.assertEqual(
        exhibition_object.start_date,
        self.datetime_to_date(self.default_exhibition['start_date'])
    )
    self.assertEqual(
        exhibition_object.end_date,
        self.datetime_to_date(self.default_exhibition['end_date'])
    )
    self.assertEqual(
        exhibition_object.install_start,
        self.datetime_to_date(self.default_exhibition['install_start'])
    )
    self.assertEqual(
        exhibition_object.install_end,
        self.datetime_to_date(self.default_exhibition['install_end'])
    )


  # Test CREATE exhibition valid
  def test_valid_exhibition_create_name(self):
    self.create_exhibition(
        name=self.default_exhibition['name'],
        start_date=self.default_exhibition['start_date'],
        end_date=self.default_exhibition['end_date'],
        install_start=self.default_exhibition['install_start'],
        install_end=self.default_exhibition['install_end'],
        opening=self.default_exhibition['opening']
    )

    exhibition_object = Exhibition.query.filter_by(
        name=self.default_exhibition['name']
    ).first()

    self.assertEqual(exhibition_object.id, 1)
    self.assertEqual(exhibition_object.name, self.default_exhibition['name'])
    self.assertEqual(
        exhibition_object.start_date,
        self.datetime_to_date(self.default_exhibition['start_date'])
    )
    self.assertEqual(
        exhibition_object.end_date,
        self.datetime_to_date(self.default_exhibition['end_date'])
    )
    self.assertEqual(
        exhibition_object.opening,
        self.datetime_to_date(self.default_exhibition['opening'])
    )
    self.assertEqual(
        exhibition_object.install_start,
        self.datetime_to_date(self.default_exhibition['install_start'])
    )
    self.assertEqual(
        exhibition_object.install_end,
        self.datetime_to_date(self.default_exhibition['install_end'])
    )
    self.assertEqual(exhibition_object.comments, '')
    self.assertEqual(exhibition_object.prm, '')
    self.assertEqual(exhibition_object.approval, '')
    self.assertEqual(exhibition_object.walkthrough, '')
    self.assertEqual(exhibition_object.cb_presentation, '')
    self.assertEqual(exhibition_object.license_mailed, '')
    self.assertEqual(exhibition_object.license_signed, '')
    self.assertEqual(exhibition_object.license_borough, '')
    self.assertEqual(exhibition_object.bond, '')
    self.assertEqual(exhibition_object.coi, '')
    self.assertEqual(exhibition_object.coi_renewal, '')
    self.assertEqual(exhibition_object.signage_submit, '')
    self.assertEqual(exhibition_object.signage_received, '')
    self.assertEqual(exhibition_object.press_draft, '')
    self.assertEqual(exhibition_object.press_approved, '')
    self.assertEqual(exhibition_object.web_text, '')
    self.assertEqual(exhibition_object.work_images, '')
    self.assertEqual(exhibition_object.deinstall_date,None)
    self.assertEqual(exhibition_object.deinstall_check, '')
    self.assertEqual(exhibition_object.bond_return, '')
    self.assertEqual(exhibition_object.press_clippings, '')


  # Test CREATE exhibition with no name value added
  def test_invalid_exhibition_create_empty(self):
    self.create_exhibition(name=False)

    self.assertRaises(AttributeError)


  # Test UPDATING exhibition
  def test_valid_exhibition_update(self):
    temp_exhibition = self.default_exhibition

    exhibition = self.create_exhibition(**temp_exhibition)

    temp_end_date = format_date('2019-07-31')

    exhibition.end_date = temp_end_date
    db.session.add(exhibition)
    db.session.commit()

    exhibition_object = Exhibition.query.filter_by(
        name=self.default_exhibition['name']
    ).first()

    self.assertEqual(exhibition_object.id, 1)
    self.assertEqual(exhibition_object.name, self.default_exhibition['name'])
    self.assertEqual(
        exhibition_object.start_date,
        self.datetime_to_date(self.default_exhibition['start_date'])
    )
    self.assertEqual(
        exhibition_object.end_date,
        self.datetime_to_date(temp_end_date)
    )


  # Test DELETING exhibition
  def test_valid_exhibition_delete(self):
    temp_exhibition = self.default_exhibition

    exhibition = self.create_exhibition(**temp_exhibition)

    exhibition_object = Exhibition.query.filter_by(
        name=temp_exhibition['name']
    ).first()

    self.assertEqual(exhibition_object.name, temp_exhibition['name'])

    db.session.delete(exhibition)
    db.session.commit()

    exhibition_object = Exhibition.query.filter_by(
        name=temp_exhibition['name']
    ).first()

    self.assertIsNone(exhibition_object)


  # Test Exhibition.serialize
  def test_valid_exhibition_serialize(self):
    temp_exhibition = self.default_exhibition

    self.create_exhibition(**temp_exhibition)

    exhibition_object = Exhibition.query.filter_by(
        name=temp_exhibition['name']
    ).first()

    self.assertEqual(
        exhibition_object.serialize,
        {
          'id': 1,
          'name': temp_exhibition['name'],
          'start_date': self.datetime_to_date(temp_exhibition['start_date']),
          'end_date': self.datetime_to_date(temp_exhibition['end_date']),
          'opening': self.datetime_to_date(temp_exhibition['opening']),
          'comments': temp_exhibition['comments'],
          'install_start': self.datetime_to_date(temp_exhibition['install_start']),
          'install_end': self.datetime_to_date(temp_exhibition['install_end']),
          'prm': temp_exhibition['prm'],
          'approval': temp_exhibition['approval'],
          'walkthrough': temp_exhibition['walkthrough'],
          'cb_presentation': temp_exhibition['cb_presentation'],
          'license_mailed': temp_exhibition['license_mailed'],
          'license_signed': temp_exhibition['license_signed'],
          'license_borough': temp_exhibition['license_borough'],
          'bond': temp_exhibition['bond'],
          'coi': temp_exhibition['coi'],
          'coi_renewal': temp_exhibition['coi_renewal'],
          'signage_submit': temp_exhibition['signage_submit'],
          'signage_received': temp_exhibition['signage_received'],
          'press_draft': temp_exhibition['press_draft'],
          'press_approved': temp_exhibition['press_approved'],
          'web_text': temp_exhibition['web_text'],
          'work_images': temp_exhibition['work_images'],
          'deinstall_date': self.datetime_to_date(temp_exhibition['deinstall_date']),
          'deinstall_check': temp_exhibition['deinstall_check'],
          'bond_return': temp_exhibition['bond_return'],
          'press_clippings': temp_exhibition['press_clippings']
        }
    )


if __name__ == '__main__':
  unittest.main()