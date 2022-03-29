#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#%% Ejercicio 4.18: Lectura de todos los árboles
#   Ejercicio 4.19: Lista de altos de Jacarandá
#   Ejercicio 4.20: Lista de altos y diámetros de Jacarandá
#   Ejercicio 4.21: Diccionario con medidas

import csv
def leer_arboles(nombre_archivo):
    with open(nombre_archivo, 'rt') as f:
        headers = next(f).strip('\n').split(',')
        filas= csv.reader(f, delimiter = "," )
        arboleda = []
        for fila in filas:
            arbol = dict(zip(headers,fila))
            arboleda.append(arbol) 
    return arboleda

nombre_archivo = '/home/famarti/Documents/Ejercicios/ejercicios_python/Data/arbolado.csv'

arboleda = leer_arboles(nombre_archivo)

jac_alt = [ (float(x['altura_tot']), float(x['diametro'])) for x in arboleda if x['nombre_com'] == 'Jacarandá']


def medidas_de_especies(especies,arboleda):
    resumen = { k : [ (float(j['altura_tot']), float(j['diametro'])) for j in arboleda if j['nombre_com'] == k ] for k in especies}
    return resumen

especies = ['Eucalipto', 'Palo borracho rosado', 'Jacarandá']

dic = medidas_de_especies(especies,arboleda)

#%%







