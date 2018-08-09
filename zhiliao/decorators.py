from functools import wraps
from flask import session,url_for,redirect

def login_requird(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        if session.get("user_id"):
            return func(*args,**kwargs)
        else:
            return redirect(url_for('login'))
    return wrapper