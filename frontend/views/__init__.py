from flask import (
    render_template,
    Blueprint
)

frontend_bp = Blueprint('frontend', __name__)


@frontend_bp.route('/')
def homepage():
    return render_template('index.html')


@frontend_bp.route('/add/')
def add_idea():
    return render_template('add_idea.html')
