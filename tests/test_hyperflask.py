import pytest
from flask import Flask
from rdflib import Graph
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from hyperflask import Hyperflask
from hyperflask.sqlalchemy import query_to_graph


@pytest.fixture
def people_data():
    """
    Mocks out a simple data structure in lieu of a real ORM/data layer
    as you might use in a real Flask application.

    Numeric keys emulate database primary keys the the data "rows" are
    simple dict objects.
    """
    return {
        1: {"name": "Fiona", "Email": "fiona@example.com"},
        2: {"name": "Henry", "Email": "harri.tewder@example.com"},
    }


@pytest.fixture
def database():
    engine = create_engine("sqlite://", convert_unicode=True)
    db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    Base = declarative_base()
    Base.query = db_session.query_property()

    class Person(Base):
        """Example ORM model for a table of person data. The class name
        and field names deliberately following the schema.org
        namespace so we can use a single namespace in the mapping
        from model to RDF graph later."""

        __tablename__ = "people"

        id = Column(Integer, primary_key=True)
        name = Column(String(50), unique=True)
        email = Column(String(120), unique=True)

    Base.metadata.create_all(bind=engine)

    db_session.add(Person(name="Fiona", email="fiona@example.com"))
    db_session.add(Person(name="Henry", email="harri.tewder@example.com"))

    db_session.commit()

    class Models:
        """Fakes a models.py module"""

        def __init__(self):
            self.Person = Person
            self.engine = engine

    return Models()


@pytest.fixture
def app(database):
    app = Flask("test")
    hf = Hyperflask(app)

    @hf.resource("/")
    def index():
        return Graph()

    @hf.resource("/people")
    def people():
        session = sessionmaker(bind=database.engine)()
        people = session.query(database.Person).all()
        return query_to_graph(people, namespace="http://schema.org/", ignore=["id"])

    return app


@pytest.fixture
def client(app):
    return app.test_client()


def test_200_response_from_home(client):
    r = client.get("/")
    assert r.status_code == 200


mimes = [
    ("text/turtle",) * 2,
    ("application/rdf+xml",) * 2,
    ("text/html, text/turtle", "text/turtle"),
]


@pytest.mark.parametrize("accept,content_type", mimes)
def test_content_negotiation(accept, content_type, client):
    r = client.get("/", headers={"Accept": accept})
    print(r.data)
    assert "Content-Type" in r.headers
    assert r.headers["Content-Type"].split(";")[0] == content_type


def test_collection(client):
    r = client.get("/people", headers={"Accept": "text/turtle"})
    g = Graph()
    g.parse(data=r.data, format="turtle")

    assert len(g) == 6

    results = {
        (row.name.toPython(), row.email.toPython())
        for row in g.query(
            """SELECT DISTINCT ?name ?email
        WHERE {
          ?id <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/Person> .
          ?id <http://schema.org/name> ?name .
          ?id <http://schema.org/email> ?email .
        }
        """
        )
    }
    assert results == {
        ("Fiona", "fiona@example.com"),
        ("Henry", "harri.tewder@example.com"),
    }
