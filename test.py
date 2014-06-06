# This file will import tests placed and
import unittest

# Import all our tests
from tests import *

# The db object
from server import db

# Create all tables
db.create_all()

if __name__ == '__main__':
    unittest.main()
