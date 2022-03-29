# -*- coding: utf-8 -*-
# seleccion_modelos.py
import numpy as np
import pandas as pd
from sklearn import linear_model
import matplotlib.pyplot as plt

def ajuste_lineal_simple(x,y):
    a = sum(((x - x.mean())*(y-y.mean()))) / sum(((x-x.mean())**2))
    b = y.mean() - a*x.mean()
    return a, b

def AIC(k, ecm, num_params):
    '''Calcula el AIC de una regresión lineal múltiple de 'num_params' parámetros, ajustada sobre una muestra de 'k' elementos, y que da lugar a un error cuadrático medio 'ecm'.'''
    aic = k * np.log(ecm) + 2 * num_params
    return aic

np.random.seed(3141) # semilla para fijar la aleatoriedad
N=50
indep_vars = np.random.uniform(size = N, low = 0, high = 10)
r = np.random.normal(size = N, loc = 0.0, scale = 8.0) # residuos
dep_vars = 2 + 3*indep_vars + 2*indep_vars**2 + r # relación cuadrática

x = indep_vars
y = dep_vars
xc = x**2

# reordeno los datos
datosxy = pd.DataFrame({'x': x, 'y': y, 'xc':xc})
X = np.concatenate((x.reshape(-1,1),xc.reshape(-1,1)),axis=1)

# inicializo los 3 modelos
lineal_model = linear_model.LinearRegression() # modelo 1
cuad_model = linear_model.LinearRegression() # modelo 2
multi_model = linear_model.LinearRegression() # modelo 3

# fiteo los 3 modelos definidos a los datos segun se deseaba
lineal_model.fit(datosxy[['x']], datosxy['y'])
cuad_model.fit(datosxy[['xc']], datosxy['y'])
multi_model.fit(X, datosxy['y'])

# defino la grilla x
grilla_x = np.linspace(start = 0, stop = 10, num = 1000)
grilla_2x = np.concatenate([grilla_x,grilla_x])

# coeficientes modelo 1
a1 = lineal_model.coef_
b1 = lineal_model.intercept_
# coeficientes modelo 2
a2 = cuad_model.coef_
b2 = cuad_model.intercept_
# coefiecientes modelo 3
a3 = multi_model.coef_
b3 = multi_model.intercept_

# valores estimados 3 modelos
y1hat = a1*x + b1
y2hat = a2*xc + b2
y3hat = a3[0]*x + a3[1]*xc + b3
# con grilla_x
grilla_y1 = lineal_model.predict(grilla_x.reshape(-1,1))
grilla_y2 = a2*(grilla_x**2) + b2
grilla_y3 = a3[0]*grilla_x + a3[1]*(grilla_x**2) + b3

datosxy.plot.scatter('x','y')
plt.plot(grilla_x, grilla_y1, c = 'green', label = 'Lineal')
plt.plot(grilla_x, grilla_y2, c = 'red', label = 'Cuadratico')
plt.plot(grilla_x, grilla_y3, c = 'cyan', label = 'Multiple')
plt.legend()
plt.show()

# Errores
res1 = y - y1hat
ecm1 = (res1**2).mean()
res2 = y - y2hat
ecm2 = (res2**2).mean()
res3 = y - y3hat
ecm3 = (res3**2).mean()
print("ECM modelo 1:", ecm1,'\n', "ECM modelo 2:",ecm2,'\n',"ECM modelo 3:",ecm3)

def fit_model(x, y, n):
    listita = []
    for i in range(n):
        v1 = x**(i+1)
        v2 = v1.reshape(-1,1)
        listita.append(v2)
    X = np.concatenate([i for i in listita], axis = 1)
    model = linear_model.LinearRegression()
    model.fit(X, y)
    a = model.coef_
    b = model.intercept_
    return a, b

def poli_grade(coef, intercept, x, n):
    y = intercept + np.zeros(len(x))
    if n>0:
        for i in range(n):
            y += coef[i]*(x)**(i+1)
        return y
    else:
        return y

aic_list = []
for i in range(1,9):
    a, b = fit_model(x, datosxy['y'], i)
    y_hat = poli_grade(a, b, x, i)
    residuo = y - y_hat
    ECM = (residuo**2).mean()
    aic = AIC(len(x), ECM, i+1)
    aic_list.append(aic)
    print('-'*25)
    print('Grado del polinomio:',str(i),'\n','Cantidad de parametros:',str(i+1),'\n','ECM:',str(round(ECM,3)),'\n','AIC:',str(round(aic,3)))

print(f'El modelo que minimiza el AIC es el de grado {np.argmin(aic_list)+1}')
