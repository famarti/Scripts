#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#%% Ejercicio 7.10: Caminatas al azar

import numpy as np
import matplotlib.pyplot as plt
import random

def randomwalk(largo):
    pasos=np.random.randint (-1,2,largo)    
    return pasos.cumsum()

N = 100000
colores = [ tuple(random.random() for _ in range(3)) for _ in range(12)]
#color = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
#             for i in range(number_of_colors)]
fig = plt.figure(figsize=(15,10))
max_values = []
curvas= []
plt.subplot(2,1,1)
plt.xticks([]), plt.yticks([-500,0,500])
plt.ylim(-600,600)
plt.title('12 caminatas al azar')
for i in range(12):
    curva = randomwalk(N)
    curvas.append(curva)
    curva_val_max = max([abs(ele) for ele in curva])
    max_values.append(curva_val_max)
    plt.plot(curva, color = colores[i])


plt.subplot(2,2,3)
lejana = max(max_values)
lejana_idx = max_values.index(lejana)
plt.title('La caminata que más se aleja')
plt.ylim(-600,600)
plt.plot(curvas[lejana_idx], color = colores[lejana_idx])
plt.xticks([]), plt.yticks([-500,0,500])

plt.subplot(2,2,4)
cercana = min(max_values)
cercana_idx = max_values.index(cercana)
plt.title('La caminata que menos se aleja')
plt.ylim(-600,600)
plt.plot(curvas[cercana_idx], color = colores[cercana_idx])
plt.xticks([]), plt.yticks([])

# fig = plt.figure()
# plt.subplot(2, 1, 1) # define la figura de arriba
# plt.plot([0,1,2],[0,1,0]) # dibuja la curva
# plt.xticks([]), plt.yticks([]) # saca las marcas

# plt.subplot(2, 2, 3) # define la primera de abajo, que sería la tercera si fuera una grilla regular de 2x2
# plt.plot([0,1],[0,1])
# plt.xticks([]), plt.yticks([])

# plt.subplot(2, 2, 4) # define la segunda de abajo, que sería la cuarta figura si fuera una grilla regular de 2x2
# plt.plot([0,1],[1,0])
# plt.xticks([]), plt.yticks([])

# plt.show()

#%%
