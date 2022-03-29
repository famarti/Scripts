# -*- coding: utf-8 -*-

class Lote:
    def __init__(self, nombre, cajones, precio):
        self.nombre = nombre
        self.cajones = cajones
        self.precio = precio
    
    def costo(self):
        costo = self.cajones * self.precio
        return costo
    
    def __repr__(self):
        return f'Lote({self.nombre},{self.cajones},{self.precio})'

        
