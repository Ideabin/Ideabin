# Our application and database
from misc import db
from server.exceptions import (
    NotFound,
    ServerError,
    InvalidRequest,
)

import json

# Some flask goodies
from flask import make_response, jsonify, request, Blueprint

# The models
from .models import Comment
from server.users.models import User
from server.ideas.models import Idea

comments_bp = Blueprint('comments', __name__)


@comments_bp.route('/<uuid:iid>/comment/', endpoint='comments', methods=['GET'])
def get_comments(iid):
    """
    Sends a list of comments present in the database for the idea
    """
    all_comments = Comment.query.filter_by(idea_id=iid).all()
    comments = []
    if all_comments:
        # Todo: Add paging to retrieve next 50 ideas and so on
        for cmnt in all_comments[0:50]:
            comments.append(cmnt.json)
    else:
        raise NotFound

    resp = make_response(json.dumps(comments), 200)
    resp.mimetype = 'application/json'
    return resp


# Todo: Requires authentication
@comments_bp.route('/<uuid:iid>/comment/', endpoint='create', methods=['POST'])
def create_comment(iid):
    """
    Creates a new comment with the json data sent
    """
    if not request.json:
        raise InvalidRequest

    # user_id = get_current_user() # from oauth

    cmnt = Comment.new(
        user_id,
        iid
        request.json['desc'],
        request.json['desc'],
    )

    return make_response(jsonify(cmnt.json), 200)


# Todo: Requires authentication
@comments_bp.route('/<uuid:iid>/comment/>', endpoint='delete', methods=['DELETE'])
def delete_comment(iid):
    """
    Delete the comment with matching comment_id
    """
    # user_id = get_current_user() # from oauth

    if not request.json:
        raise InvalidRequest

    cmnt = Comment.query.filter_by(
        comment_id=request.json['comment_id'],
        user_id=user_id,
        idea_id=iid
    ).first()
    if not cmnt:
        raise NotAllowed
    else:
        cmnt = Comment.delete(cmnt)

    return make_response(jsonify(cmnt.json), 200)

# todo: update comment data
