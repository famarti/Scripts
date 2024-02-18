# -*- coding: utf-8 -*-

import os
import netCDF4 as nc
import numpy as np
import xarray as xr
import datetime
from scipy.ndimage import map_coordinates, spline_filter

# Directorio de trabajo
workdir = os.path.join("D:/", "Programacion", "python")

# Configuración para la descarga de datos
env_name = "copernicus"
pythonexe = os.path.join("D:/", "anaconda3", "envs", env_name, "python.exe")

OUTPUT_DIRECTORY = workdir
OUTPUT_FILENAME = "datatest.nc"
USERNAME = "********"  # oculto
PASSWORD = "********"  # oculto

lon_min = -110
lon_max = 10
lat_min = -80
lat_max = -30
date_start = "2021-10-14 12:00:00"
date_end = "2021-10-19 12:00:00"  # 5 días más
depth_min = 0.494
depth_max = 65.8073

# Parámetros para la ejecución de la descarga
run_params = f"-m motuclient --motu https://nrt.cmems-du.eu/motu-web/Motu --service-id GLOBAL_ANALYSIS_FORECAST_PHY_001_024-TDS --product-id global-analysis-forecast-phy-001-024 --longitude-min {lon_min} --longitude-max {lon_max} --latitude-min {lat_min} --latitude-max {lat_max} --date-min {date_start} --date-max {date_end} --depth-min {depth_min} --depth-max {depth_max} --variable thetao --variable uo --variable vo --out-dir {OUTPUT_DIRECTORY} --out-name {OUTPUT_FILENAME} --user {USERNAME} --pwd {PASSWORD}"

# Ejecutar la descarga
os.system(str(pythonexe + " " + run_params))

# Abrir el archivo netCDF descargado
data = nc.Dataset(OUTPUT_FILENAME)

# Preparar las profundidades
depths = []
layer_depth = 10
layers = 20
for i in range(0, int(layers * layer_depth), int(layer_depth)):
    depths.append(float(i))

# Abrir el archivo netCDF con xarray
data_xarray = xr.open_dataset(OUTPUT_FILENAME)
time_dataset = data_xarray.time
u_dataset = data_xarray.uo.chunk({"time": 5})
v_dataset = data_xarray.vo.chunk({"time": 5})
t_dataset = data_xarray.thetao.sel(depth=slice(0)).chunk({"time": 5})
t_dataset = t_dataset.to_dataset().squeeze("depth")

# Renombrar dimensiones para temperatura
t_dataset = t_dataset.to_dataset().squeeze("depth")

# Interpolar la velocidad actual a las profundidades requeridas
curr_speed = xr.merge([u_dataset, v_dataset]).interp(depth=depths)
CurrentSpeedData = xr.merge([u_dataset, v_dataset]).interp(depth=depths)

# Preparar para otro intento de descarga
OUTPUT_DIRECTORY = workdir
OUTPUT_FILENAME = "datatest.nc"
USERNAME = "********"  # oculto
PASSWORD = "********"  # oculto

# Preparar las profundidades para el segundo intento
depths = []
layer_depth = 10
layers = 20
for i in range(0, int(layers * layer_depth), int(layer_depth)):
    depths.append(float(i))

# Abrir el archivo netCDF con xarray para el segundo intento
data_xarray = xr.open_dataset(OUTPUT_FILENAME, decode_times=False)
time_dataset = data_xarray.time
u_dataset = data_xarray.uo.chunk({"time": 5})
v_dataset = data_xarray.vo.chunk({"time": 5})
t_dataset = data_xarray.thetao.sel(
    depth=slice(data_xarray.thetao.depth.valid_min)
).chunk({"time": 5})
TemperatureData = t_dataset.to_dataset().squeeze("depth")
CurrentSpeedData = xr.merge([u_dataset, v_dataset]).interp(depth=depths)

# Renombrar variables
TemperatureData = TemperatureData.rename({"thetao": "water_surface_temperature"})
CurrentSpeedData = CurrentSpeedData.rename({"uo": "current_u", "vo": "current_v"})

# Configurar el tiempo
dataset_start_time = datetime.datetime.strptime(
    time_dataset.time.units[12:], "%Y-%m-%d %H:%M:%S"
)

# Convertir las fechas a formato float
new_dates = []
for i in range(0, len(CurrentSpeedData.time.values), 1):
    date = dataset_start_time + datetime.timedelta(
        hours=int(CurrentSpeedData.time.values[i])
    )

    CurrentSpeedData.time.values[i] = (
        float(str(date.year) + str(date.month).zfill(2) + str(date.day).zfill(2))
        + (date.hour * 3600 + date.minute * 60 + date.second) / 86400
    )
    TemperatureData.time.values[i] = (
        float(str(date.year) + str(date.month).zfill(2) + str(date.day).zfill(2))
        + (date.hour * 3600 + date.minute * 60 + date.second) / 86400
    )

# Corregir el tiempo de las fechas
workdir = "D:\Programacion\python"
file = "datatest.nc"
data_xarray = xr.open_dataset(workdir + "/" + file, decode_times=False)
time_dataset = data_xarray.time

new_dates = []
for i in range(0, len(CurrentSpeedData.time.values), 1):
    date = dataset_start_time + datetime.timedelta(
        hours=int(CurrentSpeedData.time.values[i])
    )

    date_float = (
        float(str(date.year) + str(date.month).zfill(2) + str(date.day).zfill(2))
        + (date.hour * 3600 + date.minute * 60 + date.second) / 86400
    )
    new_dates.append(date_float)
CurrentSpeedData.time.values = np.array(new_dates)
TemperatureData.time.values = np.array(new_dates)
