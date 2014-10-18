import json

from flask import (
    make_response,
    jsonify,
    request,
    Blueprint
)

from flask_login import (
    current_user,
    login_user,
    login_required
)

from sqlalchemy import or_

from misc import db
from misc.parser import Parser

from server.exceptions import *

from .models import User

users_bp = Blueprint('users', __name__)


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

    username = Parser.string('username')
    email = Parser.email('email')
    password = Parser.anything('password')

    u = User.query.filter(
        or_(
            User.username == username,
            User.email == email)
        ).first()

    if u:
        raise Conflict('The user already exists.')

    new = User.new(username, password, email)
    # Note: The API shouldn't be logging in user
    login_user(new)
    return make_response(jsonify(new.json), 201)


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
