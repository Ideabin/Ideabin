import unittest

from server.users.models import User

class UsersTestCase(unittest.TestCase):
    """Run tests on our 'Users' model"""

    def test_add_some_users(self):
        """
        Add some users to the db and confirm that they have been added
        """
        User.new('admin', 'admin@gmail.com')
        User.new('guest', 'guest@gmail.com')

        users = User.query.all()
        self.assertEqual(users[0].email, "admin@gmail.com")

        admin = User.query.filter_by(username='admin').first()
        self.assertEqual(admin.username, "admin")

    def test_query_users(self):
        """
        Print all user ids present in the db

        Not a test, but is just used while development
        Will probably be removed in later commits
        """

        users = User.query.all()
        for user in users:
            print(user.username, user.id)
