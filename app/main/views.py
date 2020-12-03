from datetime import datetime
from flask import render_template, session, redirect, url_for, request, flash
from forms import AddPasswordField
from Password import Password, Encryption
from collections import deque
from . import main
from methods import *

account_number = "12345"  # test field


@main.route("/", methods=["GET"])
def index():
    web_accounts = getPasswords(account_number)
    passwords_list = deque()
    for passwords in web_accounts:
        for id, details in passwords.items():
            # try:

            password = {"raw": Encryption.decrypt(details["encrypted"]), "website": Encryption.decrypt(details["website"]),
                        "username": Encryption.decrypt(details["username"]), "icon": details["icon"], "id": id,
                        "validURL": details["validURL"], "created": details["created"]
                        }
            passwords_list.append(password)
            # except:
            #     continue
    sorted_pass = sorted(passwords_list, key=lambda i: i['created'], reverse=True)
    return render_template("passwords.html", passwords=sorted_pass)


@main.route("/passwords/add", methods=["GET", "POST"])
def addPassword():
    form = AddPasswordField()
    if form.is_submitted():
        if form.validate_on_submit():
            icon = getIconFromList(request.form.getlist('cat'))
            password = Password(
                website=form.website.data,
                icon=icon,
                username=form.email.data,
                raw=form.password.data,
                _id=getPasswordCount(account_number) + 1
            )
            pushPassword(account_number, password.jsonifyResponse())
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
            "website": Encryption.encrypt(form.website.data),
            "validURL": Password.validateURL(form.website.data),
            "username": Encryption.encrypt(form.email.data),
            "encrypted": Encryption.encrypt(form.password.data),
            "modified": str(date),
        }
        updatePassword(account_number, id, password)
        flash("Successfully edited password", "info")
        return redirect("/")
    return render_template("edit.html", icons=getIcons(), form=form, password=getPassword(account_number, id), id=id)


@main.route("/passwords/delete/<id>", methods=["GET"])
def delete(id):
    deletePassword(account_number, id)
    flash("Deleted password", "success")
    return redirect("/")


@main.route("/profile",methods=["GET"])
def profile():
    return render_template("user.html")


@main.route("/login",methods=["GET","POST"])
def login():
    return render_template("login.html")
