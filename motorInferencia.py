from rdflib import Graph
from rdflib import URIRef
from rdflib.namespace import RDF
from rdflib import Namespace
################################################################################################################################################################
# Inicializa um TAD grafo e atribui a ontologia nele.
g = Graph()
g.parse("engenhariaFlorestalRDF.owl")

# Maneira elegante de acessar a URI sem precisar repeti-la.
ontology = Namespace('http://www.semanticweb.org/tulio/ontologies/2018/3/engenhariaFlorestal#')
########################### VARIAVEIS GLOBAIS    ###############################################################################################################

################################################################################################################################################################
def message(msg):
    print("#############################################")
    print(msg)
    print("#############################################")
######################### INTRO ################################################################################################################################
################################################################################################################################################################
def clima(cidade):
    print("\nTODO: Informações climáticas da cidade.\n")
    ####################################
    #### PROCEDURE #####################
########################## CLIMA ###############################################################################################################################
################################################################################################################################################################
################################################################################################################################################################
def flora_aux(planta):
    reficofage_stack = []
    reficofage_stack.append(planta.split('#')[-1])
    for(s,p,o) in g.triples((planta, ontology.pertence_a,None)):

        genero = o
        reficofage_stack.append(genero.split('#')[-1])

        for(s,p,o) in g.triples((genero, ontology.pertence_a,None)):
            familia = o
            reficofage_stack.append(familia.split('#')[-1])

        for(s,p,o) in g.triples((familia, ontology.pertence_a,None)):
            ordem = o
            reficofage_stack.append(ordem.split('#')[-1])

        for(s,p,o) in g.triples((ordem, ontology.pertence_a,None)):
            classe = o
            reficofage_stack.append(classe.split('#')[-1])    

        for(s,p,o) in g.triples((classe, ontology.pertence_a, None)):
            filo = o
            reficofage_stack.append(filo.split('#')[-1])    

        reficofage_stack.append("Plantae")
        return reficofage_stack
########################## FLORA AUX ###########################################################################################################################
################################################################################################################################################################
def printstack(stack):
    print("########## PLANTA ##################\n")
    print("Reino: " + stack.pop())
    print("Filo: " + stack.pop())
    print("Classe: " + stack.pop())
    print("Ordem: " + stack.pop())
    print("Familia: " + stack.pop())
    print("Genero: " + stack.pop())
    print("Espécie: " + stack.pop())
    print("\n####################################\n")
########################## PRINT STACK #########################################################################################################################
################################################################################################################################################################
def flora(cidade):
    # Itera sobre o grafo para encontrar o bioma predominante do estado.
    for (s,p,o) in g.triples((None, ontology.abrange, cidade)):
        bioma = s
    print('\nBioma pertencente:')
    print('   ' + bioma.split('#')[-1])

    print('\nPlantas apropriadas:\n')
    for (s,p,o) in g.triples((None, ontology.se_adapta_a, bioma)):
        printstack(flora_aux(s))        
########################## FLORA ###############################################################################################################################
################################################################################################################################################################
def cep(cidade):
    # Identifica o estado e o país
    for (s,p,o) in g.triples((cidade, ontology.localizado_em, None)):
        estado = o
    for (s,p,o) in g.triples((estado, ontology.localizado_em, None)):
        pais = o

    # Imprime as informações encontradas
    print('\nDados encontrados:')
    print('   ' + cidade.split('#')[-1] + ', ' + estado.split('#')[-1] + ', ' + pais.split('#')[-1])
########################## CEP #################################################################################################################################
################################################################################################################################################################
def ValidCity():
    # Captura e trata a entrada do usuário.
    cidade = URIRef('http://www.semanticweb.org/tulio/ontologies/2018/3/engenhariaFlorestal#' + input('\nInsira uma cidade:\n   '))
    # Força a entrada no Loop
    existe = True
    while existe:
        # Verifica se existe a cidade na ontologia e identifica o estado
        existe = False
        for (s, p, o) in g.triples((cidade, RDF.type, ontology.Cidade)):
            existe = True

        # Se a cidade existe continua a pesquisa
        if(existe):
            existe = False
        else:
            message("A cidade não existe na base de dados!")
            cidade = URIRef('http://www.semanticweb.org/tulio/ontologies/2018/3/engenhariaFlorestal#' + input('\nInsira uma nova cidade:\n   '))
            existe = True

    return cidade
######################### VALID CITY ###########################################################################################################################

########################## MAIN ################################################################################################################################
def main():
    # Cabeçalho
    message('Motor de inferência para Engenharia Florestal')
    # Input e tratamento de exceção do usuário.
    cidade = ValidCity()

    # Chamada para apresentação dos resultados.
    cep(cidade)
    flora(cidade)
    clima(cidade)
################################################################################################################################################################
main()





# TODO Informações das plantas, talvez um menu para escolher a planta e ver mais informações.