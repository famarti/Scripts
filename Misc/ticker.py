# -*- coding: utf-8 -*-
#ticker.py

from vigilante import vigilar
import csv
import informe

def elegir_columnas(rows, indices):
    for row in rows:
        yield [row[index] for index in indices]

def cambiar_tipo(rows, types):
    for row in rows:
        yield [func(val) for func,val in zip(types,row)]

def hace_dicts(rows, headers):
    for row in rows:
        yield dict(zip(headers, row))

def filtrar_datos(filas, nombres):
    for fila in filas:
        if fila['nombre'] in nombres:
            yield fila

def parsear_datos(lines):
    rows = csv.reader(lines)
    rows = elegir_columnas(rows, [0,1,2])
    rows = cambiar_tipo(rows, [str,float,int])
    rows = hace_dicts(rows, ['nombre','precio','volumen'])    
    return rows

# if __name__ == '__main__':
#     lines = vigilar('../Data/mercadolog.csv')
#     rows = parsear_datos(lines)
#     for row in rows:
#         print(row)

class FormatoTabla:
    def encabezado(self, headers):
        '''
        Crea el encabezado de la tabla.
        '''
        raise NotImplementedError()
        
    def fila(self, rowdata):
        '''
        Crea una única fila de datos de la tabla.
        '''
        raise NotImplementedError()
        
class FormatoTablaTXT(FormatoTabla):
    '''
    Generar una tabla en formato TXT
    '''
    def encabezado(self, headers):
        for h in headers:
            print(f'{h:>10s}', end=' ')
        print()
        print(('-'*10+' ')*len(headers))
    def fila(self, data_fila):
        for row in data_fila:
            tup = tuple(row)
            print('%10s %10s %10s' %(tup))
        
class FormatoTablaCSV(FormatoTabla):
    '''
    Generar una tabla en formato CSV
    '''
    def encabezado(self, headers):
        print(','.join(headers))
        
    def fila(self, data_fila):
        for row in data_fila:
            tup = tuple(row)
            print(','.join(tup))

class FormatoTablaHTML(FormatoTabla):
    '''
    Generar una tabla en formato HTML
    '''
    def encabezado(self, headers):
        print('<tr><th>'+'</th><th>'.join(headers)+'</th></tr>')
    
    def fila(self, data_fila):
        for row in data_fila:
            tup = tuple(row)
            print('<tr><th>'+'</th><th>'.join(tup)+'</th></tr>')
        
def crear_formateador(nombre):
    if nombre == 'txt':
        formateador = FormatoTablaTXT()
        return formateador
    elif nombre == 'csv':
        formateador = FormatoTablaCSV()
        return formateador
    elif nombre == 'html':
        formateador = FormatoTablaHTML()
        return formateador
    else:
        raise RuntimeError(f'Unknown format {nombre}')

def reformatear(rows):
    for row in rows:
        yield [str(row[v]) for v in list(row)]


def ticker(camion_file, log_file, fmt):
    camion = informe.leer_camion(camion_file)
    filas = parsear_datos(vigilar(log_file))
    filas = filtrar_datos(filas, camion)
    filas = reformatear(filas)
    formateador = crear_formateador(fmt)
    formateador.encabezado(['Nombre','Precio','Volumen'])
    formateador.fila(filas)
    
