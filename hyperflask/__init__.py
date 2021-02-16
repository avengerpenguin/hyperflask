from functools import wraps

from flask_rdf import flask_rdf
from rdflib import Graph


class Hyperflask:
    def __init__(self, flask_app):
        self.app = flask_app

    def resource(self, path):
        def decorator(handler):
            @self.app.route(path)
            @flask_rdf
            @wraps(handler)
            def wrapper(*args, **kwargs):
                return handler(*args, **kwargs)

            return wrapper

        return decorator


def graph():
    return Graph()
