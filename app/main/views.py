from datetime import datetime
from flask import render_template, session, redirect, url_for, request, flash
from forms import AddPasswordField, Login
from Password import Password, Encryption
from collections import deque
from . import main
from methods import *
from flask_login import login_user, login_required, logout_user
from Account import Account

account_number = "OMAR"  # test field


@main.route("/", methods=["GET"])
@login_required
def index():
    web_accounts = getPasswords(account_number)
    passwords_list = deque()
    for passwords in web_accounts:
        for id, details in passwords.items():
            # try:

            password = {"raw": Encryption.decrypt(details["encrypted"]),
                        "website": Encryption.decrypt(details["website"]),
                        "username": Encryption.decrypt(details["username"]), "icon": details["icon"], "id": id,
                        "validURL": details["validURL"], "created": details["created"]
                        }
            passwords_list.append(password)
            # except:
            #     continue
    sorted_pass = sorted(passwords_list, key=lambda i: i['created'], reverse=True)
    return render_template("passwords.html", passwords=sorted_pass)


@main.route("/passwords/add", methods=["GET", "POST"])
@login_required
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
@login_required
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
@login_required
def delete(id):
    deletePassword(account_number, id)
    flash("Deleted password", "success")
    return redirect("/")


@main.route("/profile", methods=["GET"])
@login_required
def profile():
    return render_template("user.html")


@main.route("/login", methods=["GET", "POST"])
def login():
    form = Login()
    if form.is_submitted() and form.validate_on_submit():
        username = form.username.data.lower()
        raw_pass = form.password.data
        account = validateAccount(username, raw_pass)
        if account:
            if Account.check_password(account["authentication"]["hashed"], raw_pass):
                flash("You are signed in", "success")
                rememberMe = form.rememberMe.data
                user = Account(username, raw_pass)
                user.authenticate()
                user.authentication = user.active = True
                x = login_user(user, rememberMe)
                print x
                next_page = request.args.get('next')
                if next_page is None or not next_page.startswith('/'):
                    next_page = url_for('main.index')
                return redirect(next_page)
            else:
                flash("Your username/password is wrong", "error")
        else:
            flash("There is no account with this username", "error")
        return redirect("/login")

    return render_template("login.html", form=form)


@main.route("/signup", methods=["GET", "POST"])
def signup():
    account = Account("OMAR", "test")
    addAccount(account)
    return "added"


# @main.route("/logout")
# def logout():
#     return int(getAccountId("omar")["_id"])
    # logout_user()
    # flash("You have been logged out","info")
    # return redirect("/login")
