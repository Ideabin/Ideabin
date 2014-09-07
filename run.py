from server import app

from server.errors import init_error_handlers
init_error_handlers(app)

# Import all views
from server.users.views import *
from server.ideas.views import *

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=9999, debug=True)
