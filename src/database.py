import os
import sqlite3
import io
import datetime
import pandas as pd
from flask_login import current_user

from app import app
SQLITE_DB_PATH = app.config.get("SQLITE_DB_PATH")

def fetch_groups_list():
    groups = sqlite3.connect(SQLITE_DB_PATH)
    cursor = groups.cursor()
    if current_user.role_id in [1, 3]:
        cursor.execute("SELECT * FROM Groups")
    else:
        cursor.execute("SELECT * FROM Groups WHERE curatorId=?", (current_user.id,))
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=['id', 'code', 'name', 'curatorId'])

    namelist = df['name'].drop_duplicates().to_list()

    groups_dict = dict()

    for name in namelist:
        groups_dict[name] = df[df['name'] == name][['id', 'code']].to_records(index=False).tolist()
        pass

    return groups_dict

def fetch_groups_list_plain():
    groups = sqlite3.connect(SQLITE_DB_PATH)
    cursor = groups.cursor()
    cursor.execute("SELECT * FROM Groups")
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=['id', 'code', 'name', 'curatorId'])[['id', 'code']]

    groups_dict = dict(df.values)

    return groups_dict

def fetch_groups_names_list():
    with sqlite3.connect(SQLITE_DB_PATH) as groups:
        cursor = groups.cursor()
        cursor.execute(
            'SELECT name FROM "Groups" GROUP BY name'
        )
        data = cursor.fetchall()
        groups_names_list = pd.DataFrame(data, columns=['name'])['name'].tolist()
        return groups_names_list

def fetch_users_list():
    with sqlite3.connect(SQLITE_DB_PATH) as users:
        cursor = users.cursor()
        cursor.execute(
            "SELECT id, name FROM Users ORDER BY name"
        )
        data = cursor.fetchall()
        df = pd.DataFrame(data, columns=['id', 'name'])
        users_dict = dict(df.values)
        return users_dict

# def import_excel_data(file):
#     df = pd.read_excel(file)
#
#     # Updating GROUPS in the DB
#     # groups_list = df['Группа'].drop_duplicates().to_list()
#     # print(groups_list)
#     #
#     # with sqlite3.connect(SQLITE_DB_PATH) as groups:
#     #     cursor = groups.cursor()
#     #     for group in groups_list:
#     #         cursor.execute("INSERT INTO Groups (code) values (?) ON CONFLICT (code) DO NOTHING", (group,))
#     #     groups.commit()
#
#     return df


def create_backup():
    backups_dir = "./backups"
    if not os.path.exists(backups_dir):
        os.makedirs(backups_dir)
    backup_files = [file for file in sorted(os.listdir(backups_dir)) if file.endswith(".sql")]
    if len(backup_files) > 1:
        os.remove(f"{backups_dir}/{backup_files[0]}")

    connection = sqlite3.connect(SQLITE_DB_PATH)
    dt = datetime.datetime.now()
    with io.open(f"{backups_dir}/{dt.strftime('%Y-%m-%d_%H-%M-%S')}_backup.sql", "x", encoding="utf-8") as backup:
        for line in connection.iterdump():
            backup.write(line)

if __name__ == "__main__":
    print(":D")