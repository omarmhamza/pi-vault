import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '8D2AF8FAE7D87D2F244A62F51A855'
    VERSION = "1.0.0"
    VUE = "vue.min.js"  # production vue
    USE_SESSION_FOR_NEXT = True
    GITHUB_LINK = "https://github.com/omarmhamza/pi-vault"



class DevelopmentConfig(Config):
    VERSION = "dev 1.0.0"
    MONGO_URI = os.environ.get('MONGO_URI') or "mongodb://localhost:27017/vault"
    VUE = "vue.js"
    REMEMBER_COOKIE_DURATION = timedelta(minutes=5)
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
    DEBUG = True


class ProductionConfig(Config):
    REMEMBER_COOKIE_DURATION = timedelta(minutes=5)
    PERMANENT_SESSION_LIFETIME = timedelta(days=1)
    VUE = "vue.min.js"  # production vue version
    MONGO_URI = os.environ.get('MONGO_URI') or "mongodb://localhost:27017/vault"






config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
