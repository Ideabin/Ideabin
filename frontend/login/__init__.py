from flask import redirect, url_for
from flask_login import LoginManager, current_user

from server.users.models import User

from functools import wraps

login_manager = LoginManager()
login_manager.login_view = 'login.index'
login_manager.login_message = "Please sign in to access this page."


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id=user_id)
