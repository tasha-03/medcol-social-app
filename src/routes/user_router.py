from flask import render_template, request, redirect
from src.controllers import user_controller
from src.utils import admin_only, required_roles


# @admin_only
@required_roles([1])
def users_all():
    data = user_controller.users_get_all()
    return render_template("user/all.html", data=data)

# @admin_only
@required_roles([1])
def user_edit(id: int):
    if request.method == "POST":
        login = request.form.get("login")
        name = request.form.get("name")
        password = request.form.get("password", default="")
        role_id = request.form.get("role")
        print(id, login, name, role_id, password)
        user_controller.user_edit(id, login, name, role_id, password)
        return redirect("/users")
    else:
        data = user_controller.user_get_by_id(id)
        return render_template("user/edit.html", data=data)

# @admin_only
@required_roles([1])
def user_new():
    if request.method == "POST":
        login = request.form.get("login")
        name = request.form.get("name")
        password = request.form.get("password", default="")
        role_id = request.form.get("role")
        user_controller.user_new(login, name, password, role_id)
        return redirect("/users")
    else:
        return render_template("user/new.html")