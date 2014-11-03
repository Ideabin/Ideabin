import json

from misc import db
from server.exceptions import *

from flask import (
    make_response,
    jsonify,
    request,
    Blueprint
)

from misc.parser import Parser

from .models import Tag

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


@tags_bp.route('/<uuid:tid>', endpoint='id', methods=['GET'])
def get_tag(tid):
    """
    Get a specific tag with the matching tag_id
    """

    tag = Tag.query.filter_by(tag_id=tid).first()
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


# Todo: Only moderators are allowed to delete a tag.
@tags_bp.route('/<string:tname>', endpoint='delete', methods=['DELETE'])
# @login_required()
def delete_tag(tname):
    """
    Delete the tag with matching tag_id.
    """

    tag = Tag.query.filter_by(tagname=tname).first()
    if not tag:
        raise NotFound

    Tag.delete(tag)
    return make_response('', 204)


# Todo:
# 1. Edit the tag data
# (rename to the previous tags must be taken care of)
@tags_bp.route('/<uuid:tag_id>', endpoint='edit', methods=['PUT'])
@login_required
def edit_idea(tag_id):
    """
    Update the fields of an idea.
    """
    if not request.json:
        raise InvalidRequest

    if not user.isadmin():
        raise Conflict('You are not an admin.')

    tag = Tag.query.filter_by(tag_id=tag_id).first()
    if not tag:
        raise NotFound

    # Todo: These should probably be a string with some max len
    tagname = Parser.anything('tagname')
    desc = Parser.anything('desc')

    if Tag.query.filter_by(tagname=tagname).first():
        raise Conflict('This tagname already exists. Try something else.')

    tag = Tag.update(tag, tagname, desc)

    return make_response(jsonify(tag.json), 201)
