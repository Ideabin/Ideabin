from frontend import create_app as frontend_create_app
from server import create_app as ws_create_app

from werkzeug.serving import run_simple
from werkzeug.wsgi import DispatcherMiddleware


# Note: This function will be removed during deployment.
def extra_files():
    """
    Watch files and reload the server when they change.
    """

    import os

    extra_dirs = [
        'frontend/static',
        'frontend/templates'
    ]

    extra_files = extra_dirs[:]
    for extra_dir in extra_dirs:
        for dirname, dirs, files in os.walk(extra_dir):
            for filename in files:
                filename = os.path.join(dirname, filename)
                if os.path.isfile(filename):
                    extra_files.append(filename)

    return extra_files

application = DispatcherMiddleware(frontend_create_app(), {
    '/api/1': ws_create_app()
})

if __name__ == '__main__':
    run_simple(
        hostname='127.0.0.1',
        port=9999,
        application=application,
        use_reloader=True,
        use_debugger=True,
        use_evalex=True,
        extra_files=extra_files()
    )
