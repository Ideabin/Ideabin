# Our application and database
from server import app, db

# Some flask goodies
from flask import make_response, jsonify, request

# The model
from .models import User

# A uuid url converter for flask
from misc.flask_uuid import FlaskUUID
FlaskUUID(app)


# Note: This route will probably be taken over by
# our client - the ideabin website.
@app.route('/')
def index():
    return make_response(jsonify({
        "message": "If you're looking for the IdeaBin api, \
                     start at the /api endpoint."
    }), 200)


@app.route('/api/')
def api_begins():
    return make_response(jsonify({
        "message": "The api is currently being worked on.",
        "methods":
        {
            "GET":
            [
                "/api/users/",
                "/api/users/{user_id}",
                "/api/ideas/",
                "/api/ideas/{idea_id}"
            ],
            "POST":
            [
                "/api/users/",
                "/api/ideas/"
            ],
            "DELETE":
            [
                "/api/users/{user_id}",
                "/api/ideas/{idea_id}"
            ]
        }
    }), 200)


@app.route('/api/users/', endpoint='list_users', methods=['GET'])
def get_users():
    """
    Sends a list of users present in the database
    """
    all_users = User.query.all()
    if all_users:
        users = []
        # Todo: Add paging to retrieve next 50 users and so on
        for u in all_users[0:50]:
            users.append(u.json)

        retData, retStatus = {"users": users}, 200
    else:
        retData = {"error": "There are no users in the database."}

    return make_response(jsonify(retData), retStatus)


@app.route('/api/users/<uuid:uid>', endpoint='list_user', methods=['GET'])
def get_user(uid):
    """
    Get a specific user with the matching user_id
    """

    u = User.query.filter_by(user_id=uid).first()
    if u:
        retData, retStatus = {"user": u.json}, 200
    else:
        retData = {"error": "The specified user does not exist."}

    return make_response(jsonify(retData), retStatus)


@app.route('/api/users/', endpoint='create_user', methods=['POST'])
def create_user():
    """
    Creates a new user with the json data sent
    """

    if request.json:
        retData, retStatus = request.json, 201
    else:
        retData, retStatus = {
            "error": "The input data sent should be json."}, 400

    # TODO: Check for the validity of the input (username, email, existence of
    # user, etc)

    User.new(retData['username'], retData['email'])

    return make_response(jsonify(retData), retStatus)


@app.route('/api/users/<uuid:uid>', endpoint='delete_user', methods=['DELETE'])
def delete_user(uid):
    """
    Delete the user with matching user_id
    """

    u = User.query.filter_by(user_id=uid).first()
    if u:
        retData, retStatus = {"user": u.json}, 200
    else:
        retData, retStatus = {
            "error": "The specified user does not exist."}, 404

    User.delete(u)

    return make_response(jsonify(retData), retStatus)

# TODO: Update user data


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
