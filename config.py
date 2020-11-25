import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'


class DevelopmentConfig(Config):
    MONGO_URI = "mongodb://localhost:27017/vault"


config = {
    'development': DevelopmentConfig
}
