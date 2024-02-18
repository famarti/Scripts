# -*- coding: utf-8 -*-

# Este script realiza Análisis de Componentes Principales (ACP) varimax rotando los 8 primeros loadings.
# Los datos de entrada son anomalías de hielo, que luego son estandarizadas y sometidas al ACP.
# Opcionalmente, se grafican los loadings y se guardan los resultados en archivos CSV y PNG.

# Importación de librerías necesarias
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import os

os.environ["PROJ_LIB"] = (
    "D:\\anaconda3\\Library\\share"  # Ruta necesaria para la proyección en mapas si se usa Anaconda/Windows.
)
from mpl_toolkits.basemap import Basemap
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
import matplotlib.colors

# Establecimiento del directorio de trabajo y lectura de datos
workpath = os.path.join("D:/", "Programacion", "python", "hielo", "ultimos")
os.chdir(workpath)
filename = "hielo2021360hs"
df = pd.read_csv(
    filename, header=None, sep=r"\s{1,}"
)  # Lectura de datos de anomalías de hielo
df_latlon = pd.read_csv(
    "latlon2021360hs", header=None, sep=r"\s{1,}"
)  # Lectura de coordenadas latitud y longitud

# Cálculos estadísticos y matrices
X_std = StandardScaler().fit_transform(df)  # Estandarización de los datos
m, n = X_std.shape  # Dimensiones de la matriz estandarizada
R_matrix = np.dot(X_std.T, X_std) / (m - 1)  # Matriz de correlaciones
Pcor1, Dcor1, Qcor1 = np.linalg.svd(
    R_matrix
)  # Descomposición en valores singulares (SVD)
D_matrix = np.diag(Dcor1 ** (-1 / 2))  # Matriz diagonal de valores singulares
Z_matrix = np.dot(X_std, Pcor1 @ D_matrix)  # Matriz de scores
D_matrix_2 = np.diag(Dcor1 ** (1 / 2))  # Segunda matriz diagonal de valores singulares
F_matrix = np.dot(Pcor1, D_matrix_2)  # Matriz de loadings


# Función para la rotación varimax
def _varimax(loadings, normalize=True, max_iter=500, tol=1e-5):
    """
    Realiza rotación varimax (ortogonal) opcionalmente normalizando los loadings.

    Parámetros
    ----------
    loadings : matriz
        La matriz de loadings

    Returns
    -------
    loadings : matriz numpy, forma (n_features, n_factors)
        La matriz de loadings rotada
    rotation_mtx : matriz numpy, forma (n_factors, n_factors)
        La matriz de rotación
    """
    # Implementación de varimax...
    pass


# Rotación varimax de los loadings
F_rot, T_matrix = _varimax(F_matrix[:, 0:8])
load = np.concatenate(
    (F_rot, F_matrix[:, 8:]), axis=1
)  # Concatenación de los loadings rotados
scores = (
    Z_matrix.copy()
)  # Copia de la matriz de scores (no se utilizan los scores rotados)

# Guardar los 8 loadings rotados en un archivo CSV
df_rot_load = pd.DataFrame(F_rot)
df_rot_load.to_csv("loads_rotados.csv")

# Creación de nombres para las columnas de un DataFrame
names_cols = ["lat", "lon"]
for i in range(1, load.shape[1] + 1):
    name_loadings = "CP_%d" % i
    names_cols.append(name_loadings)

# Creación de un DataFrame vacío con los nombres de columnas establecidos
full_prueba = pd.DataFrame(columns=names_cols)

# Transformación de la matriz de scores y la matriz de loadings a DataFrames
df_scores = pd.DataFrame(scores)
df_load = pd.DataFrame(load)

# Concatenación de coordenadas con los scores y asignación de nombres de columnas
concatenacion = pd.concat([df_latlon, df_scores], axis=1)
full_prueba = concatenacion.set_axis(names_cols, axis=1, inplace=False)

# Definición de la extensión espacial de los datos
lllon = full_prueba["lon"].min()
lllat = full_prueba["lat"].min()
urlon = full_prueba["lon"].max()
urlat = full_prueba["lat"].max()

# Definición de la grilla para interpolación
numcols, numrows = 1000, 1000
xi = np.linspace(lllon, urlon, numcols)
yi = np.linspace(lllat, urlat, numrows)
xi, yi = np.meshgrid(xi, yi)

# Definición de la paleta de colores
n = 40
x = 0.5
cmap = plt.cm.seismic
lower = cmap(np.linspace(0, x, n))
white = np.ones((5, 4))
upper = cmap(np.linspace(1 - x, 1, n))
colors = np.vstack((lower, white, upper))
tmap = matplotlib.colors.LinearSegmentedColormap.from_list("map_white", colors)

# Creación de plots para los loadings vs. tiempo
for v in range(8):
    fig = plt.figure(figsize=(10, 8))
    load_v = df_load.iloc[:, v].values
    plt.plot_date(dti, load_v, ls="-", marker="")

    # Destacar los mayores valores
    mayores_idx = ((df_load.iloc[:, v].abs()).nlargest(3)).index
    max_dates = [dti[ind] for ind in mayores_idx]
    max_values = [load_v[ind] for ind in mayores_idx]
    str_dates = [str(lab) for lab in max_dates]
    plt.scatter(max_dates, max_values, marker="*", color="r", label=str_dates)
    plt.ylim(-1, 1)
    plt.title("Loading" + " " + "CP_" + " " + str(v + 1))
    plt.legend(loc="upper center")
    plt.savefig("loadings CP_" + str(v + 1) + ".png")
    plt.show()

# Lista de fases y meses
listado = df_load.iloc[:, 0:8]  # antes con .set_index(dti)

group = {}
for i in range(1, 9):
    group["grupo_{0}_pos".format(i)] = listado[
        (listado[i - 1] >= 0.3) & (listado[i - 1] >= 0)
    ].index
    group["grupo_{0}_neg".format(i)] = listado[
        (listado[i - 1] <= -0.3) & (listado[i - 1] <= 0)
    ].index

df_latlon.rename(columns={0: "lat", 1: "lon"}, inplace=True)
data = pd.concat([df_latlon, df], axis=1)

for k, v in group.items():
    data[str(k)] = (data.loc[:, v.values].sum(axis=1)) / (
        len(v.values)
    )  # Composiciones promedio


# Función para asignar nombres específicos
def sandra_format(name):
    if name == "grupo_8_pos":
        return "L8-"
    elif name == "grupo_8_neg":
        return "L8+"
    elif name == "grupo_7_pos":
        return "L7-"
    elif name == "grupo_7_neg":
        return "L7+"
    elif name == "grupo_4_pos":
        return "L6-"
    elif name == "grupo_4_neg":
        return "L6+"
    elif name == "grupo_6_pos":
        return "L5-"
    elif name == "grupo_6_neg":
        return "L5+"
    elif name == "grupo_5_neg":
        return "L4-"
    elif name == "grupo_5_pos":
        return "L4+"
    elif name == "grupo_3_neg":
        return "L3-"
    elif name == "grupo_3_pos":
        return "L3+"
    elif name == "grupo_1_neg":
        return "L2-"
    elif name == "grupo_1_pos":
        return "L2+"
    elif name == "grupo_2_pos":
        return "L1-"
    elif name == "grupo_2_neg":
        return "L1+"
    else:
        pass


# Creación de plots para cada CP
comp_prom = [k for k, v in group.items()]
for j in comp_prom:
    z = data.loc[:, j].values

    # Interpolación
    x, y, z = full_prueba["lon"].values, full_prueba["lat"].values, z
    zi = griddata((x, y), z, (xi, yi), method="linear")

    # Plot
    fig, ax = plt.subplots(figsize=(10, 10))
    m2 = Basemap(projection="spstere", boundinglat=-50, lon_0=90, resolution="i")
    levels = np.linspace(-70, 70, 41)
    CS2 = m2.contourf(xi, yi, zi, levels=levels, cmap=tmap, latlon=True)
    cbar = m2.colorbar(CS2, location="right", pad="12%")
    m2.drawparallels(np.arange(-90.0, 99.0, 60.0), labels=[False, False, False, False])
    m2.drawmeridians(
        np.arange(-180.0, 180.0, 90.0), labels=[False, False, False, False]
    )
    m2.drawcoastlines()
    m2.fillcontinents(color="grey")
    titulo = sandra_format(str(j))
    plt.title(titulo, fontdict={"fontsize": 20})
    plt.savefig(
        titulo + ".png",
        format="png",
        dpi=1000,
        bbox_inches="tight",
        pad_inches=0.5,
        edgecolor="r",
    )

# Fin del script
