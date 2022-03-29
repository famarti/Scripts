#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#%% ALBUM DE FIGURITAS - COMPRANDO DE 1 EN 1.

import random
import numpy as np

def crear_album(figus_total):
    album = np.zeros(figus_total)
    return album

def album_incompleto(A):
    if 0 in A:
        return True
    else: 
        return False

def comprar_figu(figus_total):
    fig = random.randint(0,figus_total-1)
    return fig

def cuantas_figus(figus_total):
    alb = crear_album(figus_total)
    figus = 0
    while album_incompleto(alb) == True:
        me_toco_esta = comprar_figu(figus_total)
        alb[me_toco_esta] = 1
        figus += 1
    return figus

# n_repeticiones = 1000
# figus_total = 6
# simulaciones = [cuantas_figus(figus_total) for _ in range(n_repeticiones)]
# print(f'Si comprás de a 1 figurita, para completar el album de 6 deberías comprar {int(np.mean(simulaciones))} en promedio')

n_repeticiones=100
figus_total = 670
simulaciones = [cuantas_figus(figus_total) for _ in range(n_repeticiones)]
print(f'Si comprás de a 1 figurita, para completar el album de 670 deberías comprar {int(np.mean(simulaciones))} en promedio')
#%% AHORA CON PAQUETES DE 5 FIGUS

import random
import numpy as np

def crear_album(figus_total):
    album = np.zeros(figus_total)
    return album

def album_incompleto(A):
    if 0 in A:
        return True
    else: 
        return False

def comprar_paquete(figus_total, figus_paquete):
    paquete =[random.randint(0,figus_total - 1) for _ in range(figus_paquete)]
    return paquete

def cuantos_paquetes(figus_total, figus_paquete):
    alb = crear_album(figus_total)
    paq = 0
    while album_incompleto(alb) == True:
        me_tocaron = comprar_paquete(figus_total,figus_paquete)
        for fig in me_tocaron:
            alb[fig] = 1
        paq += 1
    return paq

n_repeticiones = 100
figus_total = 670
figus_paquete = 5
simulaciones = [cuantos_paquetes(figus_total, figus_paquete) for _ in range(n_repeticiones)]
print(f'Para completar el album se necesitaron en promedio {int(np.mean(simulaciones))} paquetes de figus.')

#%% PLOT QUE EXPLICITARON EN EL GIT
import matplotlib.pyplot as plt
def calcular_historia_figus_pegadas(figus_total, figus_paquete):
    album = crear_album(figus_total)
    historia_figus_pegadas = [0]
    while album_incompleto(album):
        paquete = comprar_paquete(figus_total, figus_paquete)
        while paquete:
            album[paquete.pop()] = 1
        figus_pegadas = (album>0).sum()
        historia_figus_pegadas.append(figus_pegadas)        
    return historia_figus_pegadas

#COMENTO LAS SIGUIENTES PORQUE LAS TENGO DE ANTES
#figus_total = 670
#figus_paquete = 5

plt.plot(calcular_historia_figus_pegadas(figus_total, figus_paquete))
plt.xlabel("Cantidad de paquetes comprados.")
plt.ylabel("Cantidad de figuritas pegadas.")
plt.title("La curva de llenado se desacelera al final")
plt.show()

#%%













