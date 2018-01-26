from functools import wraps

from flask import session, redirect, request, url_for


def requires_login(func):
    @wraps(func)
    def decorated_func(*args, **kwargs):
        if session['email'] is None or 'email' not in session.keys():
            return redirect(url_for("users.login_user", next=request.path))
        return func(*args, **kwargs)
    return decorated_func
