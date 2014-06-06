# Statement for enabling the development environment
DEBUG = True

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# The database that we'll be using for all testing purposes
# Todo: What about production?
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'IdeaBin.db')
DATABASE_CONNECT_OPTIONS = {}
