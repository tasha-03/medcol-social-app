from flask import render_template, request, redirect

from src.database import fetch_groups_names_list, fetch_users_list
from src.utils import admin_only, required_roles
from src.controllers import groups_controller


@required_roles([1])
def groups_all():
    data = groups_controller.groups_get_all()
    return render_template("groups/all.html", data=data)

@required_roles([1])
def group_new():
    if request.method == 'POST':
        code = request.form.get("code")
        name = request.form.get("groupname")
        curatorId = request.form.get("curatorId")
        groups_controller.group_new(code, name, curatorId)
        return redirect("/groups")
    else:
        groups_names_list = fetch_groups_names_list()
        users_dict = fetch_users_list()
        return render_template(
            "groups/new.html",
            groups_names_list=groups_names_list,
            users_dict=users_dict
        )

@required_roles([1])
def group_edit(id: int):
    if request.method == "POST":
        code = request.form.get("code")
        name = request.form.get("groupname")
        curatorId = request.form.get("curatorId")
        groups_controller.group_edit(id, code, name, curatorId)
        return redirect("/groups")
    else:
        groups_names_list = fetch_groups_names_list()
        users_dict = fetch_users_list()
        data = groups_controller.group_get_by_id(id)
        return render_template(
            "groups/edit.html",
            data=data,
            groups_names_list=groups_names_list,
            users_dict=users_dict
        )