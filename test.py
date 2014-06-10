# This file will import tests placed and
import unittest
import os

# Import all our tests
from tests import *

# Removes the db before running tests
# BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# os.remove(os.path.join(BASE_DIR, 'IdeaBin.db'))

# The db object
from server import db

# Create all tables
db.create_all()

if __name__ == '__main__':
    unittest.main()
