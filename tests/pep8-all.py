"""
Run PEP8 on all Python files in this directory and subdirectories as part of
the tests.

Original: https://gist.github.com/swenson/8142788
"""

__author__ = 'Christopher Swenson'
__email__ = 'chris@caswenson.com'
__license__ = 'CC0 http://creativecommons.org/publicdomain/zero/1.0/'

import os
import os.path
import unittest

import pep8

# ignore stuff in virtualenvs or version control directories
ignore_patterns = ('.git', 'env', '__pycache__', '_Help', 'alembic')


def ignore(dir):
    """Should the directory be ignored?"""
    for pattern in ignore_patterns:
        if pattern in dir:
            return True
    return False


class TestPep8(unittest.TestCase):
    """Run PEP8 on all files in this directory and subdirectories."""

    def test_pep8(self):
        style = pep8.StyleGuide()

        errors = 0
        for root, _, files in os.walk('.'):
            if ignore(root):
                continue

            python_files = [
                os.path.join(root, f) for f in files if f.endswith('.py')
            ]
            errors += style.check_files(python_files).total_errors

        self.assertEqual(errors, 0, 'PEP8 style errors: %d' % errors)
