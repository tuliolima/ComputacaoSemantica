# OntoFlora 1.0
# userInterface.py
# 
# Módulo de interface com usuário do motor OntoFlora.

import os
import sys
from search import *
from consistencia import *
from utils import *
from rdflib import Graph


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def quit():
    print("Goodbye!")
    input()
    cls()


def user_consistency():
    consistencyEval()
    input()


def user_search():

    option = 'DO'
    while(option != 'BACK'):
        cls()
        print("\n")
        print("- QUERY")
        print("- NEW RELATION")
        print("- BACK")
        print("\n")

        option = input("option: ").upper()

        if(option == 'QUERY'):
            exp = input(
                "Insira expressão bool utilizando 'and', 'or' e 'not': ")
            resultado = search(exp)

            print("------------------------------------")
            print("Resultado da Query: ")
            print(resultado)
            print("------------------------------------")
            print("\n")
            input()

        elif(option == 'NEW RELATION'):
            rel = input("Insira o nome da nova relação: ")
            exp = input("Insira a expressão utilizando 'and', 'or', e 'not': ")

            newRelation(rel, exp)


def user_utils(g):

    option = 'DO'
    while(option != 'BACK'):
        cls()
        print("\n")
        print("- INDIVIDUALS")
        print("- CLASSES")
        print("- PROPERTIES")
        print("- BACK")
        print("\n")

        option = input("option: ").upper()

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

    cls()

    if len(sys.argv) < 3:
        ontologyName = input("Ontology name: ")
        ontologyPath = input("Ontology path: ")
    else:
        ontologyName = sys.argv[1]
        ontologyPath = sys.argv[2]

    g = Graph()
    g.parse(ontologyPath)
    ontologyPrefix = ''
    namespaces = g.namespaces()
    for (name, prefix) in namespaces:
        if name == ontologyName:
            ontologyPrefix = str(prefix)

    configConsistencia(g, ontologyPrefix)
    configSearch(g, ontologyPrefix)

    option = 'DO'
    while(option != 'QUIT'):
        cls()
        print("\n")
        print("- SEARCH")
        print("- UTILS")
        print("- CONSISTENCY")
        print("- QUIT")
        print("\n")

        option = input("option: ").upper()

        if(option == 'SEARCH'):
            cls()
            user_search()
        elif(option == 'UTILS'):
            cls()
            user_utils(g)
        elif(option == 'CONSISTENCY'):
            cls()
            user_consistency()

    cls()
    quit()
