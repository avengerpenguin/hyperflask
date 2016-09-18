from rdflib import Graph, BNode, URIRef, RDF
from laconia import ThingFactory
from sqlalchemy import inspect


def query_to_graph(query, namespace='http://example.com/', ignore=()):

    g = Graph()
    Thing = ThingFactory(g)

    for entity in query:
        thing = Thing()

        thing_type = namespace + type(entity).__name__
        class_id = Thing(thing_type)
        getattr(thing, RDF.type).add(class_id)

        mapper = inspect(type(entity))
        for attr in mapper.attrs:
            if attr.key not in ignore:
                prop = URIRef(namespace + attr.key)
                getattr(thing, prop).add(getattr(entity, attr.key))

    return g
