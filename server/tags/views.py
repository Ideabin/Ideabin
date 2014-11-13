import json

from misc import db
from server.exceptions import *

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

from misc.parser import Parser

from .models import Tag
from server.subscriptions.models import TagSub

tags_bp = Blueprint('tags', __name__)


@tags_bp.route('/', endpoint='list', methods=['GET'])
def get_tags():
    """
    Sends a list of tags present in the database
    """
    # Todo: (1) Add paging to retrieve next 50 tags and so on
    tags = Tag.query.limit(50)
    if not tags:
        raise NotFound

    resp = make_response(json.dumps([t.json for t in tags]), 200)
    resp.mimetype = 'application/json'
    return resp


@tags_bp.route('/<uuid:tag_id>', endpoint='id', methods=['GET'])
def get_tag(tag_id):
    """
    Get a specific tag with the matching tag_id
    """

    tag = Tag.query.filter_by(tag_id=tag_id).first()
    if not tag:
        raise NotFound

    return make_response(jsonify(tag.json), 200)


@tags_bp.route('/<string:tname>', endpoint='name', methods=['GET'])
def get_tag(tname):
    """
    Get a specific tag with the matching tagname
    """

    tag = Tag.query.filter_by(tagname=tname).first()
    if not tag:
        raise NotFound

    return make_response(jsonify(tag.json), 200)


@tags_bp.route('/', endpoint='create', methods=['POST'])
def create_tag():
    """
    Creates a new tag with the json data sent
    """
    if not request.json:
        raise InvalidRequest

    name = Parser.string('name', min=2, max=50)
    desc = Parser.string('desc', optional=True)

    new = Tag.new(name, desc)
    return make_response(jsonify(new.json), 201)


@tags_bp.route('/<string:tname>', endpoint='delete', methods=['DELETE'])
@login_required
def delete_tag(tname):
    """
    Delete the tag with matching tag_id.
    """

    if not current_user.is_admin():
        raise Unauthorized

    tag = Tag.query.filter_by(tagname=tname).first()
    if not tag:
        raise NotFound

    Tag.delete(tag)
    return make_response('', 204)


@tags_bp.route('/<uuid:tag_id>/subscribe/', endpoint='subscribe',
               methods=['POST'])
@login_required
def toggle_subscription(tag_id):
    """
    Subscribes a tag
    """

    user_id = current_user.user_id
    sub = TagSub.query.filter_by(sub_by=user_id, sub_to=tag_id).first()
    if not sub:
        TagSub.new(user_id, tag_id)
        msg = "You are now subscribed."
    else:
        TagSub.delete(sub)
        msg = "You are now unsubscribed."

    return make_response(jsonify({"message": msg}), 200)

# Rename to the previous tags must be taken care of
@tags_bp.route('/<uuid:tag_id>', endpoint='edit', methods=['PUT'])
@login_required
def edit_idea(tag_id):
    """
    Update the fields of an idea.
    """
    if not request.json:
        raise InvalidRequest

    tag = Tag.query.filter_by(tag_id=tag_id).first()
    if not tag:
        raise NotFound

    if not user.isadmin():
        raise Unauthorized('Only administrators can edit a tag.')

    name = Parser.string('name', min=2, max=50)
    desc = Parser.string('desc', optional=True)

    if Tag.query.filter_by(tagname=name).first():
        raise Conflict('Tagname `%s` already exists.' % tagname)

    tag = Tag.update(tag, tagname, desc)

    return make_response(jsonify(tag.json), 201)
