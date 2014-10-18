from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

from .flask_uuid import UUID_RE

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy()


def create_tables(app):
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    db.metadata.create_all(engine)
    return engine


def validate_uuid(string):
    """Validates UUID. Returns True if valid, False otherwise."""
    return True if UUID_RE.match(string) else False
