from flask import render_template, session, redirect, url_for, request, flash, abort, current_app
from . import main
from .. import login_manager

@login_manager.unauthorized_handler
def unauthorized():
    return redirect("/login")

@main.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('error.html',code="Error 404",text="Page not found"), 404


@main.errorhandler(403)
def forbidden(e):
    # note that we set the 404 status explicitly
    return render_template('error.html',code="Error 403",text="Forbidden"), 403


@main.errorhandler(500)
def forbidden(e):
    # note that we set the 404 status explicitly
    return render_template('error.html',code="Error 500",text="Internal Server Error"), 500