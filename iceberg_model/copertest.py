# -*- coding: utf-8 -*-
"""
Created on Thu Oct 14 11:26:53 2021

@author: Facundo
"""
#%%
import os
import netCDF4 as nc
import numpy as np
import xarray as xr
import datetime
from scipy.ndimage import map_coordinates, spline_filter
#workdir = os.path.join('D:/', 'Programacion', 'python', 'tempanos', 'pruebas', 'copernicus')
workdir = os.path.join('D:/', 'Programacion', 'python')
os.chdir(workdir)

#%% Test descarga datos
env_name = 'copernicus'
pythonexe = os.path.join('D:/', 'anaconda3', 'envs', env_name, 'python.exe')

OUTPUT_DIRECTORY = workdir
OUTPUT_FILENAME = "datatest.nc"
USERNAME = "fmartinez"
PASSWORD = "QB52Zxe?aU*TTpD"

lon_min = -110
lon_max = 10
lat_min = -80
lat_max = -30
date_start = "2021-10-14 12:00:00"
date_end = "2021-10-19 12:00:00"  # 5 dias mas
depth_min = 0.494
depth_max = 65.8073
#%% Ejecutamos la descarga
run_params = f'-m motuclient --motu https://nrt.cmems-du.eu/motu-web/Motu --service-id GLOBAL_ANALYSIS_FORECAST_PHY_001_024-TDS --product-id global-analysis-forecast-phy-001-024 --longitude-min {lon_min} --longitude-max {lon_max} --latitude-min {lat_min} --latitude-max {lat_max} --date-min {date_start} --date-max {date_end} --depth-min {depth_min} --depth-max {depth_max} --variable thetao --variable uo --variable vo --out-dir {OUTPUT_DIRECTORY} --out-name {OUTPUT_FILENAME} --user {USERNAME} --pwd {PASSWORD}'

os.system(str(pythonexe + " " + run_params))
#%%
data = nc.Dataset(OUTPUT_FILENAME)
#   QUEDO VIEJO. VER MAS ABAJO
depths = []
layer_depth = 10
layers = 20
for i in range(0, int(layers * layer_depth), int(layer_depth)):
    depths.append(float(i))

data_xarray = xr.open_dataset(OUTPUT_FILENAME)
time_dataset = data_xarray.time
u_dataset = data_xarray.uo.chunk({'time':5})
v_dataset = data_xarray.vo.chunk({'time':5})
t_dataset = data_xarray.thetao.sel(depth=slice(0)).chunk({'time':5})

# remover depth dimension para data temperatura
t_dataset = t_dataset.to_dataset().squeeze("depth")


# probar sin chunk (es necesario?) chunkean en time=5 en hycomm
data_xarray = xr.open_dataset(OUTPUT_FILENAME)
time_dataset = data_xarray.time
u_dataset = data_xarray.uo
v_dataset = data_xarray.vo
t_dataset = data_xarray.thetao.sel(depth=slice(data_xarray.thetao.depth.valid_min))
#t_dataset = data_xarray.thetao
t_dataset = t_dataset.to_dataset().squeeze("depth")
curr_speed = xr.merge([u_dataset, v_dataset]).interp(depth=depths)
#antes tuve problema xq 0 no era una profundidad existente en el dataset de temperatura. puse
# la de más arriba q es 0.4940... el valid_min


CurrentSpeedData = xr.merge([u_dataset, v_dataset]).interp(depth=depths)
#%% LO SIGUIENTE, COMO REFERENCIA
 # loads sets into memory. loading sets individually before doing anything computationally intensive
# has a lower chance of opendap failure
# try:
#     # interpolates depth indexes to match user input
#     self.CurrentSpeedData = xr.merge([u_dataset, v_dataset]).interp(depth=depths)
# except Exception as e:
#     log.exception(e)
#     print(
#         "Could not download data from the server, this is most likely either due to the server being "
#         "under maintenance or is being updated.")
#     print(e)
#%% sigue...

# remover depth dimension para data temperatura (te queda solo la q te importa)
t_dataset = t_dataset.to_dataset().squeeze("depth")

############### PRIMER INTENTO############################
env_name = 'copernicus'
pythonexe = os.path.join('D:/', 'anaconda3', 'envs', env_name, 'python.exe')

OUTPUT_DIRECTORY = workdir
OUTPUT_FILENAME = "datatest.nc"
USERNAME = "fmartinez"
PASSWORD = "QB52Zxe?aU*TTpD"

lon_min = -110
lon_max = 10
lat_min = -80
lat_max = -30
date_start = "2021-10-14 12:00:00"
date_end = "2021-10-19 12:00:00"  # 5 dias mas
depth_min = 0.494
depth_max = 65.8073
#%% Ejecutamos la descarga
run_params = f'-m motuclient --motu https://nrt.cmems-du.eu/motu-web/Motu --service-id GLOBAL_ANALYSIS_FORECAST_PHY_001_024-TDS --product-id global-analysis-forecast-phy-001-024 --longitude-min {lon_min} --longitude-max {lon_max} --latitude-min {lat_min} --latitude-max {lat_max} --date-min {date_start} --date-max {date_end} --depth-min {depth_min} --depth-max {depth_max} --variable thetao --variable uo --variable vo --out-dir {OUTPUT_DIRECTORY} --out-name {OUTPUT_FILENAME} --user {USERNAME} --pwd {PASSWORD}'

os.system(str(pythonexe + " " + run_params))
#%%
#                                       LO DE ACA SIRVE PARA PRUEBAS. !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
OUTPUT_DIRECTORY = workdir
OUTPUT_FILENAME = "datatest.nc"
USERNAME = "fmartinez"
PASSWORD = "QB52Zxe?aU*TTpD"

depths = []
layer_depth = 10
layers = 20
for i in range(0, int(layers * layer_depth), int(layer_depth)):
    depths.append(float(i))

data_xarray = xr.open_dataset(OUTPUT_FILENAME,decode_times=False) # ACAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
time_dataset = data_xarray.time
u_dataset = data_xarray.uo.chunk({'time':5})
v_dataset = data_xarray.vo.chunk({'time':5})
t_dataset = data_xarray.thetao.sel(depth=slice(data_xarray.thetao.depth.valid_min)).chunk({'time':5})
TemperatureData = t_dataset.to_dataset().squeeze("depth")
CurrentSpeedData = xr.merge([u_dataset, v_dataset]).interp(depth=depths)





#CHECK UN VALUE DE TEMP
# t_dataset.thetao[0, -50, -50].values = array(16.188574, dtype=float32)

#SIGUIENTE PASO, CAMBIAR NOMBRE "thetao" a "water_surface_temperature"
# TAMBIÉN "uo" por "current_u" y "vo" por "current_v"
TemperatureData = TemperatureData.rename(
                ({"thetao": "water_surface_temperature"}))

CurrentSpeedData = CurrentSpeedData.rename(
    ({"uo": "current_u", "vo": "current_v"}))

dataset_start_time = datetime.datetime.strptime(time_dataset.time.units[12:], "%Y-%m-%d %H:%M:%S")
# converts datetime values to float representation of it
new_dates = []
for i in range(0, len(CurrentSpeedData.time.values), 1):
    date = dataset_start_time + datetime.timedelta(
        hours=int(CurrentSpeedData.time.values[i]))

    CurrentSpeedData.time.values[i] = float(
        str(date.year) + str(date.month).zfill(2)
        + str(date.day).zfill(2)) \
                                           + (
                                                       date.hour * 3600 + date.minute * 60 + date.second) / 86400
    TemperatureData.time.values[i] = float(
        str(date.year) + str(date.month).zfill(2)
        + str(date.day).zfill(2)) \
                                          + (
                                                      date.hour * 3600 + date.minute * 60 + date.second) / 86400

# LAS LAT Y LONG YA ESTAN BIEN. FALTA CORREGIR EL TIEMPO
# DE DATETIME A SU EQUIVALENTE EN FLOAT. (IGUAL Q' PARA HYCOMM)
workdir = 'D:\Programacion\python'
file = 'datatest.nc'
data_xarray = xr.open_dataset(workdir + "/" + file,decode_times=False)
time_dataset = data_xarray.time


#ARREGLO LO DE LAS DATES
new_dates = []
for i in range(0, len(CurrentSpeedData.time.values), 1):
    date = dataset_start_time + datetime.timedelta(
        hours=int(CurrentSpeedData.time.values[i]))

    date_float = float(
        str(date.year) + str(date.month).zfill(2)
        + str(date.day).zfill(2)) \
                                           + (
                                                       date.hour * 3600 + date.minute * 60 + date.second) / 86400
    new_dates.append(date_float)
CurrentSpeedData.time.values = np.array(new_dates)
TemperatureData.time.values = np.array(new_dates)
