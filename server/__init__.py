# Flask and associates
from flask import Flask

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
