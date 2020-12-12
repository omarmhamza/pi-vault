from flask import render_template, session, redirect, url_for, request, flash, abort, current_app
from . import version
import psutil
import platform
import requests
from flask_login import fresh_login_required, current_user


def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return "{} {}{}".format(round(bytes), unit, suffix)
        bytes /= factor


@version.route("/about", methods=["GET"])
def about():
    return render_template("about.html")


@version.route("/", methods=["GET"])
@fresh_login_required
def version():
    try:
        try:
            server_response = requests.get('http://127.0.0.1:5000').headers
            server = server_response["Server"]
        except:
            pass
        uname = platform.uname()
        svmem = psutil.virtual_memory()
        memory = get_size(svmem.total)
    except:
        uname = "Unknown"
        svmem = "Unknown"
        memory = "Unknown"
        server = "Unknown"
    system_information = {
        "System": uname[0],
        "Release": uname[2],
        "Machine": uname[3][0:20] + " ..." if uname != "Unknown" else uname,
        "Node": uname[1],
        "Memory Size": memory,
        "Server": server
    }
    python_version = platform.python_version()
    stack_information = {
        "Python": python_version if python_version else "Unknown" ,
        "MongoDB": "4.4.2",
        "Vue.js": "2.6.12"
    }

    return render_template("version-info.html", sys=system_information,stack=stack_information,user=current_user)


