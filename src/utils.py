import rdflib

def printIndividuals (g):
    qres = g.query(
    """
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    SELECT DISTINCT ?individual
        WHERE {
            ?individual rdf:type owl:NamedIndividual.
        }
    """)

    print("\nIndivíduos:\n")
    for row in qres:
        result_1 = row[0]
        print(result_1.split('#')[-1])

def printClasses (g):
    qres = g.query(
    """
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

def printProperties (g):
    qres = g.query(
    """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    SELECT DISTINCT ?property ?domain ?range
        WHERE {
            ?property rdf:type owl:ObjectProperty .
            ?property rdfs:range ?range .
            ?property rdfs:domain ?domain.
        }
    """)

    print("\nRelações:\n")
    for row in qres:
        result_1 = row[0]
        result_2 = row[1]
        result_3 = row[2]
        print(result_1.split('#')[-1] + " (" + result_2.split('#')[-1] + ", " + result_3.split('#')[-1] + ")")