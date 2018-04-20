from rdflib import Graph
from rdflib import URIRef
from rdflib.namespace import RDF

g = Graph()
g.parse("engenhariaFlorestalRDF.owl")

# Iterate over triples in store and print them out.

localizado = URIRef('http://www.semanticweb.org/tulio/ontologies/2018/3/engenhariaFlorestal#localizado_em')
brasilia = URIRef('http://www.semanticweb.org/tulio/ontologies/2018/3/engenhariaFlorestal#Brasília')

triples = g.triples(brasilia, localizado, o)
print(triples)
