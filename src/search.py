from rdflib import Graph
from rdflib import URIRef
from rdflib.namespace import RDF
from rdflib import Namespace
import utils

ontology = Namespace('http://www.semanticweb.org/tulio/ontologies/2018/3/engenhariaFlorestal#')
ontologyPrefix = 'http://www.semanticweb.org/tulio/ontologies/2018/3/engenhariaFlorestal#'

transitiveProperty = URIRef('http://www.w3.org/2002/07/owl#TransitiveProperty')
funtionalProperty = URIRef('http://www.w3.org/2002/07/owl#FunctionalProperty')
asymmetricProperty = URIRef('http://www.w3.org/2002/07/owl#AsymmetricProperty')
irreflexiveProperty = URIRef('http://www.w3.org/2002/07/owl#IrreflexiveProperty')

class Stack:
     def __init__(self):
         self.items = []

     def isEmpty(self):
         return self.items == []

     def push(self, item):
         self.items.append(item)

     def pop(self):
         return self.items.pop()

     def peek(self):
         return self.items[len(self.items)-1]

     def size(self):
         return len(self.items)

def isOperator(char):
    return char == 'v' or char == '&'

def hasPriority(char):
    return char == 'v'

def BoolEval(v1,v2,op):
    
    g = Graph()
    g.parse("../ontologias/engenhariaFlorestalRDF.owl")

    if(op == 'v'):
        return queryTripleString(g, ontologyPrefix, v1) or queryTripleString(g, ontologyPrefix, v2)
    else:
        return queryTripleString(g, ontologyPrefix, v1) and queryTripleString(g, ontologyPrefix, v2)

def Infix_Eval(expression):

    # Avalia a expressão infixa
    # TODO: NAO PRECISA DE MODIFICACOES 
    stack = Stack()

    for exp in expression:
        if(isOperator(exp)):
            value = BoolEval(stack.pop(),stack.pop(),exp)
            stack.push(value)
        else:
            stack.push(exp) 
    
    return stack.pop()

def StringEval(entrada):
    
    # Transforma a expressão infixa fornecida em uma expressao pos-fixa
    # TODO: NAO NECESSITA DE MODIFICAÇOES 
    saida = []
    stack = Stack()

    for exp in entrada:
        if(isOperator(exp)):
            while((not stack.isEmpty()) and hasPriority(exp)):
                op = stack.pop()
                saida.append(op)
            stack.push(exp)     
        else:
            saida.append(exp)

    while(not stack.isEmpty()):
        saida.append(stack.pop())

    return saida  
        

def validateTriple(g, ontologyPrefix, subject = None, predicate = None, object = None):
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
        isAsymmetric = False
        isIrreflexive = False
        for row in queryResult:
            result = row[0]
            if (result == transitiveProperty):
                # A propriedade é transitiva, devemos resolver a transitividade
                print("Debug: A relação é transitiva")
                isTransitive = True
            if (result == asymmetricProperty):
                # A propriedade é assimétrica
                print("Debug: A relação é assimétrica")
                isAsymmetric = True
            if (result == irreflexiveProperty):
                # A propriedade é irreflexiva
                print("Debug: A relação é irreflexiva")
                isIrreflexive = True

        # Verificar irreflexividade
        if (isIrreflexive and subject == object):
            return False

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



def queryTripleString(graph, ontologyPrefix, triple):
    """
    Recebe uma string no formato (sujeito, predicado, objeto).

    Retorna um booleano indicando se a tripla existe ou não.
    """
    if(triple == True or triple == False):
        return triple

    # retirando os parêntesis
    triple = triple[1:-1]
    # dividindo os termos
    s, p, o = triple.split(',')
    # print(s, p, o)
    
    return validateTriple(graph, ontologyPrefix, s, p, o)

if __name__ == "__main__":

    g = Graph()
    g.parse("../ontologias/engenhariaFlorestalRDF.owl")
    # utils.printIndividuals(g)
    # utils.printClasses(g)
    # utils.printProperties(g)

    entrada = input("Digite a tripla: ")
    infixa = input("Digite uma expressão booleana infixa utilizando '&' e 'v': ")

    infixa = infixa.split(" ")
    print(infixa)
    infixa = StringEval(infixa)

    print(infixa)

    print(Infix_Eval(infixa))

    result = queryTripleString(g, ontologyPrefix, entrada)

    if (result):
        print('Existe!')
    else:
        print('Não existe!')