from functools import wraps
from rdflib import Graph


class Hyperflask(object):
    def __init__(self, flask_app):
        self.app = flask_app

    def resource(self, path):
        def decorator(handler):
            @self.app.route(path)
            @wraps(handler)
            def wrapper(*args, **kwargs):
                return handler(*args, **kwargs)
            return wrapper
        return decorator

def graph():
    return Graph()
