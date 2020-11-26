from flask import render_template, session, redirect, url_for, request, flash
from forms import AddPasswordField
from Password import Password
from . import main
from .. import mongo


@main.route("/", methods=["GET"])
def index():
    account_number = "12345"  # test field
    account = mongo.db.users.find_one_or_404({"_id": account_number})
    passwords = []
    for web_account in account["passwords"]:
        entry = {"raw": Password.decrypt(web_account["encrypted"]), "website": web_account["website"],
                 "username": web_account["username"], "icon": web_account["icon_unicode"]}
        passwords.append(entry)
    return render_template("passwords.html",passwords=passwords)


@main.route("/passwords/add", methods=["GET", "POST"])
def addPassword():
    form = AddPasswordField()
    if form.is_submitted():
        if form.validate_on_submit():
            account_number = "12345"  # test field
            account = mongo.db.users.find_one_or_404({"_id": account_number})
            entry = Password(
                website=form.website.data,
                icon=str(request.form.getlist('cat').pop().decode('utf-8')).strip("&#x"),
                username=form.email.data,
                _id=len(account["passwords"]) + 1,
                raw = form.password.data
            )
            mongo.db.users.update_one(
                {"_id": account_number},
                {'$push': {"passwords": entry.jsonifyResponse()}}
            )
            flash("You successfully added a password to the list","success")
            return redirect("/")
        else:
            for field,error in form.errors.items():
                for e in error:
                    flash(e,"danger")
    icons = []
    get_icons = mongo.db.icons.find()
    for icon in get_icons:
        coded = "{}{}".format("&#x", icon["unicode"])
        icons.append((coded, icon["name"]))
    return render_template("add.html", icons=icons, form=form)



