from flask import render_template, session, redirect, url_for, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired
from forms import AddPasswordField
from . import main
from .. import mongo


@main.route("/", methods=["GET"])
def index():
    return render_template("passwords.html")


@main.route("/passwords/add", methods=["GET", "POST"])
def addPassword():
    form = AddPasswordField()
    if form.is_submitted():
        if form.validate_on_submit():
            pass
            # cat = str(request.form.getlist('cat').pop().decode('utf-8'))
            # if cat != "0":
            #     cat = cat.strip("&#x")
            #     website_icon = mongo.db.icons.find_one({"unicode":cat})
            #     print(website_icon["name"])
        else:
            print(form.errors)
    icons = []
    get_icons = mongo.db.icons.find()
    for icon in get_icons:
        coded = "{}{}".format("&#x", icon["unicode"])
        icons.append((coded,icon["name"]))
    return render_template("add.html", icons=icons, form=form)
