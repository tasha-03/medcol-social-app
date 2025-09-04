import flask_login
from flask import Flask, render_template, redirect, request, abort
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_pyfile("config.cfg")

from src.routes import auth_router
from src.routes import user_router
from src.routes import student_router
from src.routes import groups_router
from src.routes import import_router

from src.controllers.user_controller import user_object_get_by_id


FIO_FILTERING = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЫЭЮЯ"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def user_loader(id):
    return user_object_get_by_id(id)

@app.before_request
def auth_middleware():
    if request.path == "/favicon.ico":
        return
    if request.endpoint is None and not flask_login.current_user.is_authenticated:
        return redirect("/login")
    if request.endpoint is None:
        return abort(404)
    fn = app.view_functions[request.endpoint]
    if not request.endpoint or request.endpoint.rsplit('.', 1)[-1] == 'static':
        return
    if hasattr(fn, 'allowed_anonymous') and fn.allowed_anonymous:
        return
    if flask_login.current_user.is_authenticated:
        return
    return redirect("/login")

@app.errorhandler(404)
def handle_404(e):
    return render_template("404.html")

# @app.before_request
# def handle_admin():
#     if request.path == "/favicon.ico":
#         return
#     fn = app.view_functions[request.endpoint]
#     if hasattr(fn, "admin_only") and fn.admin_only:
#         if flask_login.current_user.role_id != 1:
#             return abort(404)
#         return

@app.before_request
def handle_required_roles():
    if request.path == "/favicon.ico":
        return
    fn = app.view_functions[request.endpoint]
    if hasattr(fn, "required_roles"):
        if flask_login.current_user.role_id not in fn.required_roles:
            return abort(404)
        return
    return

@app.route("/")
def students():
    return redirect("/students")

app.add_url_rule("/login", endpoint='login', methods=['GET', 'POST'], view_func=auth_router.login)
app.add_url_rule("/logout", view_func=auth_router.logout)

app.add_url_rule("/students", view_func=student_router.students_all)
app.add_url_rule("/students/excel", view_func=student_router.students_get_excel)
app.add_url_rule("/students/deleted", view_func=student_router.students_all_deleted)
app.add_url_rule("/students/new", methods=['GET', 'POST'], view_func=student_router.student_new)
app.add_url_rule("/students/<int:id>", methods=['GET', 'POST'], view_func=student_router.student_edit)
app.add_url_rule("/students/<int:id>/delete", methods=['GET', 'POST'], view_func=student_router.student_delete)
app.add_url_rule("/students/<int:id>/restore", methods=['GET', 'POST'], view_func=student_router.student_restore)

app.add_url_rule("/import/excel", methods=['GET', 'POST'], view_func=import_router.import_excel_data)
app.add_url_rule("/import/excel/confirm", methods=['GET', 'POST'], view_func=import_router.import_excel_data_confirm)

# @app.route("/import/excel", methods=['GET', 'POST'])
# def import_excel_data():
#     if request.method == 'POST':
#         file = request.files.get("file")
#         df = db.import_excel_data(file)
#         student_new_many(df)
#         return redirect("/students")
#     else:
#         return render_template("import/excel-import.html")
#
# @app.route("/import/excel/confirm", methods=['POST'])
# def import_excel_data_confirm():
#     if request.method == 'POST':
#         file = request.files.get("file")
#         df = db.import_excel_data(file)
#         return render_template("import/excel-import-results.html", result=df)
#     else:
#         return render_template("import/excel-import.html")

app.add_url_rule("/users", view_func=user_router.users_all)
app.add_url_rule("/users/new", methods=['GET', 'POST'], view_func=user_router.user_new)
app.add_url_rule("/users/<int:id>", methods=['GET', 'POST'], view_func=user_router.user_edit)

app.add_url_rule("/groups", view_func=groups_router.groups_all)
app.add_url_rule("/groups/new", methods=['GET', 'POST'], view_func=groups_router.group_new)
app.add_url_rule("/groups/<int:id>", methods=['GET', 'POST'], view_func=groups_router.group_edit)
