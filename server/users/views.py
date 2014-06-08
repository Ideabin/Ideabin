# Our application
from server import app

# Some flask goodies
from flask import make_response, jsonify

# The model
from server.users.models import User

# A uuid url converter for flask
from misc.flask_uuid import FlaskUUID
FlaskUUID(app)

# Note: This route will probably be taken over by
# our client - the ideabin website.
@app.route('/')
def index():
    return make_response(jsonify({
            "message": "If you're looking for the IdeaBin api, start at the /api endpoint."
        }), 200)


@app.route('/api')
def api_begins():
    return make_response(jsonify({
            "message": "The api is currently being worked on.",
            "methods":
            {
                "GET": "/api/users",
                "GET": "/api/user/{uuid: user_id}"
            }
        }), 200)


@app.route('/api/users', methods = ['GET'])
def get_users():
        users = []
        for u in User.query.all():
            users.append(u.json())

        return make_response(jsonify({
            "users": users
            }), 200)


@app.route('/api/user/<uuid:uid>', methods = ['GET'])
def get_user(uid):
        u = User.query.filter_by(id=uid).first()

        return make_response(jsonify({
            "user": u.json()
            }), 200)



@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({
            "error": "Whatever it is that you're looking for - it ain't here son!"
        }), 404)
