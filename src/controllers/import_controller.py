import sqlite3
from datetime import timedelta

from pandas import DataFrame
from werkzeug.datastructures import FileStorage
import pandas as pd
from flask_login import current_user

from src.controllers import groups_controller, student_controller

IMPORT_COLUMNS = {
    "fio": "ФИО",
    "birthdate": "Дата рождения",
    "groupId": "Группа"
}


def parse_excel_file(file: FileStorage) -> tuple[DataFrame, str]:
    file_format = file.filename.split(".")[-1]
    df: DataFrame = DataFrame()
    message = "OK"
    if file_format in ["xlsx", "xls"]:
        df = pd.read_excel(file)
    elif file_format == "csv":
        df = pd.read_csv(file.stream)
    else:
        message = "Wrong file format. Accepted file formats: .xlsx, .xls, .csv"
    return df, message

def import_excel_data(
        df: DataFrame,
        selected_columns: list[tuple[int,str]],
        selected_records: list[int]
):
    print(df)

    columns_dict = {}
    for sel_col, col_name in selected_columns:
        if col_name not in columns_dict:
            columns_dict[col_name] = []
        columns_dict[col_name].append(sel_col)

    final_df: DataFrame = DataFrame(columns=list(IMPORT_COLUMNS.keys()))

    selected_df: DataFrame = df.iloc[selected_records]
    for col in list(IMPORT_COLUMNS.keys()):
        if col in columns_dict.keys():
            if len(columns_dict[col]) > 1:
                cols = [selected_df.columns[i] for i in columns_dict[col]]
                final_df[col] = selected_df[cols].agg(" ".join, axis=1)
            else:
                col_name = selected_df.columns[columns_dict[col][0]]
                final_df[col] = selected_df[col_name]

    final_df["birthdate"] = pd.to_datetime(final_df["birthdate"], unit="ms", utc=True)
    final_df["birthdate"] = final_df["birthdate"] + timedelta(hours=3)
    final_df["birthdate"] = final_df["birthdate"].dt.strftime("%Y-%m-%d")

    print(final_df)

    groups_list: list[str] = final_df["groupId"].drop_duplicates().to_list()

    for i in range(len(groups_list)):
        groups_list[i] = groups_list[i].capitalize()

    print(groups_list)

    for group in groups_list:
        try:
            ind = groups_controller.group_new(code=group, name="", curatorId=current_user.id)
        except sqlite3.IntegrityError:
            ind = groups_controller.group_get_by_code(group)[0]
        final_df.loc[final_df["groupId"] == group, "groupId"] = ind

    print(final_df)
    for _, record in final_df.iterrows():
        student_controller.student_new(
            fio=record["fio"],
            group_id=record["groupId"],
            birthdate=record["birthdate"]
        )
