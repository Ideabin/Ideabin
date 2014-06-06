# This is a hackety hacky way of loading all the modules present in the
# current directory, so you don't have to manually add them here.

# All you now gotta do is create a test, place it in the current folder
# and it'll all be imported here. Slick eh?
# Copied from: http://stackoverflow.com/a/16853487/2043048

__all__ = []

import pkgutil
import inspect

for loader, name, is_pkg in pkgutil.walk_packages(__path__):
    module = loader.find_module(name).load_module(name)

    for name, value in inspect.getmembers(module):
        if name.startswith('__'):
            continue

        globals()[name] = value
        __all__.append(name)
