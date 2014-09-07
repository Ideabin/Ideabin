# Our application and database
from server import app, db
from server.exceptions import NotFound, InvalidRequest

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
    if all_ideas:
        ideas = []
        # Todo: (i)Add paging to retrieve next 50 ideas and so on
        for spark in all_ideas[0:50]:
            ideas.append(spark.json)

        retData, retStatus = {"ideas": ideas}, 200
    else:
        retData, retStatus = {
            "error": "There are no ideas in the database."}, 400

    return make_response(jsonify(retData), retStatus)


@app.route('/api/ideas/<uuid:uid>', endpoint='list_idea', methods=['GET'])
def get_idea(uid):
    """
    Get a specific idea with the matching idea_id
    """

    spark = Idea.query.filter_by(idea_id=uid).first()
    if spark:
        retData, retStatus = {"idea": spark.json}, 200
    else:
        raise NotFound

    return make_response(jsonify(retData), retStatus)


@app.route('/api/ideas/', endpoint='create_idea', methods=['POST'])
def create_idea():
    """
    Creates a new idea with the json data sent
    """
    if request.json:
        retData, retStatus = request.json, 201

        u = User.query.filter_by(user_id=retData['user_id']).first()
        if not u:
            raise InvalidRequest('The specified user does not exist.')

        Idea.new(retData['title'], retData['desc'], retData['user_id'])
    else:
        raise InvalidRequest

    return make_response(jsonify(retData), retStatus)


# Todo: Requires authentication
@app.route('/api/ideas/<uuid:iid>', endpoint='delete_idea', methods=['DELETE'])
def delete_idea(iid):
    """
    Delete the idea with matching idea_id.
    """
    if request.json:
        retData, retStatus = request.json, 201

        # user_id = get_current_user() # from oauth
        #
        # Todo: Delete the idea only if it was created by
        # the current user.

        spark = Idea.query.filter_by(idea_id=iid).first()
        if spark:
            Idea.delete(spark)
        else:
            raise NotFound
    else:
        raise InvalidRequest

    return make_response(jsonify(spark.json), 200)


# Todo: Requires authentication
@app.route('/api/ideas/<uuid:iid>/vote', endpoint='upvote', methods=['POST'])
def vote_idea(iid):
    """
    Increase the vote count of the idea with matching idea_id.
    """
    if request.json:
        retData, retStatus = request.json, 201

        # user_id = get_current_user() # from oauth
        #
        # Todo: Check whether the user has already voted
        # and decide whether to upvote or downvote.

        spark = Idea.query.filter_by(idea_id=iid).first()
        if spark:
            Idea.voting(spark)
        else:
            raise NotFound
    else:
        raise InvalidRequest

    return make_response(jsonify(spark.json), 200)

# TODO: (i)Update idea
# TODO: (i)Comment on idea
