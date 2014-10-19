from flask import (
    Blueprint,
    request,
    redirect,
    render_template,
    url_for,
    session,
    flash
)

from flask_login import (
    login_user,
    logout_user,
    login_required
)

login_bp = Blueprint('login', __name__)
logout_bp = Blueprint('logout', __name__)

from server.users.models import User


@login_bp.route('/', endpoint='index', methods=['GET', 'POST'])
def login_handler():

    if request.method == 'GET':
        return render_template('login.html')

    username = request.form['username']
    password = request.form['password']

    # Todo: (1) Turn this into a raw SQL query
    registered_user = User.get(username=username, password=password)

    if registered_user is None:
        flash('Username or Password is invalid', 'error')
        return redirect(url_for('login.index'))

    # Todo: Update the last_login_on field to current timestamp
    login_user(registered_user)
    return redirect(request.args.get('next') or url_for('frontend.index'))


@logout_bp.route('/', endpoint='logout')
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('frontend.index'))
