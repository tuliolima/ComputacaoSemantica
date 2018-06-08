#!/usr/bin/python
# -*- coding: UTF-8 -*-

import rdflib
from rdflib import 

def transitive_closure(gra, y, z):
    return gra.transitive_objects(y,z)


def detect_cycle(gra):
    import ipdb; ipdb.set_trace()
    for x,y,z in gra:
        teste = transitive_closure(gra, y, z)
        teste = [a for a in teste]
        teste = teste[1:]
        if x in teste:
            return True
    return False

transitiveProperty = URIRef('http://www.w3.org/2002/07/owl#TransitiveProperty')
funtionalProperty = URIRef('http://www.w3.org/2002/07/owl#FunctionalProperty')
asymmetricProperty = URIRef('http://www.w3.org/2002/07/owl#AsymmetricProperty')
irreflexiveProperty = URIRef('http://www.w3.org/2002/07/owl#IrreflexiveProperty')

if __name__ == "__main__":

    # ../ontologias/engenhariaFlorestalRDF.owl
    # ontologyName = input("Entre com o nome do arquivo da ontologia: ")

    ontologyName = "../ontologias/engenhariaFlorestalRDF.owl"
    g = rdflib.Graph()
    g.parse(ontologyName)
    
    ciclo = detect_cycle(g)
    if ciclo:
        print("Grafo tem ciclos")
    else:
        print("Grafo não tem ciclos")

    # Buscando Classes
    qres = g.query(
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
    properties = g.query(
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
        print(result_1.split('#')[-1] + " (" + result_2.split('#')[-1] + " ," + result_3.split('#')[-1] + ")")

    # Buscando Instâncias
    qres = g.query(
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

        # Temos que conhecer as suas características
        queryResult = g.query(
            """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX ontology: <http://www.semanticweb.org/tulio/ontologies/2018/3/engenhariaFlorestal#>
            SELECT DISTINCT ?propertyType
                WHERE {
                    ontology:""" + property + """ rdf:type owl:ObjectProperty .
                    ontology:""" + property + """ rdf:type ?propertyType .
                }
            """)

        if not queryResult:
            continue
            
        isFunctional = False
        isTransitive = False
        isAsymmetric = False
        isIrreflexive = False
        for row in queryResult:
            result = row[0]
            if (result == funtionalProperty):
                isFunctional = True
            if (result == transitiveProperty):
                isTransitive = True
            if (result == asymmetricProperty):
                isAsymmetric = True
            if (result == irreflexiveProperty):
                isIrreflexive = True

        print("\nAnalizando a relação " + property + ":")

        if isFunctional:
            print("É funcional.")

        if isTransitive:
            print("É transitiva.")

        if isAsymmetric:
            print("É assimétrica.")

            queryResult = g.query(
                """
                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX owl: <http://www.w3.org/2002/07/owl#>
                PREFIX ontology: <http://www.semanticweb.org/tulio/ontologies/2018/3/engenhariaFlorestal#>
                SELECT DISTINCT ?subject ?object 
                    WHERE {
                        ?subject ontology:""" + property + """ ?object .
                        ?object ontology:""" + property + """ ?subject .
                    }
                """)

            if not queryResult:
                print("Está consistente.")
            else:
                print("Está inconsistente.")
                # TODO Imprimir casos inconsistentes.

        if isIrreflexive:
            print("É irreflexiva.")

            queryResult = g.query(
                """
                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX owl: <http://www.w3.org/2002/07/owl#>
                PREFIX ontology: <http://www.semanticweb.org/tulio/ontologies/2018/3/engenhariaFlorestal#>
                SELECT DISTINCT ?subject
                    WHERE {
                        ?subject ontology:""" + property + """ ?subject .
                    }
                """)

            if not queryResult:
                print("Está consistente.")
            else:
                print("Está inconsistente.")
                # TODO Imprimir casos inconsistentes.
