from datetime import datetime

from flask import render_template, session, redirect, url_for, request, flash
from forms import AddPasswordField
from Password import Password
from collections import deque
from . import main
from .. import mongo
from methods import *
from .. import hashids

account_number = "12345"  # test field




@main.route("/", methods=["GET"])
def index():
    web_accounts = getPasswords(account_number)
    passwords_list = deque()
    for passwords in web_accounts:
        for id, details in passwords.items():
            try:
                password = {"raw": Password.decrypt(details["encrypted"]), "website": details["website"],
                            "username": details["username"], "icon": details["icon"], "id": id, "validURL":details["validURL"]
                            }
                passwords_list.appendleft(password)
            except:
                continue

    return render_template("passwords.html", passwords=passwords_list)


@main.route("/passwords/add", methods=["GET", "POST"])
def addPassword():
    form = AddPasswordField()
    if form.is_submitted():
        if form.validate_on_submit():
            icon = getIconFromList(request.form.getlist('cat'))
            password = Password(
                website=form.website.data,
                icon= icon,
                username=form.email.data,
                raw=form.password.data,
                _id= getPasswordCount(account_number)[0]
            )
            pushPassword(account_number,password.jsonifyResponse())
            flash("You successfully added a password to the list", "success")
            return redirect("/")
        else:
            for field, error in form.errors.items():
                for e in error:
                    flash(e, "error")

    return render_template("add.html", icons=getIcons(), form=form)


@main.route("/passwords/edit/<id>", methods=["GET", "POST"])
def edit(id):
    form = AddPasswordField()
    if form.is_submitted() and form.validate_on_submit():
        now = datetime.now()
        date = now.strftime("%d/%m/%Y, %H:%M:%S")
        icon = getIconFromList(request.form.getlist('cat'))
        password = {
            "icon": icon,
            "website": form.website.data,
            "validURL" : Password.validateURL(form.website.data),
            "username" : form.email.data,
            "encrypted": Password.encrypt(form.password.data),
            "modified": str(date),
        }
        updatePassword(account_number,id,password)
        flash("Successfully edited password", "info")
        return redirect("/")
    return render_template("edit.html", icons=getIcons(), form=form, password=getPassword(account_number,id),id=id)


@main.route("/passwords/delete/<id>", methods=["GET"])
def delete(id):
    deletePassword(account_number,id)
    flash("Deleted password", "success")
    return redirect("/")
