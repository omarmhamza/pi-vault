from datetime import datetime
from flask import render_template, session, redirect, url_for, request, flash, abort, current_app
from is_safe_url import is_safe_url
from .forms import AddPasswordField, Login, Signup
from .Password import Password
from collections import deque
from . import main
from .methods import *
from flask_login import login_user, login_required, logout_user, fresh_login_required, current_user
from .Account import Account
from . import error_views



@main.route("/", methods=["GET"])
@login_required
def index():
    if not current_user.is_authenticated:
        return current_app.login_manager.unauthorized()
    else:
        user = current_user
        web_accounts = getPasswords(user.id)
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
        return render_template("passwords.html", passwords=sorted_pass, user=user)


@main.route("/passwords/add", methods=["GET", "POST"])
@login_required
def addPassword():
    if not current_user.is_authenticated:
        return current_app.login_manager.unauthorized()
    else:
        user = current_user
        form = AddPasswordField()
        if form.is_submitted():
            if form.validate_on_submit():
                icon = getIconFromList(request.form.getlist('cat'))
                password = Password(
                    website=form.website.data,
                    icon=icon,
                    username=form.email.data,
                    raw=form.password.data,
                    _id=12312321
                    # _id=getPasswordCount(session["name"]) + 1
                )
                pushPassword(session['id'], password.jsonifyResponse())
                flash("You successfully added a password to the list", "success")
                return redirect("/")
            else:
                for field, error in form.errors.items():
                    for e in error:
                        flash(e, "error")
        return render_template("add.html", icons=getIcons(), form=form, user=user)


@main.route("/passwords/edit/<id>", methods=["GET", "POST"])
@login_required
def edit(id):
    if not current_user.is_authenticated:
        return current_app.login_manager.unauthorized()
    else:
        user = current_user
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
            updatePassword(session['id'], id, password)
            flash("Successfully edited password", "info")
            return redirect("/")
        return render_template("edit.html", icons=getIcons(), form=form, password=getPassword(session['id'], str(id)),
                               id=id, user=user)


@main.route("/passwords/delete/<id>", methods=["GET"])
@login_required
def delete(id):
    deletePassword(session['id'], id)
    flash("Deleted password", "success")
    return redirect("/")


@main.route("/profile", methods=["GET","POST"])
@fresh_login_required
def profile():
    if not current_user.is_authenticated:
        return current_app.login_manager.unauthorized()
    else:
        user = current_user
        form = Login()
        if form.is_submitted() and form.validate_on_submit():
            if checkAvailability(form.username):
                updateCredentials(user._id,form.username.data,form.password.data)
                flash("Updated credentials","success")
                return redirect("/profile")
            else:
                flash("This username is taken, please try another one.","error")
    return render_template("user.html", user=current_user,form=form)


@main.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        flash("{} you are already logged in".format(current_user.username),"info")
        return redirect("/")
    form = Login()
    if form.is_submitted() and form.validate_on_submit():
        username = form.username.data.lower()
        raw_pass = form.password.data
        account = validateAccount(username)
        if account:
            if Account.check_password(account["authentication"]["hashed"], raw_pass):
                flash("You are signed in", "success")
                rememberMe = form.rememberMe.data
                user = Account(username, raw_pass)
                user.authenticate()
                user._id = account["_id"]
                session['id'] = account["_id"]
                is_logged = login_user(user, rememberMe)
                if is_logged:
                    if rememberMe:
                        session.permanent = True
                    next_page = request.args.get('next')
                    if next_page is None or not next_page.startswith('/'):
                        next_page = url_for('main.index')
                    elif not is_safe_url(next_page, allowed_hosts={"0.0.0.0"}):
                        return "NOT SAFE"
                    return redirect(next_page)
                else:
                    flash("An error has occurred, please try again later.", "error")
            else:
                flash("Your username/password is wrong", "error")
        else:
            flash("There is no account with this username", "error")
    return render_template("login.html", form=form)


@main.route("/signup", methods=["GET", "POST"])
def signup():
    form = Signup()
    if form.is_submitted() and form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        if checkAvailability(username):
            user = Account(username=username,password=password)
            addAccount(user)
            user.authenticate()
            session['id'] = user._id
            is_logged = login_user(user)
            if is_logged:
                flash("You have successfully created an account and signed in","success")
            else:
                flash("Accounted created successfully.","info")
            return redirect("/")
        else:
            flash("This username is taken, try another one.","error")
    return render_template("signup.html",form=form)



@main.route("/logout")
def logout():
    logout_user()
    flash("You have been logged out", "info")
    return redirect("/login")






