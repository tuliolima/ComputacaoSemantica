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

class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None

class HashMap:
    def __init__(self):
        self.store = [None for _ in range(16)]
    def get(self, key):
        index = hash(key) & 15
        if self.store[index] is None:
            return None
        n = self.store[index]
        while True:
            if n.key == key:
                return n.value
            else:
                if n.next:
                    n = n.next
                else:
                    return None
    def put(self, key, value):
        nd = Node(key, value)
        index = hash(key) & 15
        n = self.store[index]
        if n is None:
            self.store[index] = nd
        else:
            if n.key == key:
                n.value = value
            else:
                while n.next:
                    if n.key == key:
                        n.value = value
                        return
                    else:
                        n = n.next
                n.next = nd

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

Global_HashMap = HashMap()

def isOperator(char):
    return char == 'or' or char == 'and' or char == 'not'

def hasPriority(char):
   return char == 'or'

def BoolEval(stack,op):

        
    g = Graph()
    g.parse("../ontologias/engenhariaFlorestalRDF.owl")

    if(op == 'or'):
        return queryTripleString(g, ontologyPrefix, stack.pop()) or queryTripleString(g, ontologyPrefix, stack.pop())
    elif(op == 'and'):
        return queryTripleString(g, ontologyPrefix, stack.pop()) and queryTripleString(g, ontologyPrefix, stack.pop())
    elif(op == 'not'):
        return not queryTripleString(g,ontologyPrefix,stack.pop())
    else:
        return queryTripleString(g,ontologyPrefix,stack.pop())    

def Infix_Eval(expression):

    # Avalia a expressão infixa
    # TODO: NAO PRECISA DE MODIFICACOES 
    stack = Stack()

    if(len(expression) == 1):
        return BoolEval(expression,' ')

    for exp in expression:
        if(isOperator(exp)):
            value = BoolEval(stack,exp)
            stack.push(value)
        else:
            stack.push(exp) 
    
    return stack.pop()

def isCloseBracket(char):
    return char == ']'

def isOpenBracket(char):
    return char == '['

def StringEval(entrada):
    
    # Transforma a expressão infixa fornecida em uma expressao pos-fixa
    # TODO: NAO NECESSITA DE MODIFICAÇOES 
    saida = []
    stack = Stack()

    for exp in entrada:

        if(isOperator(exp)):
            while((not stack.isEmpty()) and hasPriority(exp) and not isOpenBracket(stack.peek())):
                op = stack.pop()
                saida.append(op)
            stack.push(exp)

        elif(isOpenBracket(exp)):
            stack.push(exp)

        elif(isCloseBracket(exp)):
            aux = stack.pop()
            while(not isOpenBracket(aux)):
                saida.append(aux)
                aux = stack.pop()

        else:
           saida.append(exp)    

    while(not stack.isEmpty()):
        aux = stack.pop() 
        if(not isOpenBracket(aux)):
            saida.append(aux)

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

def newRelation(rel,exp):
    exp = exp.split(" ")
    Global_HashMap.put(rel,exp)

    
def evalRelation(triple):

    i = 0
    
    triple = triple[1:-1]
    s, p, o = triple.split(',')
    relation = Global_HashMap.get(p)

    if(relation == None):
        return 
   
    for exp in relation:
        if(not isOperator(exp) and not isCloseBracket(exp) and not isOpenBracket(exp)):
            relation[i] = "(" + s + "," + exp + "," + o + ")"
        i += 1

    relation = StringEval(relation)
    print(relation)
    return Infix_Eval(relation)
    

def queryTripleString(graph, ontologyPrefix, triple):
    """o
    Recebe uma string no formato (sujeito, predicado, objeto).

    Retorna um booleano indicando se a tripla existe ou não.
    """

    if(triple == True or triple == False):
        return triple

    # retirando os parênteses
    triple = triple[1:-1]
    # dividindo os termos
    s, p, o = triple.split(',')
    # print(s, p, o)

    if(Global_HashMap.get(p) != None):
        return evalRelation("("+s+","+p+","+o+")")
    return validateTriple(graph, ontologyPrefix, s, p, o)

def search(exp):      
    g = Graph()
    g.parse("../ontologias/engenhariaFlorestalRDF.owl")


    exp = exp.split(" ")
    print(exp)
    exp = StringEval(exp)

    print(exp)

    print(Infix_Eval(exp))