from rdflib import Graph
from rdflib import URIRef
from rdflib.namespace import RDF


g = Graph()
g.parse("engenhariaFlorestalRDF.owl")

# Iterate over triples in store and print them out.

localizado = URIRef('http://www.semanticweb.org/tulio/ontologies/2018/3/engenhariaFlorestal#localizado_em')
brasilia = URIRef('http://www.semanticweb.org/tulio/ontologies/2018/3/engenhariaFlorestal#Brasília')
abrange = URIRef('http://www.semanticweb.org/tulio/ontologies/2018/3/engenhariaFlorestal#abrange')
adapta = URIRef('http://www.semanticweb.org/tulio/ontologies/2018/3/engenhariaFlorestal#se_adapta_a')

# Itera sobre o grafo para encontrar o estado o qual se encontra a cidade selecionada pelo usuário.
for (s,p,o) in g.triples((brasilia, localizado, None)):
	local = o

# Itera sobre o grafo para encontrar o bioma predominante do estado.
for (s,p,o) in g.triples((None, abrange, local)):
	bioma = s

# Itera sobre o grafo para encontrar e imprimir plantas que se adaptam facilmente ao bioma predominante.
for (s,p,o) in g.triples((None, adapta, bioma)):
	print(s)