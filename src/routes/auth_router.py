from urllib.parse import unquote

import flask_login
from flask import request, render_template, redirect

from src.controllers.user_controller import user_object_get_by_login, authorize
from src.utils import allowed_anonymous


@allowed_anonymous
def login():
    if request.method == "POST":
        next_url = unquote(request.args.get("next", default="/"))

        login = request.form.get("login")
        password = request.form.get("password")

        if authorize(login, password):
            flask_login.login_user(user_object_get_by_login(login))
            return redirect(next_url)
        return render_template("auth/login.html", error="Wrong credentials")
    else:
        return render_template("auth/login.html")

def logout():
    flask_login.logout_user()
    return redirect("/")