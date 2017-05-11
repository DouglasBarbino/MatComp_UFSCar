# -*- coding: utf-8 -*-
"""
Implementacao dos algoritmos de Prim e Dijkstra
@autores: Caroline Santos e Douglas Antonio Martins Barbino
"""

import networkx as nx
import numpy as np
import random as rm

def Prim (GP, raizGP):
    return

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
Prim(GP, raizGP)

#Leitura de um grafo por meio de uma matriz de adjacencia
MAdj = np.loadtxt('cidades.txt')
GD = nx.from_numpy_matrix(MAdj)
#print(GD.nodes())
#print(GD.edges(data = True))