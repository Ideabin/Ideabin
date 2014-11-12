import json

from misc import db
from server.exceptions import *

from flask import (
    make_response,
    jsonify,
    request,
    Blueprint
)

from flask_login import (
    current_user,
    login_required
)

from server.users.models import User
from server.ideas.models import Idea

from server.notifications.models import (
    NotifIdeaByUser,
    NotifIdeaUpdate,
    NotifCommentByUser,
    NotifCommentOnIdea
)

notifs_bp = Blueprint('notifs', __name__)


@notifs_bp.route('/', endpoint='list', methods=['GET'])
@login_required
def get_notifs():
    """
    Returns notifications for the user
    """

    notifs = NotifIdeaByUser.query \
        .filter_by(user_to=current_user.user_id, read=False) \
        .limit(50).all()

    notifs += NotifIdeaUpdate.query \
        .filter_by(user_to=current_user.user_id, read=False) \
        .limit(50).all()

    notifs += NotifCommentByUser.query \
        .filter_by(user_to=current_user.user_id, read=False) \
        .limit(50).all()

    notifs += NotifCommentOnIdea.query \
        .filter_by(user_to=current_user.user_id, read=False) \
        .limit(50).all()

    resp = make_response(json.dumps([n.json for n in notifs]), 200)
    resp.mimetype = 'application/json'
    return resp
