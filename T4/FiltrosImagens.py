# -*- coding: utf-8 -*-
"""
Implementacao dos filtros da Mediana e de Wiener Adaptativo Pontual 
para tratar o ruido impulssivo e o Gaussiano, respectivamente
@autores: Caroline Santos e Douglas Antonio Martins Barbino
"""
import skimage
from skimage import io
#Carrega a imagem
imagem1 = io.imread('imagens_ruidosas\camera.png')
#Converte a imagem para float
imagem1Float = skimage.util.img_as_float(imagem1)
#Imprime a imagem
io.imshow(imagem1)