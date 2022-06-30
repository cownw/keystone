import collections
import os

try:
    # werkzeug 0.15.x
    from werkzeug.middleware import proxy_fix
except ImportError:
    # werkzeug 0.14.x
    from werkzeug.contrib import fixers as proxy_fix

