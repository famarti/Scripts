# -*- coding: utf-8 -*-
"""
animal.py
"""
import random
from tablero import Tablero

class Animal(object):
    """docstring for Animal"""
    def __init__(self):
        super(Animal, self).__init__()
        self.reproducciones_pendientes = 4
        self.edad = 0
        self.sexo = str(random.sample(['Macho','Hembra'],k=1)).strip("[]''")
        self.energia = self.energia_maxima
        self.es_reproductore = False
        self.cria_x_ciclo = 0

    def pasar_un_ciclo(self):
        self.energia -= 1 
        self.edad += 1
        self.cria_x_ciclo += 1
        if (self.reproducciones_pendientes > 0) and (self.edad > 1) and (self.cria_x_ciclo >= 1): 
            self.es_reproductore = True

    def en_vida(self):
        return (self.edad <= self.edad_maxima) and self.energia > 0

    def tiene_hambre(self):
        if self.energia <= (self.energia_maxima)/2:
            return True
        else:
            return False
        #pass

    def es_leon(self):
        return False

    def es_antilope(self):
        return False

    def puede_reproducir(self):
        return self.es_reproductore

    def tener_cria(self):
        self.reproducciones_pendientes -= 1
        self.cria_x_ciclo = 0

    def reproducirse(self, vecinos, lugares_libres):
        pos = None
        animal = vecinos
        if lugares_libres:
            animal.tener_cria()
            self.tener_cria()
            pos = random.choice(lugares_libres)

        return pos

    def alimentarse(self, animales_vecinos = None):
        self.energia = self.energia_maxima
        return None

    def moverse(self, lugares_libres):
        pos = None
        if lugares_libres:
            pos = random.choice(lugares_libres)

        return pos

    def fila_str(self):
        return f"{self.edad:>3d}    {self.energia:>3d}/{self.energia_maxima:<3d}       {self.es_reproductore!s:<5}"

    def __format__(self):
        return self.__repr__()

    def __str__(self):
        return self.__repr__()


class Leon(Animal):
    """docstring for Leon"""
    def __init__(self):
        self.energia_maxima = 6
        self.edad_maxima = 10
        super(Leon, self).__init__()
        self.cria_x_ciclo = 0

    def es_leon(self):
        return True

    def alimentarse(self, animales_vecinos):
        # Se alimenta si puede e indica la posición del animal que se pudo comer
        pos = None
        if self.tiene_hambre(): # no está lleno
            presas_cercanas = [ (pos,animal) for (pos, animal) in animales_vecinos if animal.es_antilope() ]
            if presas_cercanas: # y hay presas cerca
                super(Leon, self).alimentarse()
                (pos, animal) = random.choice(presas_cercanas)

        return pos


    def __repr__(self):
        if 'Macho' in self.sexo:
            return "Lm{}".format(self.edad)
        else:
            return "Lh{}".format(self.edad)



class Antilope(Animal):
    """docstring for Antilope"""
    def __init__(self):
        self.energia_maxima = 10
        self.edad_maxima = 6
        super(Antilope, self).__init__()
        self.reproducciones_pendientes = 3
        self.cria_x_ciclo = 0

    def es_antilope(self):
        return True

    def __repr__(self):
        if 'Macho' in self.sexo:
            return "Am{}".format(self.edad)
        else:
            return "Ah{}".format(self.edad)
