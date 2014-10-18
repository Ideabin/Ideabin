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
from server.votes.models import Vote
from server.subs.models import ISub

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
        for idea in all_ideas[0:50]:
            ideas.append(idea.json)
    else:
        raise NotFound

    resp = make_response(json.dumps(ideas), 200)
    resp.mimetype = 'application/json'
    return resp


@ideas_bp.route('/<uuid:idea_id>', endpoint='id', methods=['GET'])
def get_idea(idea_id):
    """
    Get a specific idea with the matching idea_id
    """

    idea = Idea.query.filter_by(idea_id=idea_id).first()
    if not idea:
        raise NotFound

    return make_response(jsonify(idea.json), 200)


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
    idea = Idea.query.filter_by(idea_id=iid).first()
    if not idea:
        raise NotFound

    Idea.delete(idea)
    return make_response('', 204)


@ideas_bp.route('/<uuid:idea_id>/vote/', endpoint='vote', methods=['POST'])
@login_required
def vote_idea(idea_id):
    """
    Increase the vote count of the idea with matching idea_id.
    """

    idea = Idea.query.filter_by(idea_id=idea_id).first()
    if not idea:
        raise NotFound

    user_id = current_user.user_id

    if idea.user_id == user_id:
        raise Conflict('You can not vote on your own ideas.')

    voted = Vote.query.filter_by(user_id=user_id, idea_id=idea_id).first()
    if not voted:
        Vote.new(user_id, idea_id)
    else:
        Vote.delete(voted)

    return make_response(jsonify({"vote_count": idea.vote_count}), 200)


# Todo: Requires authentication
@ideas_bp.route('/<uuid:iid>/sub', endpoint='subscription', methods=['POST'])
def sub_unsub_idea(iid):
    """
    Subscribes on an idea
    """
    # user_id = get_current_user() # from oauth

    sub = ISub.query.filter_by(user_id=user_id, idea_id=iid).first()
    if not sub:
        ISub.new(user_id, iid)
        return "you are subscribed"
    else:
        ISub.delete(sub)
        return "you are un-subscribed"


# Todo: Update idea
