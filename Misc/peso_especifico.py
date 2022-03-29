# peso_especifico.py
import pandas as pd
from sklearn import linear_model
import numpy as np
import matplotlib.pyplot as plt
import requests
import io

enlace = 'https://raw.githubusercontent.com/python-unsam/UNSAM_2020c2_Python/master/Notas/11_Recursion/longitudes_y_pesos.csv'
r = requests.get(enlace).content
data_lyp = pd.read_csv(io.StringIO(r.decode('utf-8')))

# (peso ~ longitud)

ajuste_lineal = linear_model.LinearRegression(fit_intercept=False)
ajuste_lineal.fit(data_lyp[['longitud']], data_lyp.peso)

grilla_x = np.linspace(start = 0, stop = 30, num = 1000)
grilla_y = ajuste_lineal.predict(grilla_x.reshape(-1,1))

data_lyp.plot.scatter('longitud','peso')
plt.title('ajuste lineal usando sklearn')
plt.plot(grilla_x, grilla_y, c = 'green')
plt.show()

a = ajuste_lineal.coef_
print(f'El peso especifico es de {round(a[0],3)}')

errores = data_lyp.peso - (ajuste_lineal.predict(data_lyp[['longitud']]))
print(errores)
print("ECM:", (errores**2).mean()) # error cuadrático medio