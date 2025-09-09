import sqlite3

from app import app


SQLITE_DB_PATH = app.config.get("SQLITE_DB_PATH")

def groups_get_all():
    with sqlite3.connect(SQLITE_DB_PATH) as groups:
        cursor = groups.cursor()
        cursor.execute(
            "SELECT * from DefaultGroupsView"
        )
        data = cursor.fetchall()
        return data

def group_get_by_id(id):
    with sqlite3.connect(SQLITE_DB_PATH) as groups:
        cursor = groups.cursor()
        cursor.execute(
            "SELECT * from DefaultGroupsView WHERE id=?",
            (id,)
        )
        data = cursor.fetchone()
        return data

def group_get_by_code(code: str):
    with sqlite3.connect(SQLITE_DB_PATH) as groups:
        cursor = groups.cursor()
        cursor.execute(
            "SELECT * from DefaultGroupsView WHERE code=?",
            (code,)
        )
        data = cursor.fetchone()
        return data

def group_new(code, name, curatorId):
    with sqlite3.connect(SQLITE_DB_PATH) as groups:
        cursor = groups.cursor()
        cursor.execute(
            "INSERT INTO [Groups] (code,name,curatorId) VALUES (?,?,?) RETURNING id",
            (code, name, curatorId)
        )
        row = cursor.fetchone()
        groups.commit()
        return row[0] if row else None

def group_edit(id, code, name, curatorId):
    with sqlite3.connect(SQLITE_DB_PATH) as groups:
        cursor = groups.cursor()
        cursor.execute(
            "UPDATE Groups SET code=?, name=?, curatorId=? WHERE id=?",
            (code, name, curatorId, id)
        )
        groups.commit()

def groups_get_by_curator_id(id):
    with sqlite3.connect(SQLITE_DB_PATH) as groups:
        cursor = groups.cursor()
        cursor.execute(
            "SELECT * from DefaultGroupsView WHERE curatorId=?",
            (id,)
        )
        data = cursor.fetchall()
        return data