import sqlite3

from app import app

SQLITE_DB_PATH = app.config.get("SQLITE_DB_PATH")

from src.bcrypt import hash_password, check_password
from src.classes import User

def users_get_all():
    with sqlite3.connect(SQLITE_DB_PATH) as users:
        cursor = users.cursor()
        cursor.execute(
            "SELECT id, login, name, role, roleId FROM DefaultUsersView"
        )
        data = cursor.fetchall()
        return data

def user_get_by_id(id):
    with sqlite3.connect(SQLITE_DB_PATH) as users:
        cursor = users.cursor()
        cursor.execute("SELECT id, login, name, roleId FROM Users WHERE id=?", (id,))
        data = cursor.fetchone()
        return data

def user_get_by_login(login):
    with sqlite3.connect(SQLITE_DB_PATH) as users:
        cursor = users.cursor()
        cursor.execute("SELECT id, login, name, roleId FROM Users WHERE login=?", (login,))
        data = cursor.fetchone()
        return data

def user_object_get_by_id(id):
    user_data = user_get_by_id(id)
    user = User(
        id=user_data[0],
        login=user_data[1],
        name=user_data[2],
        role_id=user_data[3]
    )
    return user

def user_object_get_by_login(login):
    user_data = user_get_by_login(login)
    user = User(
        id=user_data[0],
        login=user_data[1],
        name=user_data[2],
        role_id=user_data[3]
    )
    return user

def authorize(login, password):
    with sqlite3.connect(SQLITE_DB_PATH) as users:
        cursor = users.cursor()
        cursor.execute(
            "SELECT password FROM Users WHERE login=?",
            (login,))
        user = cursor.fetchone()
        if user:
            hashed_password = user[0]
            return check_password(password, hashed_password)
        return False


def user_new(login, name, password, role_id):

    with sqlite3.connect(SQLITE_DB_PATH) as users:
        cursor = users.cursor()
        if password != "":
            hashed_password = hash_password(password)
            cursor.execute(
                "INSERT INTO Users (login, name, password, roleId) VALUES (?,?,?,?)",
                (login, name, hashed_password, role_id)
            )
        else:
            cursor.execute(
                "INSERT INTO Users (login, name, roleId) VALUES (?,?,?,?)",
                (login, name, role_id)
            )
        users.commit()

def user_edit(id, login, name, role_id, password):
    with sqlite3.connect(SQLITE_DB_PATH) as users:
        cursor = users.cursor()
        if password != "":
            hashed_password = hash_password(password)
            cursor.execute(
                "UPDATE Users SET login=?, name=?, password=?, roleId=? WHERE id=?",
                (login, name, hashed_password, role_id, id)
            )
        else:
            cursor.execute(
                "UPDATE Users SET login=?, name=?, roleId=? WHERE id=?",
                (login, name, role_id, id)
            )
        users.commit()