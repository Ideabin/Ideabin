from flask import make_response, jsonify, Blueprint

api_bp = Blueprint('ws_api', __name__)
root_bp = Blueprint('ws_root', __name__)


@root_bp.route('/')
def index():
    return make_response(jsonify({
        "message": "If you're looking for the IdeaBin api, "
                   "start at the /api/1/ endpoint."
    }), 200)


@api_bp.route('/')
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
