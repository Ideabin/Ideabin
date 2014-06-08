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
        self.assertEqual(users[1].email, "guest@gmail.com")

    def test_update_user(self):
        """
        Try updating the details of a user
        """

        admin = User.query.filter_by(username='admin').first()
        admin.update(email="admin@gmail.com")
