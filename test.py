# This file will import tests placed and
import unittest
import os

# Import all our tests
from tests import *

# Create all tables
from misc import create_tables
from server import create_app as ws_app
create_tables(ws_app())

if __name__ == '__main__':
    unittest.main()
