# Statement for enabling the development environment
DEBUG = True

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# The database that we'll be using for all testing purposes
# Todo: What about production?
SQLALCHEMY_DATABASE_URI = "mysql+oursql://user123:pass123@localhost/ideabin"
DATABASE_CONNECT_OPTIONS = {}
