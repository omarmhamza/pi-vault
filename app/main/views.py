from datetime import datetime

from flask import render_template, session, redirect, url_for, request, flash
from forms import AddPasswordField
from Password import Password
from collections import deque
from . import main
from .. import mongo
from methods import getIcons
from .. import hashids

account_number = "12345"  # test field


@main.route("/", methods=["GET"])
def index():
    account = mongo.db.users.find_one_or_404({"_id": account_number})
    passwords = deque()
    for web_account in account["passwords"]:
        if web_account["icon_unicode"] != "0":
            icon_meta = mongo.db.icons.find_one_or_404({"unicode": web_account["icon_unicode"]})
        else:
            icon_meta = {"name": ""}
        password = {"raw": Password.decrypt(web_account["encrypted"]), "website": web_account["website"],
                    "username": web_account["username"], "icon": web_account["icon_unicode"],"id":web_account["id"],
                    "icon_name":icon_meta["name"]}
        passwords.appendleft(password)
    return render_template("passwords.html", passwords=passwords)




@main.route("/passwords/add", methods=["GET", "POST"])
def addPassword():
    form = AddPasswordField()
    if form.is_submitted():
        if form.validate_on_submit():
            account = mongo.db.users.find_one_or_404({"_id": account_number})
            entry = Password(
                website=form.website.data,
                icon=str(request.form.getlist('cat').pop().decode('utf-8')).strip("&#x"),
                username=form.email.data,
                _id=len(account["passwords"]) + 1,
                raw=form.password.data
            )
            mongo.db.users.update_one(
                {"_id": account_number},
                {'$push': {"passwords": entry.jsonifyResponse()}}
            )
            flash("You successfully added a password to the list", "success")
            return redirect("/")
        else:
            for field, error in form.errors.items():
                for e in error:
                    flash(e, "danger")

    return render_template("add.html", icons=getIcons(), form=form)


@main.route("/passwords/edit/<id>", methods=["GET", "POST"])
def edit(id):
    form = AddPasswordField()
    if form.is_submitted() and form.validate_on_submit():
        website = form.website.data
        icon = str(request.form.getlist('cat').pop().decode('utf-8')).strip("&#x")
        username = form.email.data
        encrypted = Password.encrypt(form.password.data)
        pass_index = hashids.decrypt(id)[0] - 1
        now = datetime.now()
        date = now.strftime("%d/%m/%Y, %H:%M:%S")
        updated_values =  {
            "passwords.{}.website".format(pass_index): website,
            "passwords.{}.icon_unicode".format(pass_index): icon,
            "passwords.{}.username".format(pass_index): username,
            "passwords.{}.encrypted".format(pass_index): encrypted,
            "passwords.{}.modified".format(pass_index): date,
        }

        mongo.db.users.update_one(
            {"_id": account_number},
            {'$set': updated_values}
        )
        flash("Successfully edited password","info")
        return redirect("/")
    account = mongo.db.users.find_one_or_404({"_id": account_number})
    passwords = account["passwords"]
    for password in passwords:
        if password["id"] == id:
            return render_template("edit.html", icons=getIcons(), form=form,password=password)

