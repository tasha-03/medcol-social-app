def allowed_anonymous(f):
    f.allowed_anonymous = True
    return f

def admin_only(f):
    f.admin_only = True
    return f

def required_roles(role_ids: [int]):
    def decorator(f):
        f.required_roles = role_ids
        return f
    return decorator