# -*- coding: utf-8 -*-
#%%Ejercicio 8.13: Otros puertos

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

df_zar = pd.read_csv('../Data/OBS_Zarate_2013A.csv', index_col = ['Time'], parse_dates = True )
df = pd.read_csv('../Data/OBS_SHN_SF-BA.csv', index_col=['Time'], parse_dates=True)

inicio = '2013-01'
fin = '2013-06'
alturas_zar = df_zar[inicio:fin]['H_Zarate'].to_numpy()
alturas_ba = df[inicio:fin]['H_BA'].to_numpy()

def calcular_fft(y, freq_sampleo = 24.0):
    '''y debe ser un vector con números reales
    representando datos de una serie temporal.
    freq_sampleo está seteado para considerar 24 datos por unidad.
    Devuelve dos vectores, uno de frecuencias 
    y otro con la transformada propiamente.
    La transformada contiene los valores complejos
    que se corresponden con respectivas frecuencias.'''
    N = len(y)
    freq = np.fft.fftfreq(N, d = 1/freq_sampleo)[:N//2]
    tran = (np.fft.fft(y)/N)[:N//2]
    return freq, tran

freq_zar, fft_zar = calcular_fft(alturas_zar)

plt.plot(freq_zar, np.abs(fft_zar))
plt.xlabel("Frecuencia")
plt.ylabel("Potencia (energía)")
plt.show()

# np.abs(fft_zar[0])
# Out[73]: 81.58902098429952

# print(signal.find_peaks(np.abs(fft_zar), prominence = 5))
# (array([ 22, 350], dtype=int64), {'prominences': array([5.00589774, 5.47517271]), 
#                                   'left_bases': array([  6, 323], dtype=int64), 
#                                   'right_bases': array([ 323, 1379], dtype=int64)})

plt.plot(freq_zar, np.abs(fft_zar))
plt.xlabel("Frecuencia")
plt.ylabel("Potencia (energía)")
plt.xlim(0,4)
plt.ylim(0,20)
# me quedo solo con el último pico
pico_zar = signal.find_peaks(np.abs(fft_zar), prominence = 5)[0][-1]
# es el pico a analizar, el de la onda de mareas
# marco ese pico con un circulito rojo
plt.scatter(freq_zar[pico_zar], np.abs(fft_zar)[pico_zar], facecolor = 'r')
plt.show()

# freq_zar[350]
# Out[96]: 1.9337016574585635

ang_zar = np.angle(fft_zar)[pico_zar]
# ang_zar * 24 / (2 * np.pi * freq_zar[350])
# Out[99]: -2.5569083509582056

freq_ba, fft_ba = calcular_fft(alturas_ba)
plt.plot(freq_ba, np.abs(fft_ba))
plt.xlabel("Frecuencia")
plt.ylabel("Potencia (energía)")
plt.xlim(0,4)
plt.ylim(0,20)
# me quedo solo con el último pico
pico_ba = signal.find_peaks(np.abs(fft_ba), prominence = 8)[0][-1]
#se grafican los picos como circulitos rojos
plt.scatter(freq_ba[pico_ba], np.abs(fft_ba)[pico_ba], facecolor='r')
plt.title("Espectro de Potencias Bs.As.")
plt.show()

# np.abs(fft_ba[0])
# Out[101]: 98.54696132596685

# np.abs(fft_zar[0])
# Out[102]: 68.8526204726826

# np.abs(fft_ba[350])
# Out[107]: 11.119093783070157

# np.abs(fft_zar[350])
# Out[108]: 5.489401479214873

ang_ba = np.angle(fft_ba)[pico_ba]
freq = freq_ba[pico_ba]
ang2h = 24 / (2*np.pi*freq)


retardo_onda = (ang_ba - ang_zar) * ang2h #2.909420525253802 algo menos de 3 horas tarda en llegar la onda a bsas
#%%