# OntoFlora 1.0
# consistencia.py
# 
# Módulo para realizar a análise de consistência de uma ontologia.
# Antes de tudo deve ser chamado o método configConsistencia para
# indicar qual a ontologia que será usada.

import rdflib
from rdflib import URIRef
from rdflib import Graph

# Propriedades das relações
functionalProperty = URIRef('http://www.w3.org/2002/07/owl#FunctionalProperty')
inverseFunctionalProperty = URIRef(
    'http://www.w3.org/2002/07/owl#InverseFunctionalProperty')
transitiveProperty = URIRef('http://www.w3.org/2002/07/owl#TransitiveProperty')
symmetricProperty = URIRef('http://www.w3.org/2002/07/owl#SymmetricProperty')
asymmetricProperty = URIRef('http://www.w3.org/2002/07/owl#AsymmetricProperty')
reflexiveProperty = URIRef(
    'http://www.w3.org/2002/07/owl#ReflexiveProperty')
irreflexiveProperty = URIRef(
    'http://www.w3.org/2002/07/owl#IrreflexiveProperty')


ontologyPrefix = ''
graph = None


def configConsistencia(g, ontoPrefix):
    """Seta as variáveis globais utilizadas no módulo"""

    global ontologyPrefix, graph
    graph = g
    ontologyPrefix = ontoPrefix


def detectCycle(subject, property, remember=None):
    """Detecta Ciclo em uma relação transitiva."""

    if remember is None:
        remember = {}
    if subject in remember:
        return subject
    remember[subject] = 1
    for object in graph.objects(subject, property):
        cicle = detectCycle(object, property, remember)
        if cicle != None:
            return cicle
    return None


def consistencyEval():
    """Avalia a consistência da ontologia"""

    if graph == None:
        print('Módulo consistência: O grafo não foi definido.')
        return

    # Buscando Classes
    qres = graph.query(
        """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        SELECT DISTINCT ?class
            WHERE {
                ?class rdf:type owl:Class.
            }
        """)

    print("\nClasses:\n")
    for row in qres:
        result_1 = row[0]
        print(result_1.split('#')[-1])

    # Buscando Relações
    properties = graph.query(
        """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        SELECT DISTINCT ?property ?domain ?range
            WHERE {
                VALUES ?propertyType { owl:DatatypeProperty owl:ObjectProperty }
                ?property rdf:type ?propertyType .
                ?property rdfs:range ?range .
                ?property rdfs:domain ?domain.
            }
        """)

    print("\nRelações:\n")
    for row in properties:
        result_1 = row[0]
        result_2 = row[1]
        result_3 = row[2]
        print(result_1.split(
            '#')[-1] + " (" + result_2.split('#')[-1] + " ," + result_3.split('#')[-1] + ")")

    # Buscando Instâncias
    qres = graph.query(
        """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        SELECT DISTINCT ?individual
            WHERE {
                ?individual rdf:type owl:NamedIndividual
            }
        """)

    print("\nInstâncias:\n")
    for row in qres:
        result_1 = row[0]
        print(result_1.split('#')[-1])

    # Investigando as Relações
    for row in properties:
        property = row[0].split('#')[-1]
        propertyURI = URIRef(ontologyPrefix + property)

        # Utilize um grafo auxiliar com as triplas específicas
        # dessa relação para melhorar a performance.
        propertyGraph = Graph()
        triples = graph.triples((None, propertyURI, None))
        for (s, p, o) in triples:
            propertyGraph.add((s, p, o))

        # Temos que conhecer as suas características
        queryResult = graph.query(
            """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX ontology: <""" + ontologyPrefix + """>
            SELECT DISTINCT ?propertyType
                WHERE {
                    ontology:""" + property + """ rdf:type owl:ObjectProperty .
                    ontology:""" + property + """ rdf:type ?propertyType .
                }
            """)

        # Se a relação não tem nunhuma propriedade então não há nada
        # para analizar.
        if not queryResult:
            continue

        isFunctional = False
        isInverseFunctional = False
        isTransitive = False
        isSymmetric = False
        isAsymmetric = False
        isReflexive = False
        isIrreflexive = False
        for row in queryResult:
            result = row[0]
            if (result == inverseFunctionalProperty):
                isInverseFunctionalFunctional = True
            if (result == functionalProperty):
                isFunctional = True
            if (result == transitiveProperty):
                isTransitive = True
            if (result == symmetricProperty):
                isSymmetricsymmetric = True
            if (result == asymmetricProperty):
                isAsymmetric = True
            if (result == reflexiveProperty):
                isReflexive = True
            if (result == irreflexiveProperty):
                isIrreflexive = True

        print("\nAnalizando a relação %s:", property)

        if isFunctional:
            # Cada sujeito só pode se reacionar a um objeto.
            print("É funcional.")

            inconsistent = False
            errors = ''
            for sub in propertyGraph.subjects(predicate=propertyURI):
                i = 0
                for a in propertyGraph.objects(subject=sub, predicate=propertyURI):
                    i += 1
                    if i > 1:
                        inconsistent = True
                        errors = sub.split('#')[-1] + ', '
                        break
            if inconsistent:
                print("\tEstá inconsistente.")
                print("\tA inconsistência está em: " + errors)
            else:
                print("\tEstá consistente.")

        if isInverseFunctional:
            # Cada objeto só pode ter um sujeito relacionado a ele.
            print("É inversamente funcional.")

            inconsistent = False
            errors = ''
            for obj in propertyGraph.objects(predicate=propertyURI):
                i = 0
                for a in propertyGraph.subjects(predicate=propertyURI, object=obj):
                    i += 1
                    if i > 1:
                        inconsistent = True
                        errors = sub.split('#')[-1] + ', '
                        break
            if inconsistent:
                print("\tEstá inconsistente.")
                print("\tA inconsistência está em: " + errors)
            else:
                print("\tEstá consistente.")

        if isTransitive:
            # Não pode haver ciclos na transitividade
            print("É transitiva.")

            inconsistent = False
            for sub in propertyGraph.subjects(predicate=propertyURI):
                cycleObj = detectCycle(sub, propertyURI)
                if cycleObj != None:
                    inconsistent = True
                    break
            if inconsistent:
                print("\tEstá inconsistente.")
                print("\tA inconsistência está em: " + cycleObj.split('#')[-1])
            else:
                print("\tEstá consistente.")

        if isSymmetric:
            # A relação (x, y) pode ser interpretada como (y, x).
            print("É simétrica.")

        if isAsymmetric:
            # A relação (x, y) não pode ser interpretada como (y, x).
            print("É assimétrica.")

            queryResult = propertyGraph.query(
                """
                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX owl: <http://www.w3.org/2002/07/owl#>
                PREFIX ontology: <""" + ontologyPrefix + """>
                SELECT DISTINCT ?subject ?object 
                    WHERE {
                        ?subject ontology:""" + property + """ ?object .
                        ?object ontology:""" + property + """ ?subject .
                    }
                """)

            if not queryResult:
                print("\tEstá consistente.")
            else:
                print("\tEstá inconsistente.")
                errors = ''
                for row in qres:
                    errors += row[0].split('#')[-1] + ', '
                print("\tA inconsistência está em: " + errors)

        if isReflexive:
            # Um elemento pode se relacionar com ele mesmo.
            print("É reflexiva.")

        if isIrreflexive:
            # Um elemento não pode se relacionar com ele mesmo.
            print("É irreflexiva.")

            queryResult = propertyGraph.query(
                """
                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX owl: <http://www.w3.org/2002/07/owl#>
                PREFIX ontology: <""" + ontologyPrefix + """>
                SELECT DISTINCT ?subject
                    WHERE {
                        ?subject ontology:""" + property + """ ?subject .
                    }
                """)

            if not queryResult:
                print("\tEstá consistente.")
            else:
                print("\tEstá inconsistente.")
                errors = ''
                for row in qres:
                    errors += row[0].split('#')[-1] + ', '
                print("\tA inconsistência está em: " + errors)
