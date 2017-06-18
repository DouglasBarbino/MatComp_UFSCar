# -*- coding: utf-8 -*-
"""
Implementacao dos filtros da Mediana e de Wiener Adaptativo Pontual 
para tratar o ruido impulssivo e o Gaussiano, respectivamente
@autores: Caroline Santos e Douglas Antonio Martins Barbino
"""
import skimage
import numpy as np
from skimage import io

def FiltroMediana(imagem):
    return
    
def FiltroWiener(imagem, dimensaoJanela, sigmaN):
    #Converte a imagem para float
    imagemFloat = skimage.util.img_as_float(imagem)
    #Normalizacao da imagem caso ela nao tenha nenhum pixel (255, 255, 255)
    if (imagemFloat.max() != 1.0):
        valorNormalizacao = imagemFloat.max()
        for i in range(0, imagem.shape[0]):
            for j in range(0, imagem.shape[1]):
                imagemFloat[i][j] = imagemFloat[i][j] / valorNormalizacao
    #Cria uma matriz vazia que sera a saida
    imagemTratada = np.zeros(shape=(imagem.shape[0],imagem.shape[1]))
    #Armazena o numero de pixels que a janela possui
    pixels = dimensaoJanela * dimensaoJanela
    #Momento de percorrer a imagem para trata-la
    for i in range(0, imagem.shape[0]):
        for j in range(0, imagem.shape[1]):
            #Limpa a variavel onde fica a media na janela ao redor do pixel
            media = 0
            #Coleta a media
            for k in range (pixels):
                #- Primeira coordenada lida com a altura, segunda com a largura.
                #- (dimensaoJanela-1)/2 porque queremos a mesma quantidade de pixels 
                #anteriores e posteriores a janela, alem do pixel na mesma coordenada
                media += (1/pixels) * imagemFloat[((k//dimensaoJanela)+i-((dimensaoJanela-1)/2))%imagem.shape[0]][((k%dimensaoJanela)+j-((dimensaoJanela-1)/2))%imagem.shape[1]] 
    #print(imagemFloat)
    #print(imagemFloat[0][0])
    #print(imagemFloat[0][-1])
    #Imprime a imagem
    io.imshow(imagem)
    return imagemTratada
    
#Carrega a imagem
imagem1 = io.imread('imagens_ruidosas\camera.png')

'''Testes'''
#Coordenadas
print(imagem1.shape)
#Altura
print(imagem1.shape[0])
#Largura
print(imagem1.shape[1])

imagem1Tratada = FiltroWiener(imagem1, 5, 0.01)