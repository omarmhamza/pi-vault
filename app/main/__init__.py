from flask import Blueprint

main = Blueprint('main', __name__, template_folder="./template", static_folder="./static", static_url_path='')

from . import views
