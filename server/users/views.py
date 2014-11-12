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

from sqlalchemy.sql import text
from sqlalchemy import or_

from misc import db
from misc.parser import Parser

from server.exceptions import *

from .models import User
from server.subscriptions.models import UserSub

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
    # all_users = db.engine.execute("SELECT * FROM user")
    all_users = User.query.from_statement(
        text("SELECT * FROM user LIMIT 50")).all()
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
    u = User.query.from_statement(
        text("SELECT * FROM user where user_id=:uid")).\
        params(uid=uid.hex).all()
    # u = User.query.filter_by(user_id=uid).first()
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

    # u = User.query.filter(
    #     or_(
    #         User.username == username,
    #         User.email == email)
    # ).first()
    u = User.query.from_statement(text(
        "SELECT * FROM user where username=:username OR email=:email").params(
        username=username, email=email)).all()
    if u:
        raise Conflict('The user already exists.')

    new = db.engine.execute("INSERT INTO user ()")
    new = User.new(username, password, email)
    # Note: The API shouldn't be logging in user
    login_user(new)
    return make_response(jsonify(new.json), 201)


@users_bp.route('/<uuid:uid>', endpoint='delete', methods=['DELETE'])
def delete_user(uid):
    """
    Delete the user with matching user_id
    """

    u = User.query.from_statement(
        text("SELECT * FROM user WHERE user_id==:user_id")).\
        params(user_id=uid).all()
    # u = User.query.filter_by(user_id=uid).first()
    if not u:
        raise NotFound

    # todo: user verification to delete the user

    # u = db.engine.execute("DELETE FROM user WHERE user_id==:id", id=uid)
    u = User.delete(u)

    return make_response(jsonify(u.json), 200)


@users_bp.route('/<uuid:user_id>/subscribe/', endpoint='subscribe',
                methods=['POST'])
@login_required
def toggle_subscription(user_id):
    """
    Subscribes a user
    """

    this_user_id = current_user.user_id
    if this_user_id == user_id:
        raise Conflict("You can't subscribe yourself.")

    # sub = UserSub.query.filter_by(sub_by=this_user_id,
    # sub_to=user_id).first()
    sub = UserSub.query.from_statement(text(
        "SELECT * FROM user_sub where sub_by=:by AND sub_to=:to").params(
        by=this_user_id.hex, to=user_id.hex)).all()
    if not sub:
        UserSub.new(this_user_id, user_id)
        msg = "You are now subscribed."
    else:
        UserSub.delete(sub)
        msg = "You are now unsubscribed."

    return make_response(jsonify({"message": msg}), 200)


@users_bp.route('/<uuid:user_id>', endpoint='edit', methods=['PUT'])
@login_required
def edit_idea(user_id):
    """
    Update the fields of a user.
    """
    if not request.json:
        raise InvalidRequest

    # user = User.query.filter_by(user_id=user_id).first()
    user = User.query.from_statement(
        text("SELECT * FROM user WHERE user_id==:user_id")).\
        params(user_id=uid).all()
    if not user:
        raise NotFound

    this_user_id = current_user.user_id
    if this_user_id != user_id:
        raise Unauthorized('You can only edit your own profile.')

    # Todo: (7) Decide what to do about these?
    # username = Parser.string('username', optional=True)
    # email = Parser.email('email', optional=True)
    # password = Parser.anything('password', optional=True)

    first_name = Parser.string('first_name', optional=True)
    last_name = Parser.string('last_name', optional=True)

    blog_url = Parser.uri('blog_url', optional=True)
    facebook_url = Parser.uri('facebook_url', optional=True)
    twitter_url = Parser.uri('twitter_url', optional=True)
    github_url = Parser.uri('github_url', optional=True)

    user = User.update(
        user,
        first_name=first_name,
        last_name=last_name,
        blog_url=blog_url,
        facebook_url=facebook_url,
        twitter_url=twitter_url,
        github_url=github_url
    )

    return make_response(jsonify(user.json), 201)
