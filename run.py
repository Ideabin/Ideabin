# Run a test server.
from app import app
# app.run(host='127.0.0.1', port=9876, debug=True)

# All this code is here temporarily as I am still
# trying to think of the optimum project structure
# It'll probably be moved to a separate file. Until then...

from app import db
from app.models.User import User

from sqlalchemy import exc as SQLexc

def add_user(username, email):
    new_user = User(username, email)
    try:
        db.session.add(new_user)
        db.session.commit()
    except SQLexc.IntegrityError as e:
        db.session.rollback()
        if str(e).index('is not unique'):
            print ("Not adding '%s' as it already exists." % e.params[0])

# Create all tables
db.create_all()

# Add some users
add_user('admin', 'admin@example.com')
add_user('guest', 'guest@example.com')

users = User.query.all()
print(users[0].email)

admin = User.query.filter_by(username='admin').first()
print(admin)
