# -*- coding: utf-8 -*-
#%% animal.py
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
#%% tablero.py

from random import choice
#from animal import Animal, Leon, Antilope

class Tablero(object):
    """docstring for Tablero"""
    # constructor
    def __init__(self, filas, columnas):
        super(Tablero, self).__init__()
        self.filas = filas
        self.columnas = columnas
        self.posiciones = {}
        self.n_posiciones_libres = self.filas * self.columnas

    # modificadores
    def ubicar(self,  pos, elem):
        if not self.ocupada(pos):
            self.n_posiciones_libres -= 1
        self.posiciones[pos] = elem
        return pos in self.posiciones

    def retirar(self, pos):
        self.n_posiciones_libres += 1
        return self.posiciones.pop(pos)

    def mover(self, p_origen, p_destino):
        self.ubicar(p_destino, self.retirar(p_origen))

    # getters
    def posicion(self, pos):
        return self.posiciones[pos]

    def ocupada(self,  pos):
        return pos in self.posiciones

    def libre(self,  pos):
        return pos not in self.posiciones

    def elementos(self):
        return list(self.posiciones.values())

    def n_filas(self):
        return self.filas

    def n_columnas(self):
        return self.columnas
    
    def pos_sexo(self, pos):
        especimen = None
        for k,v in self.posiciones.items():
            if k == pos:
                especimen = v.sexo
        return especimen

    def pos_animal(self, pos):
        animal = None
        animal_esp = None
        for k,v in self.posiciones.items():
            if k == pos:
                animal = v
                if animal.es_leon():
                    animal_esp = 'Leon'
                else:
                    animal_esp = 'Antilope'
        return animal_esp
        

    # modificadores complejos
    def ubicar_en_posicion_vacia(self, elem):
        if not self.hay_posiciones_libres():
            raise RuntimeError("Estás intentado agregar algo al tablero y está lleno")

        pos = choice(self.posiciones_libres())
        self.ubicar(pos, elem)


    # consultas
    def hay_posiciones_libres(self):
        return self.n_posiciones_libres > 0
        # return len(self.posiciones) <  self.filas * self.columnas

    def posiciones_ocupadas(self):
        res = []
        for f in range(self.filas):
            for c in range(self.columnas):
                if self.ocupada((f,c)):
                    res.append((f,c))

        return res

    def posiciones_libres(self):
        res = []
        for f in range(self.filas):
            for c in range(self.columnas):
                if self.libre((f,c)):
                    res.append((f,c))

        return res


    def posiciones_vecinas_libre(self, pos):
        res = self.posiciones_vecinas(pos)
        res = [ p for p in res if self.libre(p)]

        return res

    def posiciones_vecinas_con_ocupantes(self, pos):
        res = self.posiciones_vecinas(pos)
        res = [ (p, self.posicion(p)) for p in res if self.ocupada(p)]

        return res

    def coord_vecinas_con_ocupantes(self, pos):
            res = self.posiciones_vecinas(pos)
            res = [ p for p in res if self.ocupada(p)]
    
            return res

    # auxiliar
    def posiciones_vecinas(self, pos):
        desp=[(-1, -1), (-1, 0), (-1, 1),(0, 1), (1, 1), (1, 0),(1, -1), (0, -1)]

        for i in range(len(desp)):
            f = (desp[i][0] + pos[0])
            c = (desp[i][1] + pos[1])
            desp[i] = (f, c)

        desp = [ (f,c) for f,c in desp if (0<=f and f<self.filas) and (0<=c and c<self.columnas) ]

        return desp

    def potencial_pareja_vecina(self, pos):
        vecinos = self.coord_vecinas_con_ocupantes(pos)
        parejas = []
        for coord in vecinos:
            if (self.pos_animal(pos) == self.pos_animal(coord)) and (self.pos_sexo(pos) != self.pos_sexo(coord)) and (self.pos_reproductore(coord)):
                parejas.append(coord)
        return parejas

    def pos_reproductore(self, pos):
        animales = self.posiciones
        res = [k for k,v in animales.items() if v.es_reproductore]
        if pos in res:
            return True
        else:
            return False

    # impresion
    def __repr__(self):
        res = ""
        for f in range(self.filas-1,-1,-1):
            for c in range(self.columnas):
                res += f"{(str(self.posiciones[(f,c)]) if (f,c) in self.posiciones else '-'):^3}"
            res += "\n"

        return res


    def __str__(self):
        return self.__repr__()



if __name__ == "__main__":
    t = Tablero(2,3)

    for i in range(6):
        t.ubicar_en_posicion_vacia(i)
#%% mundo.py


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
#%%