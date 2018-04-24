from rdflib import Graph
from rdflib import URIRef
from rdflib.namespace import RDF
from rdflib import Namespace

# Inicializa um TAD grafo e atribui a ontologia nele.
g = Graph()
g.parse("engenhariaFlorestalRDF.owl")

# Maneira elegante de acessar a URI sem precisar repeti-la.
ontology = Namespace('http://www.semanticweb.org/tulio/ontologies/2018/3/engenhariaFlorestal#')

# Captura e trata a entrada do usuário.
cidade = URIRef('http://www.semanticweb.org/tulio/ontologies/2018/3/engenhariaFlorestal#' + input("Cidade: "))

# Itera sobre o grafo para encontrar o estado o qual se encontra a cidade selecionada pelo usuário.
for (s,p,o) in g.triples((cidade, ontology.localizado_em, None)):
	local = o

# Itera sobre o grafo para encontrar o bioma predominante do estado.
for (s,p,o) in g.triples((None, ontology.abrange, local)):
	bioma = s

# Itera sobre o grafo para encontrar e imprimir plantas que se adaptam facilmente ao bioma predominante.
for (s,p,o) in g.triples((None, ontology.se_adapta_a, bioma)):
	print(s.split('#')[-1]) # Imprime só o nome da intância. # https://stackoverflow.com/questions/20785724/rdflib-remove-namespace-from-a-uriref-resource #