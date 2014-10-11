from flask import make_response, jsonify, Blueprint

api_bp = Blueprint('api', __name__)

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
