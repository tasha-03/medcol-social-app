import io

import flask_login
import pandas as pd
from datetime import datetime
from flask import render_template, request, redirect, abort, Response

from src.controllers import student_controller, groups_controller
from src import database as db
from src.student_structure import STUDENT_STRUCTURE, STUDENT_RECORD_FIELDS, STUDENT_FIELDS, STUDENT_FIELDSETS_FILTER
from urllib.parse import unquote

from src.utils import admin_only, required_roles

FIO_FILTERING = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЫЭЮЯ"

def students_all():
    groups = db.fetch_groups_list()

    filter_options = {}

    filter_letter = request.args.get("filter_letter", default="")
    filter_group = request.args.get("filter_group", default="")

    page = request.args.get("page", type=int, default=1)
    limit = request.args.get("limit", type=int, default=150)

    age_b = request.args.get("age_b", type=int, default=0)
    age_t = request.args.get("age_t", type=int, default=100)

    filter_fields = {}
    keys = list(request.args.keys())
    for k in keys:
        if k in STUDENT_FIELDS.keys():
            field_type = STUDENT_FIELDS[k].get("type")
            v = request.args.get(k)
            filter_fields[k] = unquote(v)
            if field_type == "int" and v != "all":
                filter_fields[k] = int(v)

    if filter_letter:
        filter_letter = unquote(filter_letter)
        filter_options["filter_letter"] = filter_letter

    if filter_group:
        filter_options["filter_group"] = int(filter_group)


    data, record_count = student_controller.students_get_all(
        filter_letter=filter_letter,
        filter_group=filter_group,
        page=page,
        limit=limit,
        filter_fields=filter_fields,
        age_b=age_b,
        age_t=age_t
    )

    return render_template(
        "student/all.html",
        filter_options=filter_options,
        data=data,
        FIO_FILTERING=FIO_FILTERING,
        STUDENT_STRUCTURE=STUDENT_STRUCTURE,
        STUDENT_FIELDSETS_FILTER=STUDENT_FIELDSETS_FILTER,
        GROUPS_FILTERING=groups,
        filter_fields=filter_fields,
        record_count=record_count,
        page=page,
        limit=limit,
        age_b=age_b,
        age_t=age_t
    )

@required_roles([1])
def student_new():
    if request.method == 'POST':
        fio = request.form['fio']
        birthdate = request.form['birthdate']
        group_id = request.form['group']
        student_controller.student_new(fio=fio, birthdate=birthdate, group_id=group_id)
        return redirect("/students")
    else:
        groups = db.fetch_groups_list()
        return render_template(
            "student/new.html",
            GROUPS_FILTERING=groups
        )

def student_edit(id: int):
    if flask_login.current_user.role_id in [1, 2]:
        if request.method == 'POST':
            data = {}
            keys = list(request.form.keys())
            for k in keys:
                v = request.form.get(k)
                data[k] = v
            student_controller.student_edit(id=id, data=data)
            return redirect("/students")
        else:
            groups = db.fetch_groups_list()
            data = student_controller.student_get_by_id(id)

            if data is None:
                return abort(404)
            return render_template(
                "student/edit.html",
                data=data,
                STUDENT_STRUCTURE=STUDENT_STRUCTURE,
                GROUPS_FILTERING=groups
            )
    else:
        data = student_controller.student_get_by_id(id)
        if data is None:
            return abort(404)
        groups = db.fetch_groups_list()
        return render_template(
            "student/details.html",
            data=data,
            STUDENT_STRUCTURE=STUDENT_STRUCTURE,
            GROUPS_FILTERING=groups
        )

@required_roles([1])
def student_delete(id: int):
    if request.method == 'POST':
        student_controller.student_delete_soft(id)
        return redirect("/students")
    else:
        return render_template("student/delete.html")


@required_roles([1])
def student_restore(id: int):
    if request.method == 'POST':
        student_controller.student_restore(id)
        return redirect("/students")
    else:
        return render_template("student/restore.html")

@required_roles([1])
def students_all_deleted():
    groups = db.fetch_groups_list()

    filter_options = {}

    filter_letter = request.args.get("filter_letter", default="")
    filter_group = request.args.get("filter_group", default="")

    page = request.args.get("page", type=int, default=1)
    limit = request.args.get("limit", type=int, default=150)

    age_b = request.args.get("age_b", type=int, default=0)
    age_t = request.args.get("age_t", type=int, default=100)

    filter_fields = {}
    keys = list(request.args.keys())
    for k in keys:
        if k in STUDENT_FIELDS.keys():
            field_type = STUDENT_FIELDS[k].get("type")
            v = request.args.get(k)
            filter_fields[k] = unquote(v)
            if field_type == "int" and v != "all":
                filter_fields[k] = int(v)

    if filter_letter:
        filter_letter = unquote(filter_letter)
        filter_options["filter_letter"] = filter_letter

    if filter_group:
        filter_options["filter_group"] = int(filter_group)

    data, record_count = student_controller.students_get_all(
        filter_letter=filter_letter,
        filter_group=filter_group,
        page=page,
        limit=limit,
        filter_fields=filter_fields,
        age_b=age_b,
        age_t=age_t,
        deleted=True
    )
    return render_template(
        "student/all_deleted.html",
        filter_options=filter_options,
        data=data,
        FIO_FILTERING=FIO_FILTERING,
        STUDENT_STRUCTURE=STUDENT_STRUCTURE,
        STUDENT_FIELDSETS_FILTER=STUDENT_FIELDSETS_FILTER,
        GROUPS_FILTERING=groups,
        filter_fields=filter_fields,
        record_count=record_count,
        page=page,
        limit=limit,
        age_b=age_b,
        age_t=age_t
    )

def students_get_excel():
    filter_options = {}

    filter_letter = request.args.get("filter_letter", default="")
    filter_group = request.args.get("filter_group", default="")

    age_b = request.args.get("age_b", type=int, default=0)
    age_t = request.args.get("age_t", type=int, default=100)

    filter_fields = {}
    keys = list(request.args.keys())
    for k in keys:
        if k in STUDENT_FIELDS.keys():
            field_type = STUDENT_FIELDS[k].get("type")
            v = request.args.get(k)
            filter_fields[k] = unquote(v)
            if field_type == "int" and v != "all":
                filter_fields[k] = int(v)

    if filter_letter:
        filter_letter = unquote(filter_letter)
        filter_options["filter_letter"] = filter_letter

    if filter_group:
        filter_options["filter_group"] = int(filter_group)

    df = student_controller.students_export_to_excel(
        filter_letter=filter_letter,
        filter_group=filter_group,
        filter_fields=filter_fields,
        age_b=age_b,
        age_t=age_t
    )

    buffer = io.BytesIO()
    writer = pd.ExcelWriter(buffer, engine="xlsxwriter", date_format="yyyy-mm-dd", datetime_format="yyyy-mm-dd")


    filter_df = pd.DataFrame.from_dict(data=filter_fields, columns=["Значение"], orient="index")
    filter_df["Поле"] = filter_df.index
    filter_df["Поле"] = filter_df["Поле"].apply(
        lambda x: STUDENT_FIELDS[x]["label"]
    )

    filter_df.loc[len(filter_df)] = [age_b, "Минимальный возраст"]
    filter_df.loc[len(filter_df)] = [age_t, "Максимальный возраст"]

    filter_df = filter_df[["Поле", "Значение"]]

    filter_df.to_excel(writer, sheet_name="Параметры фильтрации", index=False)

    df.index = df.index + 1

    df["Дата рождения"] = df["Дата рождения"].apply(
        lambda x: datetime.strptime(x, "%Y-%m-%d")
    )

    df.to_excel(writer, sheet_name="Данные студентов")

    (max_row, max_col) = df.shape

    writer.sheets["Данные студентов"].autofilter(0, 2, max_row, max_col - 1)

    writer.sheets["Параметры фильтрации"].autofit()
    writer.sheets["Данные студентов"].autofit()

    writer.close()
    buffer.seek(0)

    headers = {
        "Content-Disposition": "attachment; filename=output.xlsx",
        "Content-type": "application/vnd.ms-excel"
    }

    return Response(buffer.getvalue(), mimetype="application/vnd.ms-excel", headers=headers)