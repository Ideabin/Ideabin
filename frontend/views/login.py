from flask import (
    render_template,
    Blueprint
)

login_bp = Blueprint('login', __name__)


@login_bp.route('/')
def homepage():
    return render_template('login.html')
