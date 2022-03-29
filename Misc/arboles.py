#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#%% Ejercicio 4.18: Lectura de todos los árboles
#   Ejercicio 4.19: Lista de altos de Jacarandá
#   Ejercicio 4.20: Lista de altos y diámetros de Jacarandá
#   Ejercicio 4.21: Diccionario con medidas

import csv
import os
import matplotlib.pyplot as plt
import numpy as np
def leer_arboles(nombre_archivo):
    with open(nombre_archivo, 'rt') as f:
        headers = next(f).strip('\n').split(',')
        filas= csv.reader(f, delimiter = "," )
        arboleda = []
        for fila in filas:
            arbol = dict(zip(headers,fila))
            arboleda.append(arbol) 
    return arboleda

nombre_archivo = os.path.join('/home', 'famarti', 'Documents', 'Ejercicios', 'ejercicios_python' , 'Data' , 'arbolado.csv')

arboleda = leer_arboles(nombre_archivo)

#jac_alt = [ (float(x['altura_tot']), float(x['diametro'])) for x in arboleda if x['nombre_com'] == 'Jacarandá']


#%% Ejercicio 5.25: Scatterplot (diámetro vs alto) de Jacarandás


#altos = [float(x['altura_tot']) for x in arboleda if x['nombre_com'] == 'Jacarandá']
#plt.hist(altos,bins=25)

h = np.array([float(x['altura_tot']) for x in arboleda if x['nombre_com'] == 'Jacarandá'])
d = np.array([float(x['diametro']) for x in arboleda if x['nombre_com'] == 'Jacarandá'])

n = len(h)
colores = np.random.rand(n)
plt.scatter(d,h, c = colores , alpha = 0.4 , s = 30 * (d/h))
plt.xlabel("diametro (cm)")
plt.ylabel("alto (m)")
plt.title("Relación diámetro-alto para Jacarandás")

# Se observa cierta relación directa entre la altura y el diámetro, no puedo asegurar
# si es lineal, cuadŕatica, logarítmica. La forma no me resulta clara..

#%% Ejercicio 5.26: Scatterplot para diferentes especies

def medidas_de_especies(especies,arboleda):
    resumen = { k : [ (float(j['altura_tot']), float(j['diametro'])) for j in arboleda if j['nombre_com'] == k ] for k in especies}
    return resumen

especies = ['Eucalipto', 'Palo borracho rosado', 'Jacarandá']
medidas = medidas_de_especies(especies,arboleda)
colores = ['b','g','r']
for especie in especies:
    plt.scatter(*zip(*medidas[especie]), c= colores.pop(), alpha=0.3, s=10)
    plt.xlim(0,30) 
    plt.ylim(0,200) 
    plt.xlabel("diametro (cm)")
    plt.ylabel("alto (m)")
    plt.title(f'Relación diámetro-alto para {especie}')
    plt.show()

#Pareciera que las relaciones para el palo borracho y el jacarandá son mucho más
#claras con respecto al Eucalipto, que denota mayor dispersión. Para un mismo alto,
# los eucaliptos típicamente tienen mayores diámetros que los otros dos.

#%% EXTRA

plt.scatter(*zip(*medidas['Eucalipto']), c= 'k', alpha=0.2, s=4)
plt.scatter(*zip(*medidas['Palo borracho rosado']), c= 'r', alpha=0.2, s=4)
plt.scatter(*zip(*medidas['Jacarandá']), c= 'g', alpha=0.2, s=4)
plt.xlim(0,50) 
plt.ylim(0,200)
plt.xlabel("diametro (cm)")
plt.ylabel("alto (m)")
plt.title("Relación diámetro-alto")
plt.show()

# P
#%%

