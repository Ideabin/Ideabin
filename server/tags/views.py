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
from server.ideas.models import Idea

tags_bp = Blueprint('ws_tags', __name__)


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


@tags_bp.route('/<uuid:uid>', endpoint='list_tag_ideas', methods=['GET'])
def get_tag_ideas(uid):
    """
    Get all ideas with the matching tag_id
    """

    sparks = Tag.query.filter_by(tag_id=uid).all()
    if not sparks:
        NotFound

    return make_response(jsonify(sparks.json), 200)


@tags_bp.route('/', endpoint='create_tag', methods=['POST'])
def create_tag():
    """
    Creates a new tag with the json data sent
    """
    if not request.json:
        raise InvalidRequest

    idea = Idea.query.filter_by(idea_id=retData['idea_id']).first()
    if not idea:
        raise InvalidRequest(
            "The idea you are creating new tag for, does not exist.")

    t = Tag.new(
        request.json['title'],
        request.json['idea_id']
    )

    return make_response(jsonify(t.json), 200)


# @tags_bp.route('/<uuid:uid>', endpoint='delete_tag', methods=['DELETE'])
# def delete_tag(uid):
#     """
#     Delete the tag with matching tag_id.
#     """
#     if request.json:
#         retData, retStatus = request.json, 201

# gets the tag and deletes it.
#         tag = Tag.query.filter_by(tag_id=uid).first()
#         if tag:
#             retData, retStatus = {"tag": tag.json}, 200
#             Tag.delete(tag)
#         else:
#             retData, retStatus = {
#                 "error": "The specified tag does not exist."}, 400
#     else:
#         retData, retStatus = {
#             "error": "The input data sent should be json."}, 400

#     return make_response(jsonify(retData), retStatus)

# TODO: (i)Update tag data
