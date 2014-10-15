# Our application and database
from misc import db
from server.exceptions import (
    NotFound,
    ServerError,
    InvalidRequest,
)

from flask_login import (
    current_user,
    login_required
)

import json
import re

# Some flask goodies
from flask import make_response, jsonify, request, Blueprint
from flask.ext.restful import reqparse

# The model
from .models import User

users_bp = Blueprint('users', __name__)
parser = reqparse.RequestParser()


def email(email_str):
    """ return True if email_str is a valid email """
    if re.match("[^@]+@[^@]+\.[^@]+", email_str):
        return True
    else:
        raise ValidationError("{} is not a valid email")


def string(string_str):
    """ returns true if string_str is a valid username string """
    if not (len(string_str) < 1 or string_str.isdigit()):
        return True
    else:
        raise ValidationError("{} is not a valid username string")


@users_bp.route('/me/', endpoint='me', methods=['GET'])
@login_required
def get_me():
    """
    Return data of whoever is logged in.
    """
    return make_response(jsonify(current_user.json), 200)


@users_bp.route('/', endpoint='list', methods=['GET'])
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


@users_bp.route('/<uuid:uid>', endpoint='id', methods=['GET'])
def get_user(uid):
    """
    Get a specific user with the matching user_id
    """

    u = User.query.filter_by(user_id=uid).first()
    if not u:
        raise NotFound

    return make_response(jsonify(u.json), 200)


@users_bp.route('/', endpoint='create', methods=['POST'])
def create_user():
    """
    Creates a new user with the json data sent
    """

    if not request.json:
        raise InvalidRequest

    parser.add_argument(
        'username',
        type=string,
        required=True,
        # location='form',
        help='username needs to be of string type and can\'t .'
    )
    parser.add_argument(
        'email',
        type=email,
        required=True,
        # location='form',
        help='Rate to charge for this resource'
    )

    args = parser.parse_args()

    u = User.new(
        request.json['username'],
        request.json['password'],
        request.json['email']
    )

    return make_response(jsonify(u.json), 200)


@users_bp.route('/<uuid:uid>', endpoint='delete', methods=['DELETE'])
def delete_user(uid):
    """
    Delete the user with matching user_id
    """

    u = User.query.filter_by(user_id=uid).first()
    if not u:
        raise NotFound

    # todo: user verification to delete the user

    u = User.delete(u)

    return make_response(jsonify(u.json), 200)

# Todo: Update user data
