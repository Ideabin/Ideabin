import json

from misc import db
from server.exceptions import *

from flask import (
    make_response,
    jsonify,
    request,
    Blueprint
)

from .models import Comments
from server.users.models import User
from server.ideas.models import Idea

comments_bp = Blueprint('comments', __name__)


@comments_bp.route('/<uuid:idea_id>/comments/', endpoint='list',
                   methods=['GET'])
def get_comments(idea_id):
    """
    Returns a list of comments present in the database for the idea
    """
    # Todo: Add paging to retrieve next 50 comments and so on
    comments = Comments.query.filter_by(idea_id=idea_id).limit(50)

    resp = make_response(json.dumps([c.json for c in comments]), 200)
    resp.mimetype = 'application/json'
    return resp


@comments_bp.route('/<uuid:idea_id>/comments/', endpoint='create',
                   methods=['POST'])
# @login_required
def create_comment(idea_id):
    """
    Creates a new comment with the json data sent
    """
    if not request.json:
        raise InvalidRequest

    desc_md = Parser.string('desc')

    comment = Comments.new(user_id, idea_id, desc)
    return make_response(jsonify(comment.json), 200)


@comments_bp.route('/<uuid:idea_id>/comments/', endpoint='delete',
                   methods=['DELETE'])
# @login_required
def delete_comment(idea_id):
    """
    Delete the comment with matching comment_id
    """
    if not request.json:
        raise InvalidRequest

    comment_id = Parser.uuid('comment_id')

    comment = Comments.query.filter_by(comment_id, user_id, idea_id).first()
    if not comment:
        raise NotFound
    else:
        Comments.delete(comment)

    return make_response('', 204)

# Todo: Update comment data
