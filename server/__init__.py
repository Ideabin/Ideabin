# Flask and associates
from flask import Flask, Blueprint

# SQLAlchemy
from sqlalchemy import create_engine
from flask.ext.sqlalchemy import SQLAlchemy

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

# Create all tables
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
db.metadata.create_all(engine)

# A uuid url converter for flask
from misc.flask_uuid import FlaskUUID
FlaskUUID(app)


def create_bp(app):
    """ Create all blueprints with correct  """

    from server.views import root_bp, api_bp
    from server.users.views import users_bp
    from server.ideas.views import ideas_bp

    app.register_blueprint(root_bp, url_prefix='/')
    app.register_blueprint(api_bp, url_prefix='/api/1')
    app.register_blueprint(users_bp, url_prefix='/api/1/users')
    app.register_blueprint(ideas_bp, url_prefix='/api/1/ideas')
