# Our application and database
from server import app, db
from server.users.models import User

# Some flask goodies
from flask import make_response, jsonify, request

# The model
from .models import Idea

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
        retData, retStatus = {
            "error": "The specified idea does not exist."}, 400

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
            retData, retStatus = {
                "error": "The specified user does not exist."}, 400
            return make_response(jsonify(retData), retStatus)

        Idea.new(retData['title'], retData['desc'], retData['user_id'])
    else:
        retData, retStatus = {
            "error": "The input data sent should be json."}, 400

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
            retData, retStatus = {
                "error": "The specified idea does not exist."}, 400
    else:
        retData, retStatus = {
            "error": "The input data sent should be json."}, 400

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
            retData, retStatus = {
                "error": "The specified idea does not exist."}, 400
    else:
        retData, retStatus = {
            "error": "The input data sent should be json."}, 400

    return make_response(jsonify(retData), retStatus)

# TODO: (i)Update idea
# TODO: (i)Comment on idea


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({
        "error": "Whatever it is that you're looking for - it ain't here son!"
    }), 404)


@app.errorhandler(405)
def not_allowed(error):
    return make_response(jsonify({
        "error": "This method is not allowed for the following URL."
    }), 405)
