# config.py

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class Config(object):
  """
  Common configurations
  """

  SECRET_KEY = os.environ.get('PARKS_DB_KEY')
  SQLALCHEMY_TRACK_MODIFICATIONS = True
  SQLALCHEMY_ECHO = False
  WTF_CSRF_ENABLED = True


class DevelopmentConfig(Config):
  """
  Development configurations
  """

  SQLALCHEMY_DATABASE_URI = 'sqlite:////{}/parks.db'.format(BASE_DIR)
  DEBUG = True



class ProductionConfig(Config):
  """
  Production configurations
  """

  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
  DEBUG = False


class TestConfig(Config):
  """
  Test configurations
  """

  SQLALCHEMY_DATABASE_URI = 'sqlite:////{}/test.db'.format(BASE_DIR)
  DEBUG = True
  TESTING = True
  WTF_CSRF_ENABLED = False
