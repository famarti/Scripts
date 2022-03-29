# -*- coding: utf-8 -*-

from scipy import signal # para procesar señales
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('../Data/OBS_SHN_SF-BA.csv', index_col=['Time'], parse_dates=True)

#dh = df['12-25-2014':].copy()

inicio = '2014-01'
fin = '2014-06'
alturas_sf = df[inicio:fin]['H_SF'].to_numpy()
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

# Para poder analizar una onda por medio de su transformada de Fourier, 
# es necesario que la onda sea periódica. Puede pasar que no sea el caso y que una 
# onda tenga tendencia lineal, en ese caso podríamos usar la función scipy.signal.detrend().

# En nuestro caso supondremos que la marea media se mantuvo estable a lo 
# largo del período de estudio, así que no tenemos que hacerle este procesamiento intermedio.

# Espectro de potencia y de ángulos para San Fernando

freq_sf, fft_sf = calcular_fft(alturas_sf) #calculamos la transformada de las alturas de San Fernando.

# Si quisiéramos graficar freq_sf contra fft_sf no podríamos ver mucho 
# ya que fft_sf contiene números complejos.

# La potencia (o amplitud) para cada frecuencia se calcula como el módulo 
# del número complejo correspondiente (para la frecuencia freq_sf[i] y la 
#                                      potencia es abs(fft_sf[i])). 
# Al graficar esto podemos ver la amplitud de los sinusoides para cada frecuencia. 
# Este gráfico se llama el espectro de potencias de la onda original.

plt.plot(freq_sf, np.abs(fft_sf))
plt.xlabel("Frecuencia")
plt.ylabel("Potencia (energía)")
plt.show()

# A simple vista se observan dos picos, uno en frecuencia 0 (constante relacionada con el cero de escala) 
# y otro pico cercano a la frecuencia 2 (frecuencia semidiurna) que está relacionado con la onda de mareas.

# El pico en la primera posición efectivamente se corresponde con la frecuencia 0 y su amplitud es:

# >>> freq_sf[0]
# 0.0
# >>> np.abs(fft_sf[0])
# 111.83

# A partir de esto podemos decir que las alturas del río en San Fernando durante 
# este período oscilan alrededor de los 111.8 cm de altura.

# Para analizar precisamente el pico semidiurno podemos usar find_peaks que provee
# scipy.signal para evitar hacerlo a ojo. Vamos a pedir aquellos picos que tengan 
# al menos cierta diferencia con su entorno (prominencia), un buen valor para esto es el 8. 
# Podés probar otros valores y observar el resultado.

# >>> print(signal.find_peaks(np.abs(fft_sf), prominence = 8))
# (array([350]), {'prominences': array([11.4554514]), 'left_bases': array([307]), 'right_bases': array([2109])})

# Esta respuesta nos indica que hay un pico con la prominencia solicitada (al menos 8), 
# que tiene un magnitud de 11.45 y que corresponde a la posición 350 del vector.

# >>> freq_sf[350]
# 1.

# La frecuencia relacionada con esa posición es cercana a dos, como ya habíamos
# observado en el gráfico (dos ciclos por día). Podemos distinguir los picos 
# agregando un punto rojo y mirando más de cerca el área de interés:

plt.plot(freq_sf, np.abs(fft_sf))
plt.xlabel("Frecuencia")
plt.ylabel("Potencia (energía)")
plt.xlim(0,4)
plt.ylim(0,20)
# me quedo solo con el último pico
pico_sf = signal.find_peaks(np.abs(fft_sf), prominence = 8)[0][-1]
# es el pico a analizar, el de la onda de mareas
# marco ese pico con un circulito rojo
plt.scatter(freq_sf[pico_sf], np.abs(fft_sf)[pico_sf], facecolor = 'r')
plt.show()

# Estos gráficos permiten interpretar que si descomponemos la curva de alturas 
# en San Fernando como suma de sinusoidales, el sinusoide con frecuencia 1.93 
# tiene una magnitud considerablemente llamativa. No es casualidad que este sea 
# un punto distinguido: se trata de la frecuencia de las mareas lunares.

# Ahora viene la parte un poco más sutíl: el análisis de las fases. 
# Si conocemos la fase de estas componentes en dos puertos distintos, 
# podremos estimar el tiempo que tarda en desplazarse la marea de uno a otro.

# Para calcular la fase (entre -π y π) de dicha componente 
# (la que ubicamos en la posición 350) en el puerto de San Fernando, 
# podemos simplemente usar np.angle() y pasarle el número complejo en cuestión:

# >>> ang_sf = np.angle(fft_sf)[pico_sf]
# >>> print(ang_sf)
# 1.4849

# Obtenemos un valor cercano a pi/2. Recordemos que 2pi corresponde a un 
# desfasaje de un ciclo completo de la curva. Como nuestra curva de estudio 
# tiene una frecuencia diaria ligeramente inferior a 2 (freq_sf[350]~1.93), 
# 2pi corresponde a 24/1.93 horas ~ 12.44 horas. Por lo tanto la fase obtenida 
# con angSF[350] corresponde a un retardo de

# >>> ang_sf * 24 / (2 * np.pi * freq_sf[350])
# 2.93

# Es decir, este sinusoide está desfasado poco menos de 3hs respecto al seno neutro.

# Repitamos velozmente el procedimiento para el puerto de Buenos Aires y analicemos las diferencias.

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

# Si buscamos la constante alrededor de la que oscilan las mareas según el nivel 
# del puerto de Buenos Aires obtenemos:

# >>> np.abs(fft_ba[0])
# 88.21

# Con este resultado es sencillo obtener una estimación para la diferencia de 
# alturas de los ceros de escala entre ambos puertos.

# Pregunta 1: ¿Cuál es la diferencia de altura media entre los puertos obtenida
# de esta forma?

# Pregunta 2: ¿De qué otra forma se puede estimar el valor medio de un puerto? 
# ¿Cuánto da la diferencia con este otro método?

# Por otra parte, si observamos que el espectro de potencia vemos que los 
# picos en ambos puertos son súmamente similares.

# >>> print(signal.find_peaks(np.abs(fft_ba), prominence=8))
# (array([350]), {'prominences': array([12.67228046]), 'left_bases': array([279]), 'right_bases': array([1000])})

# Las mareas de Buenos Aires tiene una componente de máxima amplitud en la 
# frecuencia 1.93 (misma que San Fernando) y con una magnitud de 12.67 
# (bastante similar a la magnitud correspondiente en San Fernando). 
# Resta estudiar la fase de la curva de los datos de df_ba en esta frecuencia 
# para poder determinar con precisión la diferencia de fase entre ambos puertos 
# para ondas de marea. Primero calculamos el ángulo de la componente 
# correspondiente y luego lo convertimos en horas usando el factor ang2h:

# >>> ang_ba = np.angle(fft_ba)[pico_ba]
# >>> print(ang_ba)
# 1.96
# >>> freq = freq_ba[pico_ba]
# >>> ang2h = 24 / (2*np.pi*freq)
# >>> ang_ba * ang2h
# 3.8786004708135566

# Por lo tanto, el retardo de la onda de mareas puede calcularse usando

# (ang_ba - ang_sf) * ang2h