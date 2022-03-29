# -*- coding: utf-8 -*-

# PROGRAMA QUE LEE TODOS LOS ARCHIVOS Y LOS CONCATENA EN 1 SOLO ARCHIVO	CON LAT LONG
# y genera el archivo de anomalías para correr las componentes principales o redes neuronales
#%%
import pandas as pd
import datetime
import os
import numpy as np
#%%
#workpath = os.path.join('D:/', 'Programacion', 'python', 'hielo')
#workpath = 'D:\Programacion\python\hielo'
#os.chdir(workpath)
#%%
def nro_to_mes(n_month):
    if n_month == '01':
        return 'Enero'
    elif n_month == '02':
        return 'Febrero'
    elif n_month == '03':
        return 'Marzo'
    elif n_month == '04':
        return 'Abril'
    elif n_month == '05':
        return 'Mayo'
    elif n_month == '06':
        return 'Junio'
    elif n_month == '07':
        return 'Julio'
    elif n_month == '08':
        return 'Agosto'
    elif n_month == '09':
        return 'Septiembre'
    elif n_month == '10':
        return 'Octubre'
    elif n_month == '11':
        return 'Noviembre'
    elif n_month == '12':
        return 'Diciembre'
    else:
        exit("El mes no es válido, revise el input.")
    
def dif_meses(año1, año2):
    return (año1.year - año2.year)*12 + año1.month - año2.month
#%% Constants
nrows = 104912
start_date = datetime.date(1979,1,1)
#%%
print('#############################################################')
print('                     Programa N2021todo.py')
print('#############################################################')
print(' ')
print('Este programa DEBE estar ubicado un nivel anterior que las siguientes carpetas:')
print(' ')
print('/datoshielo (la cual tiene los archivos de lat y lon pss25lats.txt y pss25lons.txt)')
print('/N2021folder que tiene los fAAAAMM que son del IDL')
print(' ')
workpath_input = input('Ingrese la ruta de trabajo donde está el programa N2021todo.py, sin comillas, EJEMPLO: \nD:\Programacion\python\hielo ')
workpath = str(workpath_input)
os.chdir(workpath)
auto = input('¿Modo automático, si o no?  ')
if auto not in ['si','Si','sI','SI']:
    mes = int(input("Ingrese el número de meses que se tienen:  "))
    #anio = int(input("Ingrese el número de años que se tienen:  "))
    ncols = mes
    #anio_actual = 1979 + anio
else:
    mes_actual = str(datetime.datetime.today().month).zfill(2)
    anio_actual = str(datetime.datetime.today().year)
    print(f'Comenzando el programa N2021todo.py para el mes de {nro_to_mes(mes_actual)} del año {anio_actual}')
    
    ncols = dif_meses(datetime.datetime.today(), start_date)
#%%
f_lats = pd.read_csv('datoshielo/pss25lats.txt', header=None)
f_lons = pd.read_csv('datoshielo/pss25lons.txt', header=None)

df_data = pd.DataFrame({'lat':f_lats.values.reshape(104912,), 
                        'lon':f_lons.values.reshape(104912,)}, 
                       index = [i for i in range(104912)])

# Armo matriz lat lon y todos los datos crudos del IDL

for index, i in enumerate(os.listdir(workpath+'/N2021folder/')):
    if index > ncols:
        break
    else:
        temp_file = pd.read_csv('N2021folder/'+str(i), header=None, names=[str(i)])
        df_data = pd.concat([df_data,temp_file], axis=1)
    
# Removemos los ceros, los -6666, -7777 y -8888

df_data = df_data.replace([0, -6666.0, -7777.0, -8888.0], np.nan)

# Separamos matriz con lat lon, y matriz con el resto

df_latlon = df_data.iloc[:,:2]
df_onlydata = df_data.iloc[:, 2:]

# Creo matriz media 1991.2020

df_mean = pd.DataFrame() # Será esta
meses_media = ['f'+str(anio)+str(mes).zfill(2) for anio in range(1991,2021) for mes in range(1,13)]
df_meses_media = df_onlydata.loc[:, meses_media]

for u in range(1,13):
    df_temp_mean = (df_meses_media[[col for col in df_meses_media.columns if col.endswith(str(u).zfill(2))]].sum(axis=1))/30
    col_name = str(u).zfill(2)
    ok_temp_mean = pd.DataFrame({col_name:df_temp_mean})
    df_mean = pd.concat([df_mean, ok_temp_mean], axis=1)

# Calculo de los desvios de la media

df_desvios = pd.DataFrame()

m = 0
n = 0
while m < df_onlydata.shape[1]:
    df_std_temp = df_onlydata.iloc[:,m] - df_mean.iloc[:,n]
    df_desvios = pd.concat([df_desvios,df_std_temp], axis=1)
    m += 1
    n += 1
    if n > 11:
        n = 0

df_desvios.to_csv('hielonuevo360hs',sep=',', index=False, header=False)
df_latlon.to_csv('latlonnuevo360hs', sep=',', index=False, header=False)

print('Listo! Se generaron los archivos "hielonuevo360hs" y "latlonnuevo360hs".')
print('Terminando programa N2021todo.py')
