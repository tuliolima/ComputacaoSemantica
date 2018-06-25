import os
from search import *
from consistencia import consistencyEval
from utils import *
from rdflib import Graph

def quit():
    os.system("clear")
    print("Goodbye!")
    input()

def user_consistency():
    os.system("clear")
    consistencyEval()
    input()


def user_search():
    os.system("clear")

    option = 'DO'
    while(option != 'QUIT'):
        print("\n")
        print("- QUERY")
        print("- NEW RELATION")
        print("- QUIT")
        print("\n")

        option = input("option: ")

        if(option == 'QUERY'):
            exp = input("Insira expressão bool utilizando 'and', 'or' e 'not': ")
            search(exp)
        elif(option == 'NEW RELATION'):
            rel = input("Insira o nome da nova relação: ")
            exp = input("Insira a expressão utilizando 'and', 'or', e 'not': ")
            
            newRelation(rel,exp)
    

def user_utils(g):
    os.system("clear")

    option = 'DO'
    while(option != 'QUIT'):
        print("\n")
        print("- INDIVIDUALS")
        print("- CLASSES")
        print("- PROPERTIES")
        print("- QUIT")
        print("\n") 

        option = input("option: ")

        if(option == 'INDIVIDUALS'):
            printIndividuals(g)
            input()
        elif(option == 'CLASSES'):
            printClasses(g)
            input()
        elif(option == 'PROPERTIES'):
            printProperties(g)
            input()

if __name__ == "__main__":

    g = Graph()
    g.parse("../ontologias/engenhariaFlorestalRDF.owl")

    option = 'DO'
    while(option != 'QUIT'):
        print("\n")
        print("- SEARCH")
        print("- UTILS")
        print("- CONSISTENCY")
        print("- QUIT")
        print("\n")
        
        option = input("option: ")

        if(option == 'SEARCH'):
            os.system("clear")
            user_search()
        elif(option == 'UTILS'):
            os.system("clear")
            user_utils(g)
        elif(option == 'CONSISTENCY'):
            os.system("clear")
            user_consistency()        

    quit()    