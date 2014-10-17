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
from .models import Tag

tags_bp = Blueprint('tags', __name__)


@tags_bp.route('/', endpoint='list_tags', methods=['GET'])
def get_tags():
    """
    Sends a list of tags present in the database
    """
    all_tags = Tag.query.all()
    tags = []
    if all_tags:
        # Todo: (i)Add paging to retrieve next 50 tags and so on
        # Todo: count of the ideas in a particular tag.
        for tg in all_tags[0:50]:
            tags.append(tg.json)
    else:
        raise NotFound

    resp = make_response(json.dumps(tags), 200)
    resp.mimetype = 'application/json'
    return resp


# @tags_bp.route('/<uuid:uid>', endpoint='list_tag_ideas', methods=['GET'])
# def get_tag_ideas(uid):
#     """
#     Get all ideas with the matching tag_id
#     """

#     s = Tagging.query.filter_by(tag_id=uid).all()
#     print(str(t))
#     if not s:
#         NotFound

#     sparks = []
#     for spark in s:
#         sparks.append(Idea.query.filter_by(idea_id=spark).first().json)

#     resp = make_response(json.dumps(sparks), 200)
#     resp.mimetype = 'application/json'
#     return resp


@tags_bp.route('/', endpoint='create_tag', methods=['POST'])
def create_tag():
    """
    Creates a new tag with the json data sent
    """
    if not request.json:
        raise InvalidRequest

    t = Tag.new(
        request.json['tagname'],
        request.json['desc']
    )

    return make_response(jsonify(t.json), 200)


@tags_bp.route('/<uuid:tid>', endpoint='delete_tag', methods=['DELETE'])
def delete_tag(uid):
    """
    Delete the tag with matching tag_id.
    """

    tag = Tag.query.filter_by(tag_id=tid).first()
    if not tag:
        raise NotFound

    tag = Tag.delete(tag)

    return make_response(jsonify(tag.json), 200)

    # todo: edit the tag data (rename to the previous tags must be taken care
    # of)
