# -*- coding: utf-8 -*-

import os
import datetime
import sys

folder = sys.argv[1]
current = os.getcwd()
directorio = os.path.join(current,folder)

if 'imgs_procesadas' not in current:
    os.mkdir(os.path.join(current,'imgs_procesadas'))

def grab_date(file):
    i_date = file[-12:-4]
    i_strptime = (datetime.datetime.strptime(i_date, '%Y%m%d')).timestamp()
    return i_date, i_strptime

for root, dirs, files in os.walk(directorio):
    for name in files:
        if '.png' in name:
            path_to_file = os.path.join(root,name)
            fecha_str, fecha_file = grab_date(name)
            os.utime(path_to_file,(fecha_file,fecha_file))
            new_name = name.replace(('_'+fecha_str), '')
            os.rename(path_to_file,os.path.join(current,'imgs_procesadas',new_name))
            




#######IGNORAR LO QUE SIGUE, ME SIRVE PARA MI YO DEL FUTURO.

# def grab_date(file):
#     fechas = []
#     for i in archivos:
#         i_date = i[-12:-4] #agarra la fecha que tiene en el nombre el archivo i
#         i_strftime = datetime.datetime.strptime(i_date, '%Y%m%d')
#         fechas.append(i_strftime)

# In [30]: os.stat('..\Data\ordenar\python_20190812.png')
# Out[30]: os.stat_result(st_mode=33206, st_ino=844424930454474, 
#                         st_dev=1221652788, st_nlink=1, st_uid=0, st_gid=0, 
#                         st_size=90835, st_atime=1620505740, st_mtime=1599835016, st_ctime=1620503853)