from flask import Flask, render_template
from flask_pymongo import PyMongo
from flask_wtf.csrf import CSRFProtect

from config import DevelopmentConfig

mongo = PyMongo()
csrf = CSRFProtect()


def run_app(config):
    app = Flask(__name__, template_folder='./template')
    app.config.from_object(DevelopmentConfig)
    csrf.init_app(app)
    mongo.init_app(app)
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    return app

