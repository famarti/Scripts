# -*- coding: utf-8 -*-

# Importing libraries
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import os

os.environ["PROJ_LIB"] = (
    "D:\\anaconda3\\Library\\share"  # Setting environment variable for Basemap
)
from mpl_toolkits.basemap import Basemap
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
import matplotlib.colors
import pickle

# Setting up working directory
workpath = os.path.join("D:/", "Programacion", "python", "hielo", "ultimos")
os.chdir(workpath)

# Loading data
filename = "hielo2021360hs"
df = pd.read_csv(filename, header=None, sep=r"\s{1,}")  # Reading data
df_latlon = pd.read_csv(
    "latlon2021360hs", header=None, sep=r"\s{1,}"
)  # Reading latitudes and longitudes

# Standardizing data
X_std = StandardScaler().fit_transform(df)
m, n = X_std.shape
R_matrix = np.dot(X_std.T, X_std) / (m - 1)
Pcor1, Dcor1, Qcor1 = np.linalg.svd(R_matrix)
D_matrix = np.diag(Dcor1 ** (-1 / 2))
Z_matrix = np.dot(X_std, Pcor1.dot(D_matrix))
D_matrix_2 = np.diag(Dcor1 ** (1 / 2))
F_matrix = np.dot(Pcor1, D_matrix_2)
V_expcor1 = (Dcor1 / np.sum(Dcor1)) * 100


# Function for Varimax rotation
def _varimax(loadings, normalize=True, max_iter=500, tol=1e-5):
    """
    Perform varimax (orthogonal) rotation, with optional
    Kaiser normalization.

    Parameters
    ----------
    loadings : array-like
        The loading matrix

    Returns
    -------
    loadings : numpy array, shape (n_features, n_factors)
        The loadings matrix
    rotation_mtx : numpy array, shape (n_factors, n_factors)
        The rotation matrix
    """
    X = loadings.copy()
    n_rows, n_cols = X.shape
    if n_cols < 2:
        return X

    if normalize:
        normalized_mtx = np.apply_along_axis(
            lambda x: np.sqrt(np.sum(x**2)), 1, X.copy()
        )
        X = (X.T / normalized_mtx).T

    rotation_mtx = np.eye(n_cols)
    d = 0
    for _ in range(max_iter):
        old_d = d
        basis = np.dot(X, rotation_mtx)
        transformed = np.dot(
            X.T,
            basis**3
            - (1.0 / n_rows) * np.dot(basis, np.diag(np.diag(np.dot(basis.T, basis)))),
        )
        U, S, V = np.linalg.svd(transformed)
        rotation_mtx = np.dot(U, V)
        d = np.sum(S)
        if old_d != 0 and d / old_d < 1 + tol:
            break

    X = np.dot(X, rotation_mtx)

    if normalize:
        X = X.T * normalized_mtx
    else:
        X = X.T

    loadings = X.T.copy()
    return loadings, rotation_mtx


# Applying Varimax rotation
F_rot, T_matrix = _varimax(F_matrix[:, 0:8])
load = np.concatenate((F_rot, F_matrix[:, 8:]), axis=1)
scores = Z_matrix.copy()

# Saving the rotated loadings
df_rot_load = pd.DataFrame(F_rot)
df_rot_load.to_csv("loads_rotados.csv")

# Creating column names for the dataframe
names_cols = ["lat", "lon"]
for i in range(1, load.shape[1] + 1):
    name_loadings = "CP_%d" % i
    names_cols.append(name_loadings)

full_prueba = pd.DataFrame(columns=names_cols)

df_scores = pd.DataFrame(scores)
df_load = pd.DataFrame(load)

concatenacion = pd.concat([df_latlon, df_scores], axis=1)
full_prueba = concatenacion.set_axis(names_cols, axis=1, inplace=False)

# Defining the spatial extent of the data
lllon = full_prueba["lon"].min()
lllat = full_prueba["lat"].min()
urlon = full_prueba["lon"].max()
urlat = full_prueba["lat"].max()

# Creating a grid
numcols, numrows = 1000, 1000
xi = np.linspace(lllon, urlon, numcols)
yi = np.linspace(lllat, urlat, numrows)
xi, yi = np.meshgrid(xi, yi)

# Defining color palette
n = 40
x = 0.5
cmap = plt.cm.seismic
lower = cmap(np.linspace(0, x, n))
white = np.ones((5, 4))
upper = cmap(np.linspace(1 - x, 1, n))
colors = np.vstack((lower, white, upper))
tmap = matplotlib.colors.LinearSegmentedColormap.from_list("map_white", colors)

# Plotting loadings vs time
dti = pd.Series(pd.period_range("1/1/1979", freq="M", periods=515))
for v in range(8):
    fig = plt.figure(figsize=(10, 8))
    load_v = df_load.iloc[:, v].values
    plt.plot_date(dti, load_v, ls="-", marker="")

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

# Listing phases and months
listado = df_load.iloc[:, 0:8]
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
    data[str(k)] = (data.loc[:, v.values].sum(axis=1)) / (len(v.values))

las_fechas = pd.Series(pd.period_range("1/1/1979", freq="M", periods=515))
open("patrones.txt", "w").close()
txt = open("patrones.txt", "w")
for r in group.keys():
    txt.write(r)
    txt.write("\n")
    for s in group[r]:
        txt.write(str(las_fechas[s]))
        txt.write("\n")
txt.close()


def para_sandra(name):
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


# For each CP, generate spatial patterns
comp_prom = [k for k, v in group.items()]
for j in comp_prom:
    z = data.loc[:, j].values
    x, y, z = full_prueba["lon"].values, full_prueba["lat"].values, z
    zi = griddata((x, y), z, (xi, yi), method="linear")
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
    titulo = para_sandra(str(j))
    plt.title(titulo, fontdict={"fontsize": 20})
    plt.savefig(
        titulo + ".png",
        format="png",
        dpi=1000,
        bbox_inches="tight",
        pad_inches=0.5,
        edgecolor="r",
    )


# %% Guardar
def save_obj(obj, name):
    with open(name + ".pkl", "wb+") as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


save_obj(group, "patrones")
