# config.py

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class Config(object):
  """
  Common configurations
  """
  SQLALCHEMY_DATABASE_URI = 'sqlite:////{}/parks.db'.format(BASE_DIR)
  SECRET_KEY = os.environ.get('PARKS_DB_KEY')
  SQLALCHEMY_TRACK_MODIFICATIONS = True


class DevelopmentConfig(Config):
  """
  Development configurations
  """
  DEBUG = True
  SQLALCHEMY_ECHO = False


class ProductionConfig(Config):
  """
  Production configurations
  """

  DEBUG = False
  PSQL = {
    'user': 'michaelpurwin',
    'pw': 'P1i1z1z1a1!',
    'db': 'parks_db',
    'host': 'localhost',
    'port': '5433'
  }
  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


class TestConfig(Config):
  """
  Test configurations
  """

  SQLALCHEMY_DATABASE_URI = 'sqlite:////{}/test.db'.format(BASE_DIR)
  SECRET_KEY = os.environ.get('PARKS_DB_KEY')
  DEBUG = True
  TESTING = True
  WTF_CSRF_ENABLED = False
