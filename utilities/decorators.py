from flask import redirect, url_for, session
import functools


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if session == {}:
            return redirect(url_for('login'))
        return view(**kwargs)
    return wrapped_view
