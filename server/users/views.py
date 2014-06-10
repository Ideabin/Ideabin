# Our application and database
from server import app, db

# Some flask goodies
from flask import make_response, jsonify, request

# The model
from .models import User

# A uuid url converter for flask
from misc.flask_uuid import FlaskUUID
FlaskUUID(app)

# Create all tables
db.create_all()


# Note: This route will probably be taken over by
# our client - the ideabin website.
@app.route('/')
def index():
    return make_response(jsonify({
            "message": "If you're looking for the IdeaBin api, start at the /api endpoint."
        }), 200)


@app.route('/api/')
def api_begins():
    return make_response(jsonify({
            "message": "The api is currently being worked on.",
            "methods":
            {
                "GET":
                [
                    "/api/users/",
                    "/api/users/{user_id}"
                ]
            }
        }), 200)


@app.route('/api/users/', methods = ['GET', 'POST'])
@app.route('/api/users/<uuid:uid>', methods = ['GET'])
def get_users(uid=None):
        """
        Sends a list of users present in the database
        """
        if request.method == 'GET':
            retData = {"error": "An error occurred while processing the request."}
            retStatus = 404
            if uid:
                u = User.query.filter_by(user_id=uid).first()
                if u:
                    retData = {"user": u.json}
                    retStatus = 200
                else:
                    retData = {"error": "The specified user does not exist."}
            else:
                all_users = User.query.all()
                if all_users:
                    users = []
                    # Todo: Add paging to retrieve next 50 users and so on
                    for u in all_users[0:50]:
                        users.append(u.json)

                    retData = {"users": users}
                    retStatus = 200
                else:
                    retData = {"error": "There are no users in the database."}

            return make_response(jsonify(retData), retStatus)
        else:
            return make_response(jsonify({
                    "error": "The post request has not yet been created.",
                    }), 404)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({
            "error": "Whatever it is that you're looking for - it ain't here son!"
        }), 404)
