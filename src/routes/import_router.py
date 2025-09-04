from io import StringIO
import pandas as pd
from flask import request, render_template, redirect, session

from src.controllers import import_controller
from src.utils import required_roles

@required_roles([1])
def import_excel_data():
    if request.method == 'POST':
        file = request.files.get('file')
        df, message = import_controller.parse_excel_file(file)
        session["import_df"] = df.to_json()
        return render_template(
            "import/excel-import-results.html",
            result=df,
            SUPPORTED_IMPORT_FIELDS=import_controller.IMPORT_COLUMNS
        )
    else:
        return render_template("import/excel-import.html")

@required_roles([1])
def import_excel_data_confirm():
    if request.method == 'POST':
        df = pd.read_json(StringIO(session.get("import_df")))
        selected_columns = []
        for i in range(len(df.columns)):
            value = request.form.get(f"{i}-select")
            if value != "":
                selected_columns.append((i, value))

        selected_records = request.form.getlist("selected_records", type=int)
        import_controller.import_excel_data(df, selected_columns, selected_records)

        return redirect("/students")
    else:
        return render_template("import/excel-import.html")