# Our application and database
from server import app, db

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
        # Todo: Add paging to retrieve next 50 users and so on
        for spark in all_ideas[0:50]:
            ideas.append(spark.json)

        retData, retStatus = {"ideas": ideas}, 200
    else:
        retData = {"error": "There are no ideas in the database."}

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
        retData = {"error": "The specified user does not exist."}

    return make_response(jsonify(retData), retStatus)


@app.route('/api/ideas/', endpoint='create_idea', methods=['POST'])
def create_idea():
    """
    Creates a new idea with the json data sent
    """

    if request.json:
        retData, retStatus = request.json, 201
    else:
        retData, retStatus = {
            "error": "The input data sent should be json."}, 400

    Idea.new(retData['title'], retData['user_id'])

    return make_response(jsonify(retData), retStatus)


@app.route('/api/ideas/<uuid:uid>', endpoint='delete_idea', methods=['DELETE'])
def delete_idea(uid):
    """
    Delete the idea with matching idea_id
    """

    spark = Idea.query.filter_by(idea_id=uid).first()
    if spark:
        retData, retStatus = {"idea": spark.json}, 200
    else:
        retData, retStatus = {
            "error": "The specified user does not exist."}, 400

    Idea.delete(spark)

    return make_response(jsonify(retData), retStatus)

# TODO: Voting endpoint
# TODO: Update idea
# TODO: Comment on idea


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
