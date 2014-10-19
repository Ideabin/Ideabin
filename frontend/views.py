from flask import (
    render_template,
    Blueprint
)

frontend_bp = Blueprint('frontend', __name__)


@frontend_bp.route('/', endpoint='index')
def homepage():
    return render_template('index.html')


@frontend_bp.route('/add/', endpoint='add')
def add_idea():
    return render_template('add_idea.html')


@frontend_bp.route('/register/', endpoint='register')
def register():
    return render_template('register.html')


@frontend_bp.route('/explore/', endpoint='explore')
def register():
    return render_template('explore.html')
