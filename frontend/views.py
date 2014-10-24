from flask import (
    Blueprint,
    redirect,
    render_template,
    url_for
)

from flask_login import (
    current_user,
    login_required
)

from server.exceptions import *

from server.ideas.models import Idea
from server.ideas.models import User

frontend_bp = Blueprint('frontend', __name__)


@frontend_bp.route('/', endpoint='index')
def homepage():
    if not current_user.is_anonymous():
        return redirect(url_for('frontend.explore'))
    return render_template('index.html')


@frontend_bp.route('/add/', endpoint='add')
def add_idea():
    return render_template('add.html')


@frontend_bp.route('/register/', endpoint='register')
def register():
    return render_template('register.html')


@frontend_bp.route('/profile/', endpoint='profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)


@frontend_bp.route('/explore/', endpoint='explore')
def explore():
    ideas = Idea.query.limit(50)
    return render_template('explore.html', ideas=ideas)


@frontend_bp.route('/u/<string:username>', endpoint='user')
def show_user(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        raise NotFound
    return render_template('user.html', user=user)


@frontend_bp.route('/i/<uuid:idea_id>', endpoint='idea')
def show_idea(idea_id):
    idea = Idea.query.get_or_404(idea_id)
    return render_template('idea.html', idea=idea)
