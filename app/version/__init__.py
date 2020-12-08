from flask import Blueprint

version = Blueprint('version', __name__,template_folder="./template",static_folder="./static",static_url_path='',url_prefix="/version")

from . import views
