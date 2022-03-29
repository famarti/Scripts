# -*- coding: utf-8 -*-

# Este programa toma los datos de anomalias de hielo y realiza ACP varimax rotando los 
# 8 primeros loadings. Graficar es opcional. Luego se guarda en un archivo esos Loadings rotados

# importo librerias
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import os
os.environ["PROJ_LIB"] = "D:\\anaconda3\\Library\\share" # fixr D:\anaconda3\Library\share #ahi debería estar carpeta proj
from mpl_toolkits.basemap import Basemap
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
import matplotlib.colors
#%%
workpath = os.path.join('D:/', 'Programacion', 'python', 'hielo', 'ultimos')
os.chdir(workpath)
filename = 'hielo2021360hs'
df = pd.read_csv(filename, header = None, sep = r'\s{1,}')   # leo datos
df_latlon = pd.read_csv('latlon2021360hs', header = None, sep = r'\s{1,}')# leo lats lons
#%% Cuentas estadisticas
X_std = StandardScaler().fit_transform(df) # estandarizo matriz datos

m, n = X_std.shape # m filas, n columnas

R_matrix = np.dot(X_std.T, X_std)/ (m - 1) # matriz correlaciones

Pcor1 , Dcor1 , Qcor1 = np.linalg.svd(R_matrix) # svd

D_matrix =(np.diag(Dcor1**(-1/2)))

Z_matrix = np.linalg.multi_dot([X_std, Pcor1, D_matrix]) # matriz scores

D_matrix_2 = (np.diag(Dcor1**(1/2))) # matriz diagonal

F_matrix = np.dot(Pcor1, D_matrix_2) # matriz loadings

V_expcor1 = (Dcor1/np.sum(Dcor1))*100 #var explicada por cada CP
#%% Funcion varimax
def _varimax(loadings, normalize = True, max_iter = 500, tol = 1e-5):
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

    # normalize the loadings matrix
    # using sqrt of the sum of squares (Kaiser)
    if normalize:
        normalized_mtx = np.apply_along_axis(lambda x: np.sqrt(np.sum(x**2)), 1, X.copy())
        X = (X.T / normalized_mtx).T

    # initialize the rotation matrix
    # to N x N identity matrix
    rotation_mtx = np.eye(n_cols)

    d = 0
    for _ in range(max_iter):

        old_d = d

        # take inner product of loading matrix
        # and rotation matrix
        basis = np.dot(X, rotation_mtx)

        # transform data for singular value decomposition
        transformed = np.dot(X.T, basis**3 - (1.0 / n_rows) *
                             np.dot(basis, np.diag(np.diag(np.dot(basis.T, basis)))))

        # perform SVD on
        # the transformed matrix
        U, S, V = np.linalg.svd(transformed)

        # take inner product of U and V, and sum of S
        rotation_mtx = np.dot(U, V)
        d = np.sum(S)

        # check convergence
        if old_d != 0 and d / old_d < 1 + tol:
            break

    # take inner product of loading matrix
    # and rotation matrix
    X = np.dot(X, rotation_mtx)

    # de-normalize the data
    if normalize:
        X = X.T * normalized_mtx
    else:
        X = X.T

    # convert loadings matrix to data frame
    loadings = X.T.copy()
    return loadings, rotation_mtx
#%% Operaciones matriciales adicionales

F_rot, T_matrix = _varimax(F_matrix[:,0:8])
load = np.concatenate((F_rot, F_matrix[:,8:]), axis=1)    # por comodidad, la voy a hacer df
scores = Z_matrix.copy() # no son las comp rotadas. la necesito definir solo por su estructura. no la uso

# Guardo los 8 loadings
df_rot_load = pd.DataFrame(F_rot)
df_rot_load.to_csv('loads_rotados.csv')
#%%
names_cols = ['lat', 'lon']              # creo nombres para columnas
for i in range(1,load.shape[1]+1):
    name_loadings = 'CP_%d'%i
    names_cols.append(name_loadings)

full_prueba = pd.DataFrame(columns = names_cols)  # creo DataFrame vacío con nombres de cols

df_scores = pd.DataFrame(scores)     # transformo a DataFrame la matriz de scores

df_load = pd.DataFrame(load) # transformo a DataFrame la matriz de loadings

concatenacion = pd.concat([df_latlon, df_scores],axis  = 1)   # Junto las lats y lons con la matriz de scores

full_prueba = concatenacion.set_axis(names_cols, axis = 1, inplace = False) # enchufamos a la matriz vacía eso

# Definimos la extensión espacial de nuestros datos
lllon = full_prueba['lon'].min()
lllat = full_prueba['lat'].min()
urlon = full_prueba['lon'].max()
urlat = full_prueba['lat'].max()

# Definimos la grilla, resolución 1000*1000
numcols, numrows = 1000, 1000
xi = np.linspace(lllon, urlon, numcols)
yi = np.linspace(lllat, urlat, numrows)
xi, yi = np.meshgrid(xi, yi)

# Definimos paleta de colores
n=40
x = 0.5
cmap = plt.cm.seismic
lower = cmap(np.linspace(0, x, n))
white = np.ones((5,4))
upper = cmap(np.linspace(1-x, 1, n))
colors = np.vstack((lower, white, upper))
tmap = matplotlib.colors.LinearSegmentedColormap.from_list('map_white', colors)
#%%
# Armo plot linea de los loadings vs tiempo

# Fechas de Inicio y fin: enero 1979 - marzo 2021
dti = pd.Series(pd.period_range("1/1/1979", freq="M", periods=515))

# plot
for v in range(8):
    fig = plt.figure(figsize = (10,8))
    load_v = df_load.iloc[:,v].values
    plt.plot_date(dti, load_v, ls = "-", marker = "")
    
    # scatter de mayores valores
    mayores_idx = ((df_load.iloc[:,v].abs()).nlargest(3)).index
    max_dates = [dti[ind] for ind in mayores_idx]
    max_values = [load_v[ind] for ind in mayores_idx]
    str_dates = [str(lab) for lab in max_dates]
    plt.scatter(max_dates, max_values, marker = "*", color = 'r', label = str_dates)
    plt.ylim(-1,1)
    plt.title('Loading'+' '+'CP_'+' '+str(v+1))
    plt.legend(loc = 'upper center')
    plt.savefig('loadings CP_'+str(v+1)+'.png')
    plt.show()
#%% listado de fases y meses

listado = (df_load.iloc[:,0:8]) # antes con .set_index(dti)

group = {}
for i in range(1,9):
    group["grupo_{0}_pos".format(i)] = listado[(listado[i-1] >= 0.3) & (listado[i-1] >= 0)].index
    group["grupo_{0}_neg".format(i)] = listado[(listado[i-1] <= -0.3) & (listado[i-1] <= 0)].index

df_latlon.rename(columns = {0:'lat', 1:'lon'}, inplace = True)
data = pd.concat([df_latlon, df], axis = 1)

for k,v in group.items():
    data[str(k)] = (data.loc[:, v.values].sum(axis=1))/(len(v.values)) # composiciones promedio
    
def para_sandra(name):
    if name == 'grupo_8_pos':
        return 'L8-'
    elif name == 'grupo_8_neg':
        return 'L8+'
    elif name == 'grupo_7_pos':
        return 'L7-'
    elif name == 'grupo_7_neg':
        return 'L7+'
    elif name == 'grupo_4_pos':
        return 'L6-'
    elif name == 'grupo_4_neg':
        return 'L6+'
    elif name == 'grupo_6_pos':
        return 'L5-'
    elif name == 'grupo_6_neg':
        return 'L5+'
    elif name == 'grupo_5_neg':
        return 'L4-'
    elif name == 'grupo_5_pos':
        return 'L4+'
    elif name == 'grupo_3_neg':
        return 'L3-'
    elif name == 'grupo_3_pos':
        return 'L3+'
    elif name == 'grupo_1_neg':
        return 'L2-'
    elif name == 'grupo_1_pos':
        return 'L2+'
    elif name == 'grupo_2_pos':
        return 'L1-'
    elif name == 'grupo_2_neg':
        return 'L1+'
    else:
        pass

#%% Para cada CP hacemos lo siguiente:
comp_prom = [k for k,v in group.items()]
for j in comp_prom:
    z = data.loc[:,j].values
    
    #interpolamos
    x, y, z = full_prueba['lon'].values, full_prueba['lat'].values, z
    zi = griddata((x, y), z, (xi,yi), method='linear')
    
    #plot
    fig, ax = plt.subplots(figsize=(10,10))
    m2 = Basemap(projection='spstere',boundinglat=-50,lon_0=90,resolution='i')
    levels = np.linspace(-70,70,41)
    CS2 = m2.contourf(xi,yi,zi,levels = levels,cmap = tmap, latlon=True)
    #conts = m2.contour(xi, yi, zi, levels = [-20.0,-10.0, 10.0, 20.0], colors=('k',),linestyles=('-',),linewidths=(2,))
    #labs = m2.clabel(conts, fmt = '%2.1d', colors = 'k', fontsize=14)
    cbar = m2.colorbar(CS2,location='right', pad="12%")
    m2.drawparallels(np.arange(-90.,99.,60.),labels=[False,False,False,False])
    m2.drawmeridians(np.arange(-180.,180.,90.),labels=[False,False,False,False])
    m2.drawcoastlines()
    m2.fillcontinents(color='grey')
    #m2.drawmapboundary(fill_color='black')
    titulo = para_sandra(str(j))
    plt.title(titulo, fontdict={'fontsize':20})
    plt.savefig(titulo+'.png',format='png', dpi=1000, bbox_inches = 'tight', pad_inches = 0.5, edgecolor='r')
    #plt.show()
#%%