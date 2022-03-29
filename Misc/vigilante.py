# -*- coding: utf-8 -*-
# vigilante.py
#%%
# import os
# import time

# f = open('../Data/mercadolog.csv')
# f.seek(0, os.SEEK_END) # mover el índice 0 posiciones desde el EOF (end of file)

# while True:
#     line = f.readline()
#     if line == '':
#         time.sleep(0.5) ##Esperar un rato y
#         continue        # vuelve al comienzo del while.
#     fields = line.split(',')
#     nombre = fields[0].strip('"')
#     precio = float(fields[1])
#     volumen = int(fields[2])
#     if volumen > 1000:
#         print(f'{nombre:>10s} {precio:>10.2f} {volumen:>10d}')
#%% 
import os
import time

def vigilar(nomarchivo):
    with open(nomarchivo) as f:
        f.seek(0, os.SEEK_END)
        while True:
            line = f.readline()
            if line == '':
                time.sleep(0.5) 
                continue  
            yield line

# for line in vigilar('../Data/mercadolog.csv'):
#     print(line)

if __name__ == '__main__':
    import informe
    
    camion = informe.leer_camion('../Data/camion.csv')
    
    for line in vigilar('../Data/mercadolog.csv'):
        fields = line.split(',')
        nombre = fields[0].strip('"')
        precio = float(fields[1])
        volumen = int(fields[2])
        
        if nombre in camion:
            print(f'{nombre:>10s} {precio:>10.2f} {volumen:>10d}')
#%%