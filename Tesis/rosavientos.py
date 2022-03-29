import pandas as pd
from windrose import WindroseAxes
from matplotlib import pyplot as plt
import matplotlib.cm as cm
import numpy as np
import os

workdir = os.path.join('D:/', 'Programacion', 'python', 'tesis', 'csv')
os.chdir(workdir)
# CARGAR DATOS
#esult=pd.read_csv("uwind_dir_marzo.csv",encoding = "ISO-8859-1", sep=';')
#result=pd.read_csv("uwind_dir_febrero.csv",encoding = "ISO-8859-1", sep=';')
result=pd.read_csv("uwind_dir_enero.csv",encoding = "ISO-8859-1", sep=';')
WindDir =result['WindDir'].values
WindSpd	=result['WindSpd'].values
for i in range(0,len(WindSpd)):
    if WindDir[i]<-8000:
        WindDir[i]=np.nan
for l in range(0,len((WindSpd))):
    if WindSpd[l]<0:
        WindSpd[l]=0
for k in range(0,len(WindSpd)):
    if WindSpd[k]<0.277:
        WindSpd[k]=0

ws = WindSpd.copy()
wd = WindDir.copy()


ax = WindroseAxes.from_ax()
ax.bar(wd, ws, normed=True, opening=0.8, edgecolor='white', nsector=8)
ax.set_legend(fontsize = 'xx-large')
ax.set_yticks(np.arange(10, 30, step=5))
ax.set_yticklabels(np.arange(10, 30, step=5))
ax.set_xticklabels(['E', 'NE', 'N', 'NO', 'O', 'SO', 'S', 'SE'])
plt.savefig('windrose_enero.png', format = 'png', dpi = 1000, bbox_inches = 'tight', pad_inches = 0.5)