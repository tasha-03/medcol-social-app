import sqlite3

import flask_login
import pandas
from flask_login import current_user

from app import app
from src.controllers.groups_controller import groups_get_by_curator_id

SQLITE_DB_PATH = app.config.get("SQLITE_DB_PATH")

from src.database import fetch_groups_list, fetch_groups_list_plain
from src.student_structure import STUDENT_RECORD_FIELDS, STUDENT_STRUCTURE, STUDENT_FIELDSETS_FILTER, STUDENT_FIELDS


def to_yes_no(x):
    if x in [1, "1"]:
        return "Да"
    return "Нет"

def students_get_all(
    filter_letter: str,
    filter_group: str,
    page: int,
    limit: int,
    filter_fields: dict,
    age_b: int = 0,
    age_t: int = 100,
    deleted: bool = False
):
    search_view = "DefaultStudentsView"
    if deleted:
        search_view = "DeletedStudentsView"

    select_expression = f"SELECT id, fio, [group], birthdate, addedByUser, modifiedByUser, lastModified FROM {search_view}"
    filter_options = {}

    filter_options["age"] = f"(date('now') - date(birthdate)) >= {age_b} and (date('now') - date(birthdate)) <= {age_t}"

    if current_user.role_id not in [1, 3]:
        filter_options["curator_id"] = f"curatorId={current_user.id}"

    if filter_letter:
        filter_options["filter_letter"] = f"fio LIKE '{filter_letter}%'"

    if filter_group:
        filter_options["filter_group"] = f"groupId={filter_group}"

    for field, value in filter_fields.items():
        if value == "all":
            continue
        if value == "":
            filter_options[field] = f"{field} IS NULL"
        else:
            filter_options[field] = f"{field}='{value}'"

    filter_expression = ""

    if len(filter_options) == 0:
        pass
    if len(filter_options) == 1:
        filter_expression = filter_expression + " WHERE " + next(iter(filter_options.values()))
    if len(filter_options) > 1:
        filter_expression = filter_expression + " WHERE " + " AND ".join(filter_options.values())

    if limit > 0:
        limit_expression = f" LIMIT {str(limit)} OFFSET {(page - 1) * limit}"
    else:
        limit_expression = ""

    print(select_expression + filter_expression + limit_expression)

    with sqlite3.connect(SQLITE_DB_PATH) as students:
        cursor = students.cursor()
        cursor.execute(
            select_expression + filter_expression + limit_expression
        )
        data = cursor.fetchall()
        cursor.execute(
            f"SELECT count(*) from {search_view}" + filter_expression
        )
        record_count = cursor.fetchone()[0]
        return data, record_count

def student_get_by_id(id):
    with sqlite3.connect(SQLITE_DB_PATH) as students:
        cursor = students.cursor()
        if current_user.role_id in [1, 3]:
            cursor.execute("SELECT * FROM Students WHERE id=?", (id,))
        else:
            cursor.execute(
                "SELECT * FROM Students WHERE id=? AND groupId IN(SELECT id FROM [Groups] WHERE curatorId=?)",
                (id, current_user.id)
            )
        data = cursor.fetchone()
        if data:
            df = pandas.DataFrame(data=[data], columns=STUDENT_RECORD_FIELDS)
            student_data = df.to_dict(orient="records")[0]

            return student_data
        return data

def student_new(fio, birthdate, group_id):
    with sqlite3.connect(SQLITE_DB_PATH) as students:
        cursor = students.cursor()
        cursor.execute(
            "INSERT INTO Students (fio,birthdate,groupId,addedByUser,modifiedByUser) VALUES (?,?,?,?,?)",
            (fio, birthdate, group_id,flask_login.current_user.id,flask_login.current_user.id)
        )
        students.commit()

def student_new_many(students_df: pandas.DataFrame):
    sql_expression = "INSERT INTO Students (fio,birthdate,groupId,addedByUser,modifiedByUser) VALUES "
    groups = dict((v, k) for k, v in fetch_groups_list_plain().items())
    data_rows = []
    for row in students_df.itertuples(index=False):
        date_parts = row[2].split(".")
        date_string = f"{date_parts[2]}-{date_parts[1]}-{date_parts[0]}"
        data_rows.append(f"('{row[1]}','{date_string}',{groups[row[3]]},{current_user.id},{current_user.id})")

    with sqlite3.connect(SQLITE_DB_PATH) as students:
        cursor = students.cursor()
        cursor.execute(sql_expression + ",".join(data_rows))
        students.commit()


def student_edit(id, data: dict):
    data_str = ",".join([f"{k}='{v}'" for k,v in data.items()])

    with sqlite3.connect(SQLITE_DB_PATH) as students:
        cursor = students.cursor()
        cursor.execute(
            f"UPDATE Students SET {data_str}, modifiedByUser=? WHERE id=?", (current_user.id,id)
        )
        students.commit()

def student_delete_soft(id):
    with sqlite3.connect(SQLITE_DB_PATH) as students:
        cursor = students.cursor()
        cursor.execute("UPDATE Students SET deleted=1, modifiedByUser=? WHERE id=?", (current_user.id,id))
        students.commit()

def student_restore(id):
    with sqlite3.connect(SQLITE_DB_PATH) as students:
        cursor = students.cursor()
        cursor.execute("UPDATE Students SET deleted=0, modifiedByUser=? WHERE id=?", (current_user.id,id))
        students.commit()

def students_export_to_excel(
    filter_letter: str,
    filter_group: str,
    filter_fields: dict,
    age_b: int = 0,
    age_t: int = 100,
    deleted: bool = False
):
    filter_options = {}

    filter_options["deleted"] = f"deleted={1 if deleted else 0}"

    filter_options["age"] = f"(date('now') - date(birthdate)) >= {age_b} and (date('now') - date(birthdate)) <= {age_t}"

    if current_user.role_id not in [1, 3]:
        curr_id = current_user.id
        groups = groups_get_by_curator_id(curr_id)
        filter_options["filter_group"] = f"groupId IN ({','.join([f'{group[0]}' for group in groups])})"

    if filter_letter:
        filter_options["filter_letter"] = f"fio LIKE '{filter_letter}%'"

    if filter_group:
        filter_options["filter_group"] = f"groupId={filter_group}"

    for field, value in filter_fields.items():
        if value == "all":
            continue
        if value == "":
            filter_options[field] = f"{field} IS NULL"
        else:
            filter_options[field] = f"{field}='{value}'"

    filter_expression = ""

    if len(filter_options) == 0:
        pass
    if len(filter_options) == 1:
        filter_expression = filter_expression + " WHERE " + next(iter(filter_options.values()))
    if len(filter_options) > 1:
        filter_expression = filter_expression + " WHERE " + " AND ".join(filter_options.values())

    with sqlite3.connect(SQLITE_DB_PATH) as students:
        cursor = students.cursor()
        cursor.execute(
            "SELECT * FROM Students" + filter_expression + " ORDER BY fio ASC"
        )
        data = cursor.fetchall()

    if data:
        groups_dict = fetch_groups_list_plain()
        STUDENT_RECORD_FIELDS_LABELS = [v["label"] for k,v in STUDENT_FIELDS.items()]

        df = pandas.DataFrame(data=data, columns=STUDENT_RECORD_FIELDS_LABELS)
        df = df.drop(columns=[
            STUDENT_FIELDS["id"]["label"],
            STUDENT_FIELDS["deleted"]["label"],
            STUDENT_FIELDS["addedByUser"]["label"],
            STUDENT_FIELDS["modifiedByUser"]["label"],
            STUDENT_FIELDS["lastModified"]["label"]
        ])

        df[STUDENT_FIELDS["groupId"]["label"]] = df[STUDENT_FIELDS["groupId"]["label"]].apply(
            lambda groupId: groups_dict[groupId]
        )
        df[STUDENT_FIELDS["dormitory"]["label"]] = df[STUDENT_FIELDS["dormitory"]["label"]].apply(to_yes_no)
        df[STUDENT_FIELDS["transportPass"]["label"]] = df[STUDENT_FIELDS["transportPass"]["label"]].apply(to_yes_no)
        df[STUDENT_FIELDS["svoChild"]["label"]] = df[STUDENT_FIELDS["svoChild"]["label"]].apply(to_yes_no)

        return df
    return data