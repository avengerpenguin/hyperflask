from flask import Flask
from hyperflask import Hyperflask
from hyperflask.sqlalchemy import query_to_graph
from rdflib import Graph
import pytest
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import httpretty
import re


@pytest.fixture(autouse=True)
def mock_requests_to_use_flask_test_client(request, app):

    client = app.test_client()

    def get_callback(http_request, uri, headers):
        print(dict(http_request.headers))
        r = client.get(uri, headers=dict(http_request.headers))

        response_headers = {
            'content-type': r.headers['Content-Type'],
            'content-length': len(r.headers['Content-Length']),
        }
        response_headers.update(headers)

        print(dict(r.headers))
        return int(r.status_code), response_headers, r.data

    httpretty.register_uri(httpretty.GET, re.compile('.*'), body=get_callback)
    httpretty.enable()

    request.addfinalizer(httpretty.disable)
    request.addfinalizer(httpretty.reset)


@pytest.fixture
def app():
    app = Flask('test')
    hf = Hyperflask(app)

    @hf.resource('/')
    def index():
        return Graph()

    return app


@pytest.fixture
def client(app):
    return app.test_client()


def test_200_response_from_home(client):
    r = client.get('/')
    assert r.status_code == 200


mimes = [
    ('text/turtle',) * 2,
    ('application/rdf+xml',) * 2,
    ('text/html, text/turtle', 'text/turtle'),
]


@pytest.mark.parametrize("accept,content_type", mimes)
def test_content_negotiation(accept, content_type, client):
    r = client.get('/', headers={'Accept': accept})
    print(r.data)
    assert 'Content-Type' in r.headers
    assert r.headers['Content-Type'].split(';')[0] == content_type
    
