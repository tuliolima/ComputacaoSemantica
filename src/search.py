from rdflib import Graph
from rdflib import URIRef
from rdflib.namespace import RDF
from rdflib import Namespace
import utils

ontology = Namespace('http://www.semanticweb.org/tulio/ontologies/2018/3/engenhariaFlorestal#')
ontologyPrefix = 'http://www.semanticweb.org/tulio/ontologies/2018/3/engenhariaFlorestal#'

transitiveProperty = URIRef('http://www.w3.org/2002/07/owl#TransitiveProperty')
funtionalProperty = URIRef('http://www.w3.org/2002/07/owl#FunctionalProperty')



def validateTriple(g, subject = None, predicate = None, object = None):
    """
    Verifica se a tripla é válida no grafo.
    Leva em conta a transitividade, reflexividade e simetria das relações.
    """

    subjectURI = URIRef(ontologyPrefix + subject)
    predicateURI = URIRef(ontologyPrefix + predicate)
    objectURI = URIRef(ontologyPrefix + object)

    # Primeiro temos que conhecer a relação e suas propriedades
    # A relação existe?
    queryResult = g.query(
        """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        SELECT DISTINCT ?relation
            WHERE {
                ?relation rdf:type owl:ObjectProperty .
            }
        """)
    existingRelation = False
    
    for row in queryResult:
        result = row[0]
        if (result == predicateURI):
            # A relação existe
            print('Debug: A relação existe')
            existingRelation = True
    
    if (existingRelation):

        # Temos que conhecer as suas propriedades
        queryResult = g.query(
            """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX ontology: <http://www.semanticweb.org/tulio/ontologies/2018/3/engenhariaFlorestal#>
            SELECT DISTINCT ?property
                WHERE {
                    ontology:""" + predicate + """ rdf:type ?property .
                }
            """)

        isTransitive = False
        for row in queryResult:
            result = row[0]
            if (result == transitiveProperty):
                # A propriedade é transitiva, devemos resolver a transitividade
                print("Debug: A relação é transitiva")
                isTransitive = True

        # Construir a lista de objetos do sujeito especificado
        if (isTransitive):
            objects = g.transitive_objects(subjectURI, predicateURI)

        else:
            objects = g.objects(subjectURI, predicateURI)

        if objectURI in objects:
            return True
        else:
            # A tripla não existe
            return False
    else:
        # A relação não existe
        return False


# Main

g = Graph()
g.parse("../ontologias/engenhariaFlorestalRDF.owl")
# utils.printIndividuals(g)
# utils.printClasses(g)
# utils.printProperties(g)

entrada = input("Digite a tripla: ")
print()

# retirando os parêntesis
tripla = entrada[1:-1]
# dividindo os termos
s, p, o = tripla.split(', ')
# print(s, p, o)

if (validateTriple(g, s, p, o)):
    print('Existe!')
else:
    print('Não existe!')

