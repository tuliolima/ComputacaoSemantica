#!/usr/bin/python
# -*- coding: UTF-8 -*-

import rdflib

g = rdflib.Graph()

# ... add some triples to g somehow ...
g.parse("../ontologias/engenhariaFlorestalRDF.owl")

qres = g.query(
    """PREFIX ontology:   <http://www.semanticweb.org/tulio/ontologies/2018/3/engenhariaFlorestal#>
    SELECT DISTINCT ?cidade ?pais
        WHERE {
            ?cidade ontology:localizado_em ?estado .
            ?estado ontology:localizado_em ?pais
        }""")

print("\nCidades:\n")
for row in qres:
    local_1 = row[0]
    local_2 = row[1]
    print(local_1.split('#')[-1] + " localizado em " + local_2.split('#')[-1])

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

qres = g.query(
    """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    SELECT DISTINCT ?property ?domain ?range
        WHERE {
            ?property rdf:type owl:DatatypeProperty .
            ?property rdfs:range ?range .
            ?property rdfs:domain ?domain.
        }
    """)

print("\nRelações:\n")
for row in qres:
    result_1 = row[0]
    result_2 = row[1]
    result_3 = row[2]
    print(result_1.split('#')[-1] + " (" + result_2.split('#')[-1] + " ," + result_3.split('#')[-1] + ")")