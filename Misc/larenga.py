# -*- coding: utf-8 -*-
#larenga.py
def pascal(n,k):
    ''' Triangulo de Pascal
    Pre: n,k mayores o iguales a cero
    Pos: Devuelve el valor del triangulo
    en la fila n, columna k.'''
    if n==0 and k==0:
        res = 1
    elif n<0 and k<0:
        raise RuntimeError('Esa ubicacion no se encuentra dentro de la piramide.')
    elif n<0 or k<0:
        res = 0
    else:
        res = pascal(n-1,k) + pascal(n-1,k-1)
    return res