from flask import render_template, redirect, flash
from . import main
from .. import login_manager

login_manager.login_view = 'main.login'
login_manager.login_message = "You have to login to access this page"
login_manager.login_message_category = "info"
login_manager.refresh_view = 'main.login'
login_manager.needs_refresh_message = "Session timedout, please re-login"
login_manager.needs_refresh_message_category = "info"
login_manager.refresh_view = "main.login"
login_manager.needs_refresh_message = (
    "To protect your account, please reauthenticate to access this page."
)
login_manager.needs_refresh_message_category = "info"


# @login_manager.unauthorized_handler
# def unauthorized():
#     flash("You need to be logged in to access this page!","error")
#     return redirect("/login")

@main.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('error.html', code="Error 404", text="Page not found"), 404


@main.errorhandler(403)
def forbidden(e):
    # note that we set the 404 status explicitly
    return render_template('error.html', code="Error 403", text="Forbidden"), 403


@main.errorhandler(500)
def forbidden(e):
    # note that we set the 404 status explicitly
    return render_template('error.html', code="Error 500", text="Internal Server Error"), 500
