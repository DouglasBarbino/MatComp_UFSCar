# -*- coding: utf-8 -*-
"""
Implementacao dos algoritmos de Prim e Dijkstra
@autores: Caroline Santos e Douglas Antonio Martins Barbino
"""

import networkx as nx
import numpy as np
import random as rm

def Prim (GP, raizGP):
    #Inicializacao de um grafo que vai receber o MST resultante da execucao do Prim
    #e atribuicao de todos os nos que existem no grafo original
    GrafoPrim = nx.Graph()
    GrafoPrim.add_nodes_from(GP)
    #print(GrafoPrim.nodes())
    #print(GrafoPrim.edges(data = True))
    for i in GP.nodes():
        #atribui peso infinito para todos os nos, depois eh corrigido o do raiz
        GP.node[i]['peso'] = float('inf')
    GP.node[raizGP]['peso'] = 0
    #Percorre os nos para saber qual possui o menor peso
    while (GP.number_of_nodes() > 0):
        #limpa a variavel de menor peso
        menorPeso = float('inf')
        #verifica qual eh o vertice com menor peso, simulando a primitiva EXTRACT-MIN
        for i in GP.nodes():
            if GP.node[i]['peso'] <= menorPeso:
                verticeMenorPeso = i
                menorPeso = GP.node[i]['peso']
        # percorre todos os vizinhos do no com o menor peso
        for i in GP.neighbors(verticeMenorPeso):
            #Verifica se o peso da aresta eh menor que o peso armazendo ateh o momento
            if GP.node[i]['peso'] > GP.get_edge_data(verticeMenorPeso,i)['weight']:
                GP.node[i]['peso'] = GP.get_edge_data(verticeMenorPeso,i)['weight']
                #Armazena o peso e o vizinho do no para que, ao final da execucao, a MST seja criada
                GrafoPrim.node[i]['peso'] = GP.get_edge_data(verticeMenorPeso,i)['weight']
                GrafoPrim.node[i]['vizinho'] = verticeMenorPeso
        GP.remove_node(verticeMenorPeso)
    #Atribuicao das arestas escolhidas para compor a MST no grafo que estah apenas com os nos
    for i in GrafoPrim.nodes():
        #Raiz nao eh adicionada pois ela nao tem vizinho
        if (i != raizGP):            
            GrafoPrim.add_edge(i, GrafoPrim.node[i]['vizinho'], weight=GrafoPrim.node[i]['peso'])
    return GrafoPrim

def Dijkstra ():
    return
    
#Leitura de um grafo por meio de uma lista de arestas
GP = nx.read_edgelist('women.txt', nodetype=int, data=(('weight',float),))
#print(GP.nodes())
#print(GP.edges(data = True))

#Define um vertice inicial aleatorio
vertices = GP.nodes()
raizGP = vertices[rm.randint(0,GP.number_of_nodes()-1)]
#Chama o algoritmo de Prim. 
#Note que nao eh passada a lista de pesos das arestas como no algoritmo 
#original, pois ela eh facilmente obtida por GP.get_edge_data(v1, v2)['weight']
MSTPrim = Prim(GP, raizGP)
print(MSTPrim.nodes())
print(MSTPrim.edges(data = True))

#Leitura de um grafo por meio de uma matriz de adjacencia
MAdj = np.loadtxt('cidades.txt')
GD = nx.from_numpy_matrix(MAdj)
#print(GD.nodes())
#print(GD.edges(data = True))