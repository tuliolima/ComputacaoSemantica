from rdflib import Graph
from rdflib import URIRef
from rdflib.namespace import RDF
from rdflib import Namespace

# Inicializa um TAD grafo e atribui a ontologia nele.
g = Graph()
g.parse("engenhariaFlorestalRDF.owl")

# Maneira elegante de acessar a URI sem precisar repeti-la.
ontology = Namespace('http://www.semanticweb.org/tulio/ontologies/2018/3/engenhariaFlorestal#')

# Cabeçalho
print('\nMotor de inferência para a ontologia de Engenharia Florestal')

while 1:
    # Captura e trata a entrada do usuário.
    print('\nDigite a cidade desejada:')
    cidade = URIRef('http://www.semanticweb.org/tulio/ontologies/2018/3/engenhariaFlorestal#' + input())

    print('\nBuscando...')

    # Verifica se existe a cidade na ontologia e identifica o estado
    existe = False
    for (s, p, o) in g.triples((cidade, RDF.type, ontology.Cidade)):
        existe = True

    # Se a cidade existe continua a pesquisa
    if(existe):
        break
    else:
        print('\n! A cidade não existe !')

# Identifica o estado e o país
for (s,p,o) in g.triples((cidade, ontology.localizado_em, None)):
    estado = o
for (s,p,o) in g.triples((estado, ontology.localizado_em, None)):
    pais = o

# Imprime as informações encontradas
print('\nDados encontrados:')
print('   ' + cidade.split('#')[-1] + ', ' + estado.split('#')[-1] + ', ' + pais.split('#')[-1])

# TODO Informações climáticas da cidade.

# Itera sobre o grafo para encontrar o bioma predominante do estado.
for (s,p,o) in g.triples((None, ontology.abrange, cidade)):
	bioma = s

print('\nBioma pertencente:')
print('   ' + bioma.split('#')[-1])

print('\nPlantas apropriadas:')
# Itera sobre o grafo para encontrar e imprimir plantas que se adaptam facilmente ao bioma predominante.
for (s,p,o) in g.triples((None, ontology.se_adapta_a, bioma)):
	print('   ' + s.split('#')[-1]) # Imprime só o nome da intância. # https://stackoverflow.com/questions/20785724/rdflib-remove-namespace-from-a-uriref-resource #
print()

# TODO Informações das plantas, talvez um menu para escolher a planta e ver mais informações.