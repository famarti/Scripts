# Librerías
import geopandas as gpd
import os
from patoolib.util import Encoding2Mime
import urllib.request
import patoolib
import datetime
import pandas as pd
from shapely import geometry
import rtree
from shutil import copyfile
import numpy as np
import subprocess
#%% Situamos en carpeta
workdir = os.path.join('D:/', 'Programacion', 'python', 'tempanos', 'NRC_Python_Iceberg_Drift_Model-IIL_size', 'shapefile_py')
os.chdir(workdir)
# Ruta al main.py
maindir = os.path.join('D:/', 'Programacion', 'python', 'tempanos', 'NRC_Python_Iceberg_Drift_Model-IIL_size', 'source', 'system', 'main.py')
# Parametros para la corrida
param = str('D:\\Programacion\\python\\tempanos\\NRC_Python_Iceberg_Drift_Model-IIL_size\\tests\\1-berg-no-ensemble\\BergModel.in')
# Exe de python con el environment adecuado.
env_name = 'icebergshn' # OJO! O LLAMAR ASÍ AL ENV DE CONDA, O MODIFICAR ESTA VARIABLE
#env_name = 'icetesting'
pythonexe = os.path.join('D:/', 'anaconda3', 'envs', env_name, 'python.exe')
#%% Establezco fecha
fecha_dtime = datetime.datetime.today()
if fecha_dtime.weekday() in [0,1,2,3]: # fecha puesta en lunes o viernes, cuando tenemos carta.
    fecha_dtime = fecha_dtime - datetime.timedelta(days=fecha_dtime.weekday())
else:
    fecha_dtime = fecha_dtime - datetime.timedelta(days=fecha_dtime.weekday() - 4)
url_date = "{0}{1}{2}".format(str(fecha_dtime.year), str(fecha_dtime.month).zfill(2), str(fecha_dtime.day ).zfill(2))
#%% Hacemos limpieza de archivos shape viejos
for fname in os.listdir(workdir):
    if fname.startswith("ICE"):
        os.remove(os.path.join(workdir, fname))
#%% Descargo archivo tempanos y descomprimo
url = 'https://www.polarview.aq/images/35_ARGiceberg/current/' + url_date + '.zip'
try:
    urllib.request.urlretrieve(url, "data.zip")
    patoolib.extract_archive("data.zip", outdir = workdir)
    print(f'Se ha descargado y unzippeado la data del dia {url_date} exitosamente')
except Exception:
    print('La web Polarview aun no esta actualizada')
    
#%% manejo archivo geopandas
file_iceshape = str("ICEBERGRISK_"+url_date+".shp")
file_icelimit = str("ICELIMIT_"+url_date+".shp")
data_shape = gpd.read_file(file_iceshape)
ice_limit = gpd.read_file(file_icelimit)
ice_limit['bordes'] = ice_limit.boundary
shapefile = data_shape.to_crs(epsg=3031) # para calcular centroides, situamos World Geodetic System en antartida
shapefile['centroides'] = shapefile.centroid
shape_coord = shapefile['centroides'].to_crs(epsg=4326) # volvemos a coordenadas normales
puntos = gpd.GeoDataFrame(shape_coord, geometry='centroides')
icelimit_poli = gpd.GeoDataFrame(ice_limit, crs=4326, geometry='bordes')
pointsinside = gpd.sjoin(puntos,icelimit_poli,how="inner")
pointsoutside = puntos[~puntos.index.isin(pointsinside.index)]

coordenadas = [(x,y) for x,y in zip(pointsoutside['centroides'].x , pointsoutside['centroides'].y)]
lats = [y for x,y in zip(pointsoutside['centroides'].x , pointsoutside['centroides'].y)]
lons = [x for x,y in zip(pointsoutside['centroides'].x , pointsoutside['centroides'].y)]

ref = [x for x in data_shape['REFERENCE']]
np.save('referencias', ref)
#%% Armado de Berg.in
# Berg.in path
bergin_file = os.path.join('../', 'tests', '1-berg-no-ensemble', 'Berg.in')
# Berg_full.in path
berg_file = os.path.join('./', 'Bergfull.in')
# Berg.out path
bergout_file = os.path.join('../', 'tests', '1-berg-no-ensemble', 'Berg.out')
# Run options
model_type = 'MODEL CIS'+'\n'
runtype = 'RUNTYPE ANALYSIS'+'\n'
date_init ="{0}{1}{2}{3}{4}".format(str(fecha_dtime.year), str(fecha_dtime.month).zfill(2), str(fecha_dtime.day ).zfill(2), '12', '0000')
date_end = fecha_dtime + datetime.timedelta(days=4)
end_date = "{0}{1}{2}{3}{4}".format(str(date_end.year), str(date_end.month).zfill(2), str(date_end.day ).zfill(2), '12', '0000')
start = str('START'+" "+ date_init+'\n')
end =  str('TARGET'+" "+ end_date+'\n')
melt = 'MELT OFF'+'\n'
options = [model_type, runtype, start, end, melt]
# iceberg config
iceberg_id = 'SNGL'
iceberg_names = [str('A'+str(i)) for i in range(len(coordenadas))] 
branch = '1'
latitudes = [round(x,4) for x in lats]
longitudes = [round(x,4) for x in lons]
size = 'IIL' # o en su defecto LRG
shape = 'TAB'
mobility = 'DFT'
length = str(30743.2) # ya veremos esto
PercentMelt = '0'
EstimatedSpeed = '0'
Direction = '0'
zeros = '.4f'
# Bergfull.in viejo limpieza
open(berg_file, 'w').close()
# Bergfull.in writing
with open(berg_file, 'w') as berg:
    for opt in options:
        berg.write(opt)
    for i in range(len(coordenadas)):
        if str(latitudes[i]) == 'nan' or str(longitudes[i]) == 'nan' or longitudes[i] >= -5.0 or str(ref[i]) == 'None': # primeras dos condiciones son las mask, la otra es para zonas de agua
            pass
        else:
            berg.write(str(iceberg_id+" "+iceberg_names[i]+"      "+branch+"   "+date_init+"   "+f"{latitudes[i]:,{zeros}}"+"     "+f"{longitudes[i]:,{zeros}}"+"    "+size+"   "+shape+"  "+mobility+"  "+length+"  "+PercentMelt+"    "+EstimatedSpeed+"    "+Direction+'\n'))
f = open(berg_file, 'a+') # para elimiinar el ultimo "\n"
f.seek(f.tell() - 2, 0)
f.truncate()
f.close()
#%% Limpiamos contenidos viejos del Berg.out
open(bergout_file, 'w').close()

#%% Copiamos los Berg_'s a la carpeta 1-berg-no-ensamble como "Berg.in" y corremos el modelo (las veces necesarias)

copyfile(berg_file, bergin_file)
print('Se procede a correr el modelo')
#os.system(str(pythonexe + " " + maindir + " " + param))
subprocess.call([pythonexe, maindir, param])