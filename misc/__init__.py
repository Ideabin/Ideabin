from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy()

def create_tables(app):
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    db.metadata.create_all(engine)
    return engine
