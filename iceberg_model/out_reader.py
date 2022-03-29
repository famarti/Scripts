# -*- coding: utf-8 -*-
#%%
import pandas as pd
import os
#%%
#path_to_master = os.path.join('D:/', 'Programacion', 'python', 'tempanos',
#                              'NRC_Python_Iceberg_Drift_Model-master', 'tests',
#                              '1-berg-no-ensemble',)

#path_to_iil = os.path.join('D:/', 'Programacion', 'python', 'tempanos',
#                              'NRC_Python_Iceberg_Drift_Model-IIL_size', 'tests',
#                              '1-berg-no-ensemble',)

path_to_hycom = os.path.join('D:/', 'Programacion', 'python', 'tempanos',
                             'NRC_Python_Iceberg_Drift_Model-IIL_size', 'tests',
                             '1-berg-no-ensemble', 'B09I', '20211123', 'hycom', 'Berg.out')

path_to_coper = os.path.join('D:/', 'Programacion', 'python', 'tempanos',
                             'NRC_Python_Iceberg_Drift_Model-IIL_size', 'tests',
                             '1-berg-no-ensemble', 'B09I', '20211123', 'copernicus', 'Berg.out')

path_to_coper_melt = os.path.join('D:/', 'Programacion', 'python', 'tempanos',
                             'NRC_Python_Iceberg_Drift_Model-IIL_size', 'tests',
                             '1-berg-no-ensemble', 'B09I', '20211123','melt_on','original', 'copernicus', 'Berg.out')

path_to_master = os.path.join('D:/', 'Programacion', 'python', 'tempanos',
                             'NRC_Python_Iceberg_Drift_Model-IIL_size', 'tests',
                             '1-berg-no-ensemble', 'B09I', '20211123', 'master_hycom', 'Berg.out')

workdir = os.path.join('D:/', 'Programacion', 'python', 'tempanos')

os.chdir(workdir)
#%%
df_hycom = pd.read_csv(path_to_hycom, header = None, sep = r'\s{1,}')
df_coper = pd.read_csv(path_to_coper, header = None, sep = r'\s{1,}')
df_coper_melt_fix = pd.read_csv(path_to_coper_melt, header = None, sep = r'\s{1,}')
df_master = pd.read_csv(path_to_master, header = None, sep = r'\s{1,}')
#df = pd.read_csv('berg_C.out', header = None, sep = r'\s{1,}') # para los de Gaston

#df_A = df[df[1] == 'A']
#df_B = df[df[1] == 'B']
#df_C = df[df[1] == 'C']
#%%
#df_A.to_csv('out_A.csv',index=False)
#df_B.to_csv('out_B.csv',index=False)
#df_C.to_csv('out_C.csv',index=False)
#%%
df_hycom.to_csv('hycom_20211123.csv', index=False)
df_coper.to_csv('coper_20211123.csv', index=False)

df_coper_melt_fix.to_csv('coper_meltorig_20211123.csv', index=False)
df_master.to_csv('hycom_master_20211123.csv', index=False)