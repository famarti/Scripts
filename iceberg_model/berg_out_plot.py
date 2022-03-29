# imports
import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
import geopandas as gpd
from shapely.geometry import Point
import datetime
#%% Carpeta de trabajo
workdir = os.path.join('D:/', 'Programacion', 'python','tempanos', 'NRC_Python_Iceberg_Drift_Model-IIL_size', 'shapefile_py')
os.chdir(workdir)
path_to_bergout = os.path.join('../', 'tests', '1-berg-no-ensemble', 'Berg.out')
#%% Manejo archivos con pandas
bergout = pd.read_csv(path_to_bergout, header=None, sep = r'\s{1,}', engine='python')
ref = np.load('referencias.npy', allow_pickle=True) #archivo referencias.npy traido de la ejecucion de shapefile.py
iceberg_names = [str('A'+str(i)) for i in range(0,len(ref))]  # 3220 nro de centroides = len(ref)
#%%###################################Solo para pruebas########################################
backup_dir = os.path.join('D:/', 'Programacion', 'python', 'tempanos', 'backup_varios')
os.chdir(backup_dir)
bergout = pd.read_csv('Berg.out', header=None, sep= r'\s{1,}', engine='python')
ref = np.load('referencias.npy', allow_pickle=True)
iceberg_names = [str('A'+str(i)) for i in range(0,len(ref))]  # 3220 nro de centroides = len(ref
################################################################################################
#%% Anexamos la data de cantidad de icebergs al Berg.out con el archivo 'referencias.npy'
bergout['berg_ref'] = 1 # inicializo la columna con las ref de cant de icebergs
dic_ref = {k:v for k,v in zip(iceberg_names,ref)}
for i in range(len(bergout)):
    bergout['berg_ref'][i] = dic_ref[str(bergout.iloc[i,1])]
#%% Referencias para los colores
def referenciar(data, refs, colors):
    '''
    Esta funcion sirve para colorizar las
    referencias de icebergs para posteriormente
    tener una columna con los colores para plotear
    Parametros:
    - data: (Df)Dataframe al cual vamos a agregarle una
    columna con referencias de colores ('r', 'g' o 'y')
    - refs: (str)columna de data que tiene las referencias del
    shape de la carta de tempanos. Solo puede ser 'FEW'
    'ISOLATED' o 'MANY'
    - colors: (str)nombre que desearias que tuviese la columna
    de data que va a tener las referencias de colores.
    '''
    data[colors] = 1
    for j in range(len(data)):
        if data[refs][j] == 'ISOLATED':
            data[colors][j] = 'g'
        elif data[refs][j] == 'FEW':
            data[colors][j] = 'y'
        elif data[refs][j] == 'MANY':
            data[colors][j] = 'r'
        else:
            pass
referenciar(bergout, 'berg_ref', 'color_ref')
#%% Nos quedamos con los puntos que si figuran en el Berg.out (que fueron modelados)
outs = {}
for name in iceberg_names:
    if name in bergout[1].values:
        outs[name] = bergout[bergout[1] == name] 

# Lectura de archivo shape para utilizar la grilla de la carta
fecha_dtime = datetime.datetime.today()
if fecha_dtime.weekday() in [0,1,2,3]: # fecha puesta en lunes o viernes, cuando tenemos carta.
    fecha_dtime = fecha_dtime - datetime.timedelta(days=fecha_dtime.weekday())
else:
    fecha_dtime = fecha_dtime - datetime.timedelta(days=fecha_dtime.weekday() - 4)
url_date = "{0}{1}{2}".format(str(fecha_dtime.year), str(fecha_dtime.month).zfill(2), str(fecha_dtime.day ).zfill(2))

file_iceshape = str("ICEBERGRISK_"+url_date+".shp")
data_shape = gpd.read_file(file_iceshape)
carta_temp = data_shape.geometry.copy()
geo_grilla = gpd.GeoDataFrame(carta_temp)
#%% Graficado post 24hs
# Un poco de Data Wrangling
col_names = ['Id', 'Name', 'Branch', 'Start_Date', 'Latitude', 'Longitude', 'Size', 'Shape', 'Mobility', 'Length', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'Ref', 'Col']
ronda_24 = pd.DataFrame([outs.get(i_names).iloc[25,:] for i_names in outs.keys()])
new_names = {u:v for u,v in zip(ronda_24.columns.values.tolist(), col_names)}
ronda_24 = ronda_24.rename(columns = new_names, inplace = False)
geo_24 = gpd.GeoDataFrame(ronda_24, geometry=gpd.points_from_xy(ronda_24.Longitude, ronda_24.Latitude))
df_24 = geo_24.reset_index(drop=True, inplace=False)
referenciar(df_24, 'Ref', 'Col')

ronda_48 = pd.DataFrame([outs.get(i_names).iloc[49,:] for i_names in outs.keys()])
new_names = {u:v for u,v in zip(ronda_48.columns.values.tolist(), col_names)}
ronda_48 = ronda_48.rename(columns = new_names, inplace = False)
geo_48 = gpd.GeoDataFrame(ronda_48, geometry=gpd.points_from_xy(ronda_48.Longitude, ronda_48.Latitude))
df_48 = geo_48.reset_index(drop=True, inplace=False)
referenciar(df_48, 'Ref', 'Col')

ronda_72 = pd.DataFrame([outs.get(i_names).iloc[73,:] for i_names in outs.keys()])
new_names = {u:v for u,v in zip(ronda_72.columns.values.tolist(), col_names)}
ronda_72 = ronda_72.rename(columns = new_names, inplace = False)
geo_72 = gpd.GeoDataFrame(ronda_72, geometry=gpd.points_from_xy(ronda_72.Longitude, ronda_72.Latitude))
df_72 = geo_72.reset_index(drop=True, inplace=False)
referenciar(df_72, 'Ref', 'Col')
#%%
# Defino clase Tempano
class Tempano(object):
    def __init__(self, name, latitude, longitude, reference, color):
        self.name = name
        self.latitude= latitude
        self.longitude = longitude
        self.reference = reference
        self.color = color

    def posicion(self):
        return Point(self.longitude, self.latitude)

    def cercanos(self, other):
        if abs(self.latitude - other.latitude) < 0.1 and abs(self.longitude - other.longitude) < 0.1:
            return True
        else:
            return False

    def __repr__(self):
        return f'Tempano({self.name})'

# Inicializo la clase
ice_24 = [Tempano(a,b,c,d,e) for a, b, c, d, e in zip(
    df_24['Name'], df_24['geometry'].y, df_24['geometry'].x, df_24['Ref'], df_24['Col'])]

# Arreglo de la grilla
geo_grilla['colores'] = 1
for j in range(len(geo_grilla)):
    if geo_grilla['geometry'][j] is None:
        geo_grilla['colores'][j] = 'w'
    else:
        pass

def redef_color(grid_color, temp_color):
    '''
    Funcion para establecer colores en casos de 
    convergencias de témpanos en determinada celda (grid)
    Parámetros:
    - grid_color: color que tenia la celda previamente
    - temp_color: color asignado al grupo de témpanos que llega
    a esa celda
    Ámbos colores deben ser únicamente 'r' 'g' 'y' o 'w'
    '''

    grilla = str(grid_color)
    tempano = str(temp_color)
    if grilla == 'w':
        return tempano
    else:
        if grilla == 'g' and tempano == 'g':
            return 'y'
        elif grilla == 'g' and tempano == 'y':
            return 'y'
        elif grilla == 'g' and tempano == 'r':
            return 'r'
        elif grilla == 'y' and tempano == 'g':
            return 'y'
        elif grilla == 'y' and tempano == 'y':
            return 'r'
        elif grilla == 'y' and tempano == 'r':
            return 'r'
        else:
            return 'r'

grd_i = 0
while grd_i<len(geo_grilla):
    if geo_grilla['geometry'][grd_i] is None:
        pass
    else:
        for tpano in ice_24:
            if tpano.posicion().within(geo_grilla['geometry'][grd_i]):
                if geo_grilla['colores'][grd_i] is 1:
                    geo_grilla['colores'][grd_i] = tpano.color
                    ice_24.pop(ice_24.index(tpano))
                else:
                    geo_grilla['colores'][grd_i] = redef_color(geo_grilla['colores'][grd_i], tpano.color)
                    ice_24.pop(ice_24.index(tpano))
            else:
                continue
    grd_i += 1

ice24_dic = {
    'Id':[_.name for _ in ice_24],
    'geometry':[_.posicion() for _ in ice_24],
    'colores':[_.color for _ in ice_24],
    'referencia':[_.reference for _ in ice_24],
    'celda':[1 for _ in range(len(ice_24))]
}
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
ax = world[world.continent == 'Antarctica'].plot(color='white', edgecolor='black', figsize=(15,10))
ax.set_xlim(-100,0)
ice24_grid = gpd.GeoDataFrame(ice24_dic, crs="EPSG:4326")
ice24_grid.plot(ax=ax, marker='s')
plt.show()
#%%