import os

 # we expect an environ named 'DEBUG' with in production,
 # with any value for which, bool(os.environ.get('DEBUG')) = True
in_production = os.environ.get('DEBUG')

if in_production:
    from .main import *
else:  # no environment variable named 'DEBUG', we're not in production
    from .dev import *