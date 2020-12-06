from flask import Flask, render_template
from flask_pymongo import PyMongo
from flask_wtf.csrf import CSRFProtect
from hashids import Hashids
from config import DevelopmentConfig
from flask_login import LoginManager

mongo = PyMongo()
csrf = CSRFProtect()
hashids = Hashids(min_length=5)
login_manager = LoginManager()
login_manager.login_view = 'main.login'
login_manager.login_message = "You have to login to access this page"
login_manager.login_message_category = "info"
login_manager.session_protection = "strong"


def run(config):
    app = Flask(__name__, template_folder='./template/')
    app.config.from_object(DevelopmentConfig)
    login_manager.init_app(app)

    csrf.init_app(app)
    mongo.init_app(app)
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    return app
