import flask_login


class User(flask_login.UserMixin):
    def __init__(self, id, login, name, role_id):
        self.id = id
        self.login = login
        self.name = name
        self.role_id = role_id
