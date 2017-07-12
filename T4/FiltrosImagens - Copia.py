# -*- coding: utf-8 -*-
"""
Implementacao dos filtros da Mediana e de Wiener Adaptativo Pontual 
para tratar o ruido impulssivo e o Gaussiano, respectivamente
@autores: Caroline Santos e Douglas Antonio Martins Barbino
"""
import skimage
import numpy as np
from skimage import io
from skimage import exposure

def FiltroMediana(imagem,dimensaoJanela):
    #Converte a imagem para float
    imagemFloat = skimage.util.img_as_float(imagem)
    if (imagemFloat.max() != 1.0):
        valorNormalizacao = imagemFloat.max()
        #Percorre a altura da imagem
        for i in range(0, imagem.shape[0]):
            #Percorre a largura da imagem
            for j in range(0, imagem.shape[1]):
                imagemFloat[i][j] = imagemFloat[i][j] / valorNormalizacao
    imagemTratada = np.zeros(shape=(imagem.shape[0],imagem.shape[1]))
    exposure.rescale_intensity(imagemTratada, in_range=(-1, 1))
    pixels = dimensaoJanela*dimensaoJanela
    #Momento de percorrer a imagem para trata-la (loop externo = altura; loop interno = largura)
    for i in range(0, imagem.shape[0]):
        for j in range(0, imagem.shape[1]):
            elementos_janela=[]
            for k in range (pixels):
                #- Primeira coordenada lida com a altura, segunda com a largura.
                #- (dimensaoJanela-1)/2 porque queremos a mesma quantidade de pixels 
                #anteriores e posteriores a janela, alem do pixel na mesma coordenada
                elementos_janela.append(imagemFloat[((k//dimensaoJanela)+i-((dimensaoJanela-1)/2))%imagem.shape[0]][((k%dimensaoJanela)+j-((dimensaoJanela-1)/2))%imagem.shape[1]] )
            
                #- Primeira coordenada lida com a altura, segunda com a largura.
                #- (dimensaoJanela-1)/2 porque queremos a mesma quantidade de pixels 
                #anteriores e posteriores a janela, alem do pixel na mesma coordenada
            size_elementos = len(elementos_janela)
            indiceMediana = size_elementos/2
            elementos_janela.sort()
            mediana = elementos_janela[int(indiceMediana)]
            #Atribuicao do pixel tratado na nova imagem
            imagemTratada[i][j] = mediana
    return imagemTratada
            
    
def FiltroWiener(imagem, dimensaoJanela, sigmaN):
    #Converte a imagem para float
    imagemFloat = skimage.util.img_as_float(imagem)
    #Normalizacao da imagem caso ela nao tenha nenhum pixel branco ([255, 255, 255], 1.0 em float)
    if (imagemFloat.max() != 1.0):
        valorNormalizacao = imagemFloat.max()
        #Percorre a altura da imagem
        for i in range(0, imagem.shape[0]):
            #Percorre a largura da imagem
            for j in range(0, imagem.shape[1]):
                imagemFloat[i][j] = imagemFloat[i][j] / valorNormalizacao
    #Cria uma matriz vazia que sera a saida
    imagemTratada = np.zeros(shape=(imagem.shape[0],imagem.shape[1]))
    #Armazena o numero de pixels que a janela possui
    pixels = dimensaoJanela * dimensaoJanela
    #Momento de percorrer a imagem para trata-la (loop externo = altura; loop interno = largura)
    for i in range(0, imagem.shape[0]):
        for j in range(0, imagem.shape[1]):
            #Limpa algumas variaveis
            miF = 0 #media
            sigmaF = 0 #variancia na janela
            sigmaS = 0 #variancia local
            for k in range (pixels):
                #- Primeira coordenada lida com a altura, segunda com a largura.
                #- (dimensaoJanela-1)/2 porque queremos a mesma quantidade de pixels 
                #anteriores e posteriores a janela, alem do pixel na mesma coordenada
                miF += (1/pixels) * imagemFloat[((k//dimensaoJanela)+i-((dimensaoJanela-1)/2))%imagem.shape[0]][((k%dimensaoJanela)+j-((dimensaoJanela-1)/2))%imagem.shape[1]] 
            for k in range (pixels):
                sigmaF += (1/pixels) * (imagemFloat[((k//dimensaoJanela)+i-((dimensaoJanela-1)/2))%imagem.shape[0]][((k%dimensaoJanela)+j-((dimensaoJanela-1)/2))%imagem.shape[1]] - miF)**2
            #Modifica sigmaS caso sigmaF - sigmaN sejam maiores do que 0, 
            #caso contrario fica o valor limpo anteriormente
            if (sigmaF - sigmaN > 0):
                sigmaS = sigmaF - sigmaN
            #Atribuicao do pixel tratado na nova imagem
            imagemTratada[i][j] = miF + (sigmaS * (imagemFloat[i][j] - miF) / (sigmaS + sigmaN))
    return imagemTratada
    
#Carrega a imagem
imagem1 = io.imread('imagens_ruidosas\camera_gaussian.png')
imagem2= io.imread('imagens_ruidosas\camera_sal_e_pimenta.png')

'''--Testes--'''
#Coordenadas
#print(imagem1.shape)
#Altura
#print(imagem1.shape[0])
#Largura
#print(imagem1.shape[1])
'''----------'''
#Imprime a imagem
#io.imshow(imagem)

#imagem1Tratada = FiltroWiener(imagem1, 5, 0.01)
#Salvar imagem tratada
#io.imsave('imagens_ruidosas\camera_gaussian_tratada5.png', imagem1Tratada)
imagem2Tratada = FiltroMediana(imagem2,3)
#Salvar imagem tratada
io.imsave('imagens_ruidosas\camera_sal_e_pimenta_tratada.png', imagem2Tratada)