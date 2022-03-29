# -*- coding: utf-8 -*-
#!/usr/bin/env python3

import os
import sys
#%% Version humilde, para carpeta ordenar
# path_to_dir= os.path.join('..','Data','ordenar')
# os.chdir(path_to_dir)

# for root,dirs,files in os.walk('.'):
#     for name in files:
#         if '.png' in name:
#             print(os.path.join(root,name))
#%%Versión full
directorio = sys.argv[1]
current = os.getcwd()    
folder = os.path.join(current,directorio)
for root, dirs, files in os.walk(folder):
    for name in files:
        if '.png' in name:
            print(os.path.join(root,name))
#%%