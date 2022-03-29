# -*- coding: utf-8 -*-
# Ultimate version de cosas en tesis
#%% Procesado de datos
import os
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import numpy as np
path_to_csvs = os.path.join('D:/','Programacion','python','tesis','csv')

os.chdir(path_to_csvs)
#%%
df = pd.read_csv("neepython_bis_final.csv", sep = ';')

dates = pd.date_range(start='12/21/2012',freq='30min',periods=5184)
# fechas = []
# for date in dates:
#     cut = date.strftime('%Y-%m-%d')
#     fechas.append(cut)
    
df_ok = df.set_index(dates)

df_ok['GPP(ton/ha)'] = df_ok['GPP']*(44.01*1800*0.00000001)
df_ok['Reco(ton/ha)'] = df_ok['Reco']*(44.01*1800*0.00000001)

# df_ok['Fechas'] = fechas

#datos como df_ok pero diario, acumulados:
datos = df_ok.resample('24H').sum()
#Pachorra de renombrar columnas mode on:
datos['Calor Sensible(W/m2)'] = datos['H']
datos['Calor Latente(W/m2)'] = datos['LE']
#Fechas relevantes
inicio_emer_v3 = '2012-12-21'
R1V8 = '2013-01-25'
R3V12 = '2013-02-05'
R5V15 = '2013-02-22'
R7 = '2013-04-06'
Fin = '2013-04-07'

datos['Fase']= 1
datos['Fase'][inicio_emer_v3:R1V8] = '1- S,E,V3'
datos['Fase'][R1V8:R3V12] = '2- R1V8'
datos['Fase'][R3V12:R5V15] = '3- R3V12'
datos['Fase'][R5V15:R7] = '4- R5V15'
datos['Fase'][R7:Fin] = '5- R7'

#%% Ploteos
Vars = ['NEE(ton/ha)', 'GPP(ton/ha)', 'Reco(ton/ha)', 'Calor Sensible(W/m2)','Calor Latente(W/m2)']
labels = [r'$NEE\ (ton\ de\ C/ha\ día)$', r'$GPP\ (ton\ de\ C/ha\ día)$', r'$Reco\ (ton\ de\ C/ha\ día)$', r'$Calor\ Sensible\ (W/m^2\ día)$',r'$Calor\ Latente\ (W/m^2\ día)$']
Fechas = pd.date_range(start='12/21/2012', freq='D', periods=108)
colores = ['r','g','y','b','m']
lab = 0
for var in Vars:
    grouping = datos.groupby('Fase')[var]
    plt.figure(figsize=(15,10))
    for i, (title,group) in enumerate(grouping):
        plt.bar(group.index, group, color = colores[i], label=title)
    plt.legend(fontsize='large')
    plt.tick_params(direction='in',length=10,width=2)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.gcf().autofmt_xdate()
    plt.grid(True,axis='y',color='k',linestyle='--', linewidth=0.5)
    plt.axhline(0, color='black',linewidth=1)
    plt.ylabel(labels[lab],fontsize=18)
    lab += 1
    if var == 'Calor Sensible(W/m2)':
        plt.savefig('sensible.png', format='png', dpi = 1000, bbox_inches = 'tight', pad_inches = 0.5)
    else:
        plt.savefig(str(var[:3])+'.png', format = 'png', dpi = 1000, bbox_inches = 'tight', pad_inches = 0.5)
#%%Radiación
zeros = np.zeros(1306)

fechas_null = pd.DataFrame({'rad':zeros,'par':zeros}, dtype = float)

df_rad = pd.read_csv("rad_neta.csv")

df_rad_par = pd.read_csv("rad_par.csv")

df_rad_casi_full = pd.concat([df_rad,df_rad_par],axis=1)

rad_full = pd.concat([fechas_null,df_rad_casi_full], axis = 0)
dates = pd.date_range(start='12/21/2012 00:00',end= '04/08/2013 09:00' ,freq='15min')

df_rad_ok = rad_full.set_index(dates)

#acum diarios
datos_rad = df_rad_ok.resample('24H').sum()
datos_rad['par']['2012-12-21':'2013-01-02'] = np.nan
datos_rad['rad']['2012-12-21':'2013-01-02'] = np.nan
#elimino días pocos datos
datos_rad['par']['2013-01-03'] = np.nan
datos_rad['rad']['2013-01-03'] = np.nan

datos_rad['par']['2013-01-15'] = np.nan
datos_rad['rad']['2013-01-15'] = np.nan

datos_rad['par']['2013-01-16'] = np.nan
datos_rad['rad']['2013-01-16'] = np.nan

datos_rad['par']['2013-04-08'] = np.nan
datos_rad['rad']['2013-04-08'] = np.nan

datos_rad = datos_rad.set_index(pd.date_range(start = '12/21/2012', end = '04/08/2013', freq ='D').strftime('%Y-%m-%d'))

#plots
fig = plt.figure(figsize=(15,10))
ax = fig.add_subplot(111)
ax2 = ax.twinx()
width = 0.4
#datos_rad.iloc[:,0].plot(kind = 'bar', color = 'red', ax = ax, width = width, position = 1, label = 'Neta')
#datos_rad.iloc[:,1].plot(kind = 'bar', color = 'green', ax = ax2, width = width, position = 0, label = 'Par')
#datos_rad.iloc[:,0].plot(kind = 'line', color = 'red')
#datos_rad.iloc[:,1].plot(kind = 'line', color = 'green')
ax.plot(datos_rad.index, datos_rad.iloc[:,0], color = 'red',linestyle = '--', linewidth = 2.5)
ax2.plot(datos_rad.index, datos_rad.iloc[:,1], color = 'green' )
ax.set_ylabel(r'$Radiación\ Neta\ (J/m^2 día)$', color = 'red', fontsize = 17)
ax2.set_ylabel(r'$Radiación\ Par\ (J/m^2 día)$', color = 'green', fontsize = 17)
ax.tick_params(axis = 'y', direction='inout',length=10,width=2, labelsize = 15, labelcolor = 'r', color = 'r' )
ax2.tick_params(axis = 'y', direction='inout',length=10,width=2, labelsize = 15, labelcolor = 'g', color = 'g' )
ax.tick_params(axis = 'x',direction='inout',length=10,width=2,labelsize = 15)
ax.set_xticks(np.arange(11,108,15))
plt.grid(True,axis='y',color='k',linestyle='--', linewidth=0.5)
#plt.axhline(0, color='black',linewidth=1)
plt.gcf().autofmt_xdate()
#ax.legend(fontsize='xx-large')
#ax2.legend(fontsize='xx-large',loc = (0.913,0.9))
plt.savefig('radiacion.png', format = 'png', dpi = 1000, bbox_inches = 'tight', pad_inches = 0.5)
#%% Acumulados por fase.
inicio_emer = '2012-12-21'
V3 = '2013-01-07'
R1V8 = '2013-01-25'
R3V12 = '2013-02-05'
R5V15 = '2013-02-22'
R7 = '2013-04-06'
Fin = '2013-04-07'

datos['Fase']= 1
datos['Fase'][inicio_emer:V3] = '1- S,E'
datos['Fase'][V3:R1V8] = '2- V3'
datos['Fase'][R1V8:R3V12] = '3- R1V8'
datos['Fase'][R3V12:R5V15] = '4- R3V12'
datos['Fase'][R5V15:R7] = '5- R5V15'
datos['Fase'][R7:Fin] = '6- R7'

feno = datos['Fase'].unique().tolist()
carbo = ['NEE(ton/ha)', 'GPP(ton/ha)', 'Reco(ton/ha)']
acu = [datos.groupby('Fase')[c].sum().tolist() for c in carbo]
feno_labels = ["S & E", "V3","R1V8","R3V12","R5V15","R7"]


# X = np.arange(6)
# fig = plt.figure(figsize=(20,15))
# ax = fig.add_axes([0,0,1,1])
# ax.bar(X, acu[0], color = 'b', width = 0.25, label = 'NEE')
# ax.bar(X + 0.25, acu[1], color = 'g', width = 0.25, label = 'GPP')
# ax.bar(X + 0.50, acu[2], color = 'r', width = 0.25, label = 'Reco')
# ax.tick_params(axis = 'y', direction='in',length=15,width=2, labelsize = 30)
# #plt.xticks(feno_labels,fontsize=30)
# #ax.set_yticks((np.arange(-8, 1.5, step=0.5)),fontsize=30)
# ax.set_ylabel(r'$(ton/ha\ fase)$', fontsize = 30)
# plt.grid(True,axis='y',color='k',linestyle='--', linewidth=0.5)
# ax.legend(fontsize=30)
# plt.axhline(0, color='black',linewidth=1)
# plt.show()


X = np.arange(6)
plt.figure(figsize=(15,10))
plt.bar(X, acu[0], color = 'g', width = 0.25, label = 'NEE')
plt.bar(X + 0.25, acu[1], color = 'b', width = 0.25, label = 'GPP')
plt.bar(X + 0.50, acu[2], color = 'r', width = 0.25, label = 'Reco')
plt.xticks(X + 0.25, feno_labels,fontsize=15)
plt.yticks((np.arange(-4, 8, step=2)),fontsize=15)
plt.ylabel(r'$(ton\ de\ C/ha\ fase)$', fontsize = 17)
plt.grid(True,axis='y',color='k',linestyle='--', linewidth=0.5)
plt.legend(fontsize = 'large')
plt.axhline(0, color='black',linewidth=1)
plt.tick_params(direction='inout',length=10,width=2)
plt.savefig('acu_fases.png', format = 'png', dpi = 1000, bbox_inches = 'tight', pad_inches = 0.5)

#%% Usando datos y datos_rad

# Estimo cada 10 días QE/Rn y QH/RN

# Sumatoria cada 10 días de QE y QH
Qx_10 = datos.resample('10D').sum()

for r, rad in enumerate(df_rad_ok['rad']):
    if (rad == 0) or (rad < -1000):
        df_rad_ok['rad'][r] = np.nan

rad_10 = df_rad_ok.resample('10D').sum()

flux_vs_rad = pd.DataFrame({'QH/RN':[(x/y)*100 for x, y in zip(Qx_10['Calor Sensible(W/m2)'], rad_10['rad']) if y != 0],
                            'QE/RN':[(x/y)*100 for x, y in zip(Qx_10['Calor Latente(W/m2)'], rad_10['rad']) if y != 0]})

f_v_r_labels = ['3-10 Enero', '11-20 Enero', '21-31 Enero', '1-10 Febrero', '11-20 Febrero', '21-28 Febrero',
                '1-10 Marzo', '11-20 Marzo', '21-31 Marzo', '1-7 Abril']

width = 0.35
Y = np.arange(10)
fig, ax = plt.subplots(figsize=(15,10))
ax.bar(Y - width/2, flux_vs_rad['QE/RN'], color = 'g', width = width, label = r'$Q_E/RN\ $ (%)')
ax.bar(Y + width/2, flux_vs_rad['QH/RN'], color = 'b', width = width, label = r'$Q_H/RN\ $ (%)')
ax.set_xticks(Y)
ax.set_xticklabels(f_v_r_labels, fontsize = 20, rotation = 25)
ax.set_yticks((np.arange(0, 60, step = 10)))
ax.tick_params(axis = 'x',length = 10,width = 2, labelsize = 17)
ax.tick_params(axis = 'y',length = 10,width = 2, labelsize = 17)
plt.grid(True,axis = 'y',color = 'k',linestyle = '--', linewidth = 0.5)
ax.legend(fontsize = 'xx-large')
plt.axhline(0, color = 'black',linewidth = 1)
fig.tight_layout()
plt.savefig('flujos_vs_rad.png', format = 'png', dpi = 1000, bbox_inches = 'tight', pad_inches = 0.5)




























