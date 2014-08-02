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
        self.assertEqual(len(users), 2)

    def test_update_user(self):
        """
        Try updating the details of a user
        """

        admin = User.query.filter_by(username='admin').first()
        admin.update(username="root", email="admin@outlook.com")

        self.assertEqual(admin.username, "root")
        self.assertEqual(admin.email, "admin@outlook.com")

        admin.update(username="admin", email="admin@gmail.com")
