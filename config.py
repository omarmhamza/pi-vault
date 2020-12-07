import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    # REMEMBER_COOKIE_DURATION = timedelta(minutes=120)
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)

class DevelopmentConfig(Config):
    MONGO_URI = "mongodb://localhost:27017/vault"


config = {
    'development': DevelopmentConfig
}
