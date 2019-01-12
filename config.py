# config.py

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class Config(object):
  """
  Common configurations
  """

  SQLALCHEMY_DATABASE_URI = 'sqlite:////{}/parks.db'.format(BASE_DIR)

  # SECRET_KEY = 'tomagatchi!!'
  SECRET_KEY = os.environ.get('PARKS_DB_KEY')


  SQLALCHEMY_TRACK_MODIFICATIONS = True

  # Flask MSearch
  MSEARCH_INDEX_NAME = 'msearch'
  MSEARCH_BACKEND = 'whoosh'
  # auto create or update index
  MSEARCH_ENABLE = True

  MAX_SEARCH_RESULTS = 50


class DevelopmentConfig(Config):
  """
  Development configurations
  """

  DEBUG = True

  SQLALCHEMY_ECHO = False

  print 'THIS APP IS IN DEBUG MODE. YOU SHOULD NOT SEE THIS IN PRODUCTION.'


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

  # SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % PSQL
  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}