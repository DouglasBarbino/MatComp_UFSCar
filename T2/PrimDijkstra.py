# -*- coding: utf-8 -*-
"""
Implementacao dos algoritmos de Prim e Dijkstra
@autores: Caroline Santos e Douglas Antonio Martins Barbino
"""

import networkx as nx
import random as rm

def Prim ():
    return

def Dijkstra ():
    return
    
G = nx.read_edgelist('women.txt', nodetype=int, data=(('weight',float),))
print(G.nodes())
print(G.edges(data = True))