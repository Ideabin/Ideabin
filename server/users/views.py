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

# The model
from .models import User

users_bp = Blueprint('ws_users', __name__)


@users_bp.route('/', endpoint='list_users', methods=['GET'])
def get_users():
    """
    Sends a list of users present in the database
    """
    all_users = User.query.all()
    users = []
    if all_users:
        # Todo: Add paging to retrieve next 50 users and so on
        for u in all_users[0:50]:
            users.append(u.json)
    else:
        raise NotFound

    # jsonify is not used, because it can't send json lists
    resp = make_response(json.dumps(users), 200)
    resp.mimetype = 'application/json'
    return resp


@users_bp.route('/<uuid:uid>', endpoint='list_user', methods=['GET'])
def get_user(uid):
    """
    Get a specific user with the matching user_id
    """

    u = User.query.filter_by(user_id=uid).first()
    if not u:
        raise NotFound

    return make_response(jsonify(u.json), 200)


@users_bp.route('/', endpoint='create_user', methods=['POST'])
def create_user():
    """
    Creates a new user with the json data sent
    """

    if not request.json:
        raise InvalidRequest

    # Todo: Check for the validity of the input
    # (username, email, existence of user, etc)

    u = User.new(request.json['username'], request.json['email'])

    return make_response(jsonify(u.json), 200)


@users_bp.route('/<uuid:uid>', endpoint='delete_user', methods=['DELETE'])
def delete_user(uid):
    """
    Delete the user with matching user_id
    """

    u = User.query.filter_by(user_id=uid).first()
    if not u:
        raise NotFound

    u = User.delete(u)

    return make_response(jsonify(u.json), 200)

# Todo: Update user data
