from flask import Flask, render_template
from flask_pymongo import PyMongo
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig, ProductionConfig
from flask_login import LoginManager

mongo = PyMongo()
csrf = CSRFProtect()
login_manager = LoginManager()
login_manager.session_protection = "strong"


def run(config):
    app = Flask(__name__, template_folder='./template/')
    if config == "production":
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)
    login_manager.init_app(app)
    csrf.init_app(app)
    mongo.init_app(app)
    from .main import main as main_blueprint
    from .version import version as version_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(version_blueprint)
    return app
