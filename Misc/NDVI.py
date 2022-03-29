# -*- coding: utf-8 -*-

#%%
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import axes_grid1
from matplotlib.colors import ListedColormap
import matplotlib.patches as mpatches
import os
import sys
#%%
class Bandas:
    def __init__(self):
        '''
        Inicializo variables de bandas

        '''
        self.banda_1 = np.load('LC08_L1TP_225084_20180213_20180222_01_T1_sr_band1_clip.npy')
        self.banda_2 = np.load('LC08_L1TP_225084_20180213_20180222_01_T1_sr_band2_clip.npy')
        self.banda_3 = np.load('LC08_L1TP_225084_20180213_20180222_01_T1_sr_band3_clip.npy')
        self.banda_4 = np.load('LC08_L1TP_225084_20180213_20180222_01_T1_sr_band4_clip.npy')
        self.banda_5 = np.load('LC08_L1TP_225084_20180213_20180222_01_T1_sr_band5_clip.npy')
        self.banda_6 = np.load('LC08_L1TP_225084_20180213_20180222_01_T1_sr_band6_clip.npy')
        self.banda_7 = np.load('LC08_L1TP_225084_20180213_20180222_01_T1_sr_band7_clip.npy')
        
    def NDVI(self):
        '''
        Estimación del NDVI        
        '''
        bNIR_bR = self.banda_5 + self.banda_4
        bNIR_bR[bNIR_bR == 0] = 0.001
        ndvi = (self.banda_5 - self.banda_4) / (bNIR_bR)
        return ndvi

#%%   
def add_colorbar(im,aspect=20,pad_fraction=0.5):
    divider=axes_grid1.make_axes_locatable(im.axes)
    width= axes_grid1.axes_size.AxesY(im.axes, aspect=1./aspect)
    pad=axes_grid1.axes_size.Fraction(pad_fraction, width)
    current_ax=plt.gca()
    cax=divider.append_axes("right", size=width, pad=pad)
    plt.sca(current_ax)
    return im.axes.figure.colorbar(im, cax=cax)
    
def vmini(x):
    return np.percentile(x.flatten(), 10)
        
def vmaxi(x):
    return np.percentile(x.flatten(), 90)
    
def ploteo(x):
    '''
    Ploteo básico de bandas.

    '''
    plt.figure(figsize=(7,7), dpi=150)
    im = plt.imshow(x, vmin = vmini(x), vmax = vmaxi(x))
    add_colorbar(im)
    plt.xticks([])
    plt.yticks([])
    plt.show()
    
def clases_ndvi(x):
    '''
    Asigna clases del 0 al 4, según los valores
    que encuentre en la matriz ingresada.
    (pensada para el caso con x = ndvi)

    '''
    clases = np.zeros(x.shape)
    for i in range(x.shape[0]):
        for j in range(x.shape[1]):
            if x[i][j] < 0:
                clases[i][j] = 0
            elif 0 < x[i][j] < 0.1:
                clases[i][j] = 1
            elif 0.1 <= x[i][j] < 0.25:
                clases[i][j] = 2
            elif 0.25 <= x[i][j] < 0.4:
                clases[i][j] = 3
            elif 0.4 <= x[i][j] < 3:
                clases[i][j] = 4
            else:
                pass
    return clases

def plot_ndvi(x):
    '''
    Ploteo especial para visualizar NDVI y 
    sus clases.

    '''
    plt.figure(figsize=(7,7), dpi=150)
    colormap = ListedColormap(['black','y', 'yellowgreen', 'g', 'darkgreen'])
    im = plt.imshow(x, cmap=colormap)
    plt.xticks([])
    plt.yticks([])
    p0 = mpatches.Patch(color='black', label='No vegetada')
    p1 = mpatches.Patch(color='y', label='Área desnuda')
    p2 = mpatches.Patch(color='yellowgreen', label='Vegetación baja')
    p3 = mpatches.Patch(color='g', label='Vegetación moderada')
    p4 = mpatches.Patch(color='darkgreen', label='Vegetación densa')
    plt.legend(handles=[p0, p1, p2, p3, p4], fontsize='xx-small',loc='upper left', bbox_to_anchor=(1, 1))
    plt.title('Landsat 8 - Clases de NDVI')
    plt.show()

def crear_img_png(carpeta, banda):
    '''
    En la "carpeta" ingresada, formato str, se grafica el número
    de banda ingresado en la variable "banda". (banda debe ser una 
    cadena entre el 1 y el 7 inclusive.

    '''
    current = os.getcwd()
    directorio = os.path.join(current,carpeta)
    var_name = eval('Bandas().banda_{}'.format(str(banda)))
    plt.figure(figsize=(7,7), dpi=150)
    im = plt.imshow(var_name, vmin = vmini(var_name), vmax = vmaxi(var_name))
    add_colorbar(im)
    plt.xticks([])
    plt.yticks([])
    plt.title('Banda={}'.format(str(banda)))
    plt.savefig(directorio+'\\'+'banda_'+str(banda)+'.png')
    plt.show()

def crear_hist_png(carpeta, banda, bins):
    '''
    En la "carpeta" ingresada, formato str, se grafica el histograma
    asociado al nro de banda ingresado en la variable "banda" 
    (banda debe ser una cadena entre el 1 y el 7 inclusive.
    bins son la cantidad de intervalos del histograma, debe ser int.
    '''
    current = os.getcwd()
    directorio = os.path.join(current,carpeta)
    var_name = eval('Bandas().banda_{}'.format(str(banda)))
    plt.figure(figsize=(7,7), dpi=150)
    plt.hist(var_name.flatten(),bins = bins)
    plt.xlim((vmini(var_name)-0.5,vmaxi(var_name)+0.5))
    plt.title('Histograma Banda={}'.format(str(banda)))
    plt.savefig(directorio+'\\'+'hist_banda_'+str(banda)+'.png')
    plt.show()
    
#%% Ver una banda
# bandauno = Bandas().banda_1
# ploteo(bandauno)
#%%Análisis NDVI
# ndvi = Bandas().NDVI()
# ndvi_class = clases_ndvi(ndvi)
# plot_ndvi(ndvi_class)
#%%Un poquito de testeo
# crear_img_png('testing', '1')
# crear_hist_png('testing', '2', 100)
#%%
for i in range(1,8):
    crear_img_png('testing', i)
    crear_hist_png('testing', i, 100)
#%%Banda 5: La que veo con mayor bimodalidad.

binaria = Bandas().banda_5
binaria[binaria<=1] = -1
binaria[binaria>1] = 1
plt.figure(figsize=(7,7), dpi=150)
colormap = ListedColormap(['blue','red'])
im = plt.imshow(binaria, cmap=colormap)
plt.xticks([])
plt.yticks([])
plt.title('Binaria banda 5')
plt.show()
# viendo esto intuyo fuertemente que los dos tipos de pixeles responden a sectores
# a tierra (rojo) o agua (azul)
































#ESTO QUEDA PARA MI, NO VER.
# banda_1 = np.load('LC08_L1TP_225084_20180213_20180222_01_T1_sr_band1_clip.npy')
# banda_2 = np.load('LC08_L1TP_225084_20180213_20180222_01_T1_sr_band2_clip.npy')
# banda_3 = np.load('LC08_L1TP_225084_20180213_20180222_01_T1_sr_band3_clip.npy')
# banda_4 = np.load('LC08_L1TP_225084_20180213_20180222_01_T1_sr_band4_clip.npy')
# banda_5 = np.load('LC08_L1TP_225084_20180213_20180222_01_T1_sr_band5_clip.npy')
# banda_6 = np.load('LC08_L1TP_225084_20180213_20180222_01_T1_sr_band6_clip.npy')
# banda_7 = np.load('LC08_L1TP_225084_20180213_20180222_01_T1_sr_band7_clip.npy')
# for i in range(1,8):
#     var_name = 'banda_{}'.format(i)
#     plt.imshow(eval(var_name))
#     plt.show()