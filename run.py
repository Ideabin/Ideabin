# Run a test server.
from server import app

# Import all views
from server.users.views import *
from server.ideas.views import *

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=9999, debug=True)
