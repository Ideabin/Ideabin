# The flask app
from server import app

# Errors and Exceptions
from server.errors import init_error_handlers
init_error_handlers(app)

# Create all blueprints
from server import create_bp
create_bp(app)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=9999, debug=True)
