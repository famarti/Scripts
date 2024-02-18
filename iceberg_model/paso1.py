import geopandas as gpd
import os
import urllib.request
import patoolib
import datetime
import pandas as pd
from shapely import geometry
import numpy as np
import subprocess

# Situamos en la carpeta de trabajo
workdir = os.path.join(
    "D:/",
    "Programacion",
    "python",
    "tempanos",
    "NRC_Python_Iceberg_Drift_Model-IIL_size",
    "shapefile_py",
)
os.chdir(workdir)

# Ruta al main.py
maindir = os.path.join(
    "D:/",
    "Programacion",
    "python",
    "tempanos",
    "NRC_Python_Iceberg_Drift_Model-IIL_size",
    "source",
    "system",
    "main.py",
)

# Parametros para la corrida
param = str(
    "D:\\Programacion\\python\\tempanos\\NRC_Python_Iceberg_Drift_Model-IIL_size\\tests\\1-berg-no-ensemble\\BergModel.in"
)

# Exe de python con el environment adecuado.
env_name = "icebergshn"
pythonexe = os.path.join("D:/", "anaconda3", "envs", env_name, "python.exe")

# Establecemos la fecha
fecha_dtime = datetime.datetime.today()
if fecha_dtime.weekday() in [
    0,
    1,
    2,
    3,
]:  # fecha puesta en lunes o viernes, cuando tenemos carta.
    fecha_dtime = fecha_dtime - datetime.timedelta(days=fecha_dtime.weekday())
else:
    fecha_dtime = fecha_dtime - datetime.timedelta(days=fecha_dtime.weekday() - 4)
url_date = "{0}{1}{2}".format(
    str(fecha_dtime.year),
    str(fecha_dtime.month).zfill(2),
    str(fecha_dtime.day).zfill(2),
)

# Hacemos limpieza de archivos shape viejos
for fname in os.listdir(workdir):
    if fname.startswith("ICE"):
        os.remove(os.path.join(workdir, fname))

# Descargamos y descomprimimos el archivo de tempanos
url = "https://www.polarview.aq/images/35_ARGiceberg/current/" + url_date + ".zip"
try:
    urllib.request.urlretrieve(url, "data.zip")
    patoolib.extract_archive("data.zip", outdir=workdir)
    print(f"Se ha descargado y descomprimido la data del día {url_date} exitosamente")
except Exception:
    print("La web Polarview aún no está actualizada")

# Manejamos el archivo geopandas
file_iceshape = str("ICEBERGRISK_" + url_date + ".shp")
file_icelimit = str("ICELIMIT_" + url_date + ".shp")
data_shape = gpd.read_file(file_iceshape)
ice_limit = gpd.read_file(file_icelimit)
ice_limit["bordes"] = ice_limit.boundary
shapefile = data_shape.to_crs(epsg=3031)
shapefile["centroides"] = shapefile.centroid
shape_coord = shapefile["centroides"].to_crs(epsg=4326)
puntos = gpd.GeoDataFrame(shape_coord, geometry="centroides")
icelimit_poli = gpd.GeoDataFrame(ice_limit, crs=4326, geometry="bordes")
pointsinside = gpd.sjoin(puntos, icelimit_poli, how="inner")
pointsoutside = puntos[~puntos.index.isin(pointsinside.index)]

# Coordenadas
coordenadas = [
    (x, y) for x, y in zip(pointsoutside["centroides"].x, pointsoutside["centroides"].y)
]
lats = [y for x, y in zip(pointsoutside["centroides"].x, pointsoutside["centroides"].y)]
lons = [x for x, y in zip(pointsoutside["centroides"].x, pointsoutside["centroides"].y)]

ref = [x for x in data_shape["REFERENCE"]]
np.save("referencias", ref)

# Armado de Berg.in
bergin_file = os.path.join("../", "tests", "1-berg-no-ensemble", "BergModel.in")
berg_file = os.path.join("./", "Bergfull.in")
bergout_file = os.path.join("../", "tests", "1-berg-no-ensemble", "Berg.out")

model_type = "MODEL CIS" + "\n"
runtype = "RUNTYPE ANALYSIS" + "\n"
date_init = "{0}{1}{2}{3}{4}".format(
    str(fecha_dtime.year),
    str(fecha_dtime.month).zfill(2),
    str(fecha_dtime.day).zfill(2),
    "12",
    "0000",
)
date_end = fecha_dtime + datetime.timedelta(days=4)
end_date = "{0}{1}{2}{3}{4}".format(
    str(date_end.year),
    str(date_end.month).zfill(2),
    str(date_end.day).zfill(2),
    "12",
    "0000",
)
start = "START" + " " + date_init + "\n"
end = "TARGET" + " " + end_date + "\n"
melt = "MELT OFF" + "\n"
options = [model_type, runtype, start, end, melt]

iceberg_id = "SNGL"
iceberg_names = [str("A" + str(i)) for i in range(len(coordenadas))]
branch = "1"
latitudes = [round(x, 4) for x in lats]
longitudes = [round(x, 4) for x in lons]
size = "IIL"
shape = "TAB"
mobility = "DFT"
length = str(30743.2)
PercentMelt = "0"
EstimatedSpeed = "0"
Direction = "0"
zeros = ".4f"

open(berg_file, "w").close()
with open(berg_file, "w") as berg:
    for opt in options:
        berg.write(opt)
    for i in range(len(coordenadas)):
        if (
            str(latitudes[i]) == "nan"
            or str(longitudes[i]) == "nan"
            or longitudes[i] >= -5.0
            or str(ref[i]) == "None"
        ):
            pass
        else:
            berg.write(
                str(
                    iceberg_id
                    + " "
                    + iceberg_names[i]
                    + "      "
                    + branch
                    + "   "
                    + date_init
                    + "   "
                    + f"{latitudes[i]:,{zeros}}"
                    + "     "
                    + f"{longitudes[i]:,{zeros}}"
                    + "    "
                    + size
                    + "   "
                    + shape
                    + "  "
                    + mobility
                    + "  "
                    + length
                    + "  "
                    + PercentMelt
                    + "    "
                    + EstimatedSpeed
                    + "    "
                    + Direction
                    + "\n"
                )
            )
f = open(berg_file, "a+")  # para eliminar el último "\n"
f.seek(f.tell() - 2, 0)
f.truncate()
f.close()

open(bergout_file, "w").close()

copyfile(berg_file, bergin_file)
print("Se procede a correr el modelo")
subprocess.call([pythonexe, maindir, param])
