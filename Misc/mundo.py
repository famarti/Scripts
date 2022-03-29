# -*- coding: utf-8 -*-
"""
mundo.py

"""

from animal import Animal, Leon, Antilope
from tablero import Tablero
import random

def print_debug(msg, print_flag=False):
    if print_flag:
        print(msg)

class Mundo(object):
    """docstring for Mundo"""

    def __init__(self, columnas, filas, n_leones, n_antilopes, debug=False):
        super(Mundo, self).__init__()

        self.debug = debug

        self.ciclo = 0
        self.tablero = Tablero(filas, columnas)
        self.llenar_mundo(n_leones, n_antilopes)


    def llenar_mundo(self, n_leones, n_antilopes):
        for _ in range(n_leones):
            if self.tablero.hay_posiciones_libres():
                print_debug("ubicando un leon", self.debug)
                leon = Leon()
                self.tablero.ubicar_en_posicion_vacia(leon)

        for _ in range(n_antilopes):
            if self.tablero.hay_posiciones_libres():
                print_debug("ubicando un Antilope", self.debug)
                anti = Antilope()
                self.tablero.ubicar_en_posicion_vacia(anti)

    def cant_leones(self):
        return sum([1 for x in self.tablero.elementos() if x.es_leon()])

    def cant_antilopes(self):
        return sum([1 for x in self.tablero.elementos() if x.es_antilope()])
    
    def animales_presentes(self):
        return self.tablero.posiciones

    def etapa_movimiento(self):
        print_debug(f"Iniciando Movimiento en ciclo {self.ciclo}", self.debug)
        for p in self.tablero.posiciones_ocupadas():
            animal = self.tablero.posicion(p)

            posiciones_libres = self.tablero.posiciones_vecinas_libre(p)
            nueva_posicion = animal.moverse(posiciones_libres)
            if nueva_posicion:
                self.tablero.mover(p, nueva_posicion)

    def etapa_alimentacion(self):
        print_debug(f"Iniciando Alimentación en ciclo {self.ciclo}", self.debug)
        for p in self.tablero.posiciones_ocupadas():
            animal = self.tablero.posicion(p)
            animales_cercanos = self.tablero.posiciones_vecinas_con_ocupantes(p)
            desplazo = animal.alimentarse(animales_cercanos)
            if desplazo:
                self.tablero.ubicar(desplazo, self.tablero.retirar(p))

    def etapa_reproduccion(self):
        print_debug(f"Iniciando Reproducción en ciclo {self.ciclo}", self.debug)
        anim = self.animales_presentes()
        anim_coord = [k for k,v in anim.items()]
        for coord in anim_coord:
            parejas_posibles = self.tablero.potencial_pareja_vecina(coord)
            libres = self.tablero.posiciones_vecinas_libre(coord)
            if (parejas_posibles) and (libres) and (self.tablero.pos_reproductore(coord)):
                pos_elegide = random.choice(parejas_posibles)
                elegide = anim[pos_elegide]
                pos_cria = anim[coord].reproducirse(elegide, libres)
                print_debug('Se cruzan'+str(anim[coord])+'y'+str(elegide), self.debug)
                if elegide.es_leon():
                    self.tablero.ubicar(pos_cria, Leon())
                else:
                    self.tablero.ubicar(pos_cria, Antilope())

    def cerrar_un_ciclo(self):
        print_debug(f"Concluyendo ciclo {self.ciclo}", self.debug)
        for p in self.tablero.posiciones_ocupadas():
            animal = self.tablero.posicion(p)
            animal.pasar_un_ciclo() #envejecer, consumir alimento
            if not animal.en_vida():
                self.tablero.retirar(p)
        self.ciclo += 1

    def pasar_un_ciclo(self):
        self.etapa_movimiento()
        self.etapa_alimentacion()
        self.etapa_reproduccion()
        self.cerrar_un_ciclo()


    def __repr__(self):
        res = str(self.tablero)
        res += f"\nEstamos en la ciclo {self.ciclo}"
        res += f"\nCon {self.cant_leones()} Leones, y {self.cant_antilopes()} Antilopes."
        if False:
            res += '\nEspecie   Posicion   años  energia   puede_reproduc\n'
            for p in self.tablero.posiciones_ocupadas():
                animal = self.tablero.posicion(p)
                res += f'{"Leon    " if animal.es_leon() else "Antilope"} {str(p):^10s} {animal.fila_str()}\n'

        return res

    def __str__(self):
        return self.__repr__()
