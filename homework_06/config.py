from os import getenv

"""
"postgresql+psycopg2://app:password@localhost/shop",
"sqlite+pysqlite:///database.db"
"""

SQLALCHEMY_DATABASE_URI = getenv(
    "SQLALCHEMY_DATABASE_URI",
    "postgresql+psycopg2://app:password@localhost/shop",
)


class Config:
    DEBUG = False
    TESTING = False
    ENV = "development"

    SECRET_KEY = "\xb8\xd5\xcf\xee\x0c\x974$\x81?\xdd\xe1G\n\xab\xe2"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI


class ProductionConfig(Config):
    ENV = "production"
    SECRET_KEY = "\x13\xd1|\x9c\x1a\xfe+\x05\x05MN\xa0/\xa3\xaf\xee"


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
