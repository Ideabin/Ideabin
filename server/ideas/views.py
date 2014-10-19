import json

from flask import (
    make_response,
    jsonify,
    request,
    Blueprint
)

from flask_login import (
    login_required,
    current_user
)

from misc import db
from server.exceptions import *

from misc.parser import Parser

from .models import Idea
from server.users.models import User

ideas_bp = Blueprint('ideas', __name__)


@ideas_bp.route('/', endpoint='list', methods=['GET'])
def get_ideas():
    """
    Sends a list of ideas present in the database
    """
    all_ideas = Idea.query.all()
    ideas = []
    if all_ideas:
        # Todo: Add paging to retrieve next 50 ideas and so on
        for spark in all_ideas[0:50]:
            ideas.append(spark.json)
    else:
        raise NotFound

    resp = make_response(json.dumps(ideas), 200)
    resp.mimetype = 'application/json'
    return resp


@ideas_bp.route('/<uuid:uid>', endpoint='id', methods=['GET'])
def get_idea(uid):
    """
    Get a specific idea with the matching idea_id
    """

    spark = Idea.query.filter_by(idea_id=uid).first()
    if not spark:
        raise NotFound

    return make_response(jsonify(spark.json), 200)


@ideas_bp.route('/', endpoint='create', methods=['POST'])
@login_required
def create_idea():
    """
    Creates a new idea with the json data sent
    """
    if not request.json:
        raise InvalidRequest

    # Todo: These should probably be a string with some max len
    title = Parser.anything('title')
    desc = Parser.anything('desc')
    status = Parser.string('status', max=20, optional=True)
    tags = Parser.list('tags', optional=True)

    new = Idea.new(title, desc, current_user.user_id, tags)

    return make_response(jsonify(new.json), 201)


# Todo: Requires authentication
@ideas_bp.route('/<uuid:iid>', endpoint='delete', methods=['DELETE'])
# @login_required
def delete_idea(iid):
    """
    Delete the idea with matching idea_id.
    """
    spark = Idea.query.filter_by(idea_id=iid).first()
    if not spark:
        raise NotFound

    Idea.delete(spark)
    return make_response('', 204)


# Todo: Requires authentication
@ideas_bp.route('/<uuid:iid>/vote', endpoint='upvote', methods=['POST'])
def vote_idea(iid):
    """
    Increase the vote count of the idea with matching idea_id.
    """
    # user_id = get_current_user() # from oauth
    #
    # Todo: Check whether the user has already voted
    # and decide whether to upvote or downvote.

    spark = Idea.query.filter_by(idea_id=iid).first()
    if not spark:
        raise NotFound

    i = Idea.voting(spark)

    return make_response(jsonify(i.json), 200)

# Todo: Update idea
# Todo: Comment on idea
