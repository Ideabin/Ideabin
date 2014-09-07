# Our application and database
from server import app, db
from server.exceptions import (
    NotFound,
    ServerError,
    InvalidRequest,
)

import json

# Some flask goodies
from flask import make_response, jsonify, request

# The models
from .models import Idea
from server.users.models import User

# A uuid url converter for flask
from misc.flask_uuid import FlaskUUID
FlaskUUID(app)


@app.route('/api/ideas/', endpoint='list_ideas', methods=['GET'])
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


@app.route('/api/ideas/<uuid:uid>', endpoint='list_idea', methods=['GET'])
def get_idea(uid):
    """
    Get a specific idea with the matching idea_id
    """

    spark = Idea.query.filter_by(idea_id=uid).first()
    if not spark:
        raise NotFound

    return make_response(jsonify(spark.json), 200)


@app.route('/api/ideas/', endpoint='create_idea', methods=['POST'])
def create_idea():
    """
    Creates a new idea with the json data sent
    """
    if not request.json:
        raise InvalidRequest

    u = User.query.filter_by(user_id=request.json['user_id']).first()
    if not u:
        raise InvalidRequest('The specified user does not exist.')

    i = Idea.new(
        request.json['title'],
        request.json['desc'],
        request.json['user_id']
    )

    return make_response(jsonify(i.json), 200)


# Todo: Requires authentication
@app.route('/api/ideas/<uuid:iid>', endpoint='delete_idea', methods=['DELETE'])
def delete_idea(iid):
    """
    Delete the idea with matching idea_id.
    """
    # user_id = get_current_user() # from oauth
    #
    # Todo: Delete the idea only if it was created by
    # the current user.

    spark = Idea.query.filter_by(idea_id=iid).first()
    if not spark:
        raise NotFound

    i = Idea.delete(spark)

    return make_response(jsonify(i.json), 200)


# Todo: Requires authentication
@app.route('/api/ideas/<uuid:iid>/vote', endpoint='upvote', methods=['POST'])
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
