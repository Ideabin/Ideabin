import unittest

from server.users.models import User

class UsersTestCase(unittest.TestCase):
    """Run tests on our 'Users' model"""

    def test_add_some_users(self):
        """
        Add some users to the db.
        Confirm that they have been added
        """
        User.new('admin', 'admin@gmail.com')
        User.new('guest', 'guest@gmail.com')

        users = User.query.all()
        self.assertEqual(users[0].email, "admin@gmail.com")

        admin = User.query.filter_by(username='admin').first()
        self.assertEqual(admin.username, "admin")
