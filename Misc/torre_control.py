# -*- coding: utf-8 -*-

#torre_control.py
class TorreDeControl:
    '''
    Cola de aviones, con operaciones de nueva_partida,
    nuevo_arribo con prioridad para encolar a lista de espera,
    ver_estado para preguntar qué aviones esperan aterrizar/despegar, 
    asignar_pista para desencolar aviones en espera, entre otras.
    '''
    def __init__(self):
        '''
        creamos cola vacía
        '''
        self.items = []
        self.items_vip = []
    
    def nuevo_arribo(self, x):
        self.items_vip.append(x)
        
    def nueva_partida(self, x):
        self.items.append(x)
    
    def ver_estado(self):
        if len(self.items) != 0:
            print(f'Vuelos esperando para despegar: {self.imprimir_despegar()}')
        else:
            print('No hay vuelos esperando para despegar')
        
        if len(self.items_vip) != 0:
            print(f'Vuelos esperando para aterrizar: {self.imprimir_arribar()}')
        else:
            print('No hay vuelos esperando para aterrizar')
    
    def long_cola(self):
        return len(self.items) + len(self.items_vip)
    
    def esta_vacia(self):
        return self.long_cola() == 0
    
    def asignar_pista(self):
        if self.esta_vacia():
            print('No hay vuelos en espera')
        
        else:
        
            if len(self.items_vip):
                avion = self.items_vip.pop(0)
                print(f'El vuelo {avion} aterrizó con éxito.')
            else:
                avion = self.items.pop(0)
                print(f'El vuelo {avion} despegó con éxito.')
        
    
    def imprimir_despegar(self):
        res = ''
        res += ', '.join(self.items)
        return res
    def imprimir_arribar(self):
        res = ''
        res += ', '.join(self.items_vip)
        return res
    
class Cola:
    '''Representa a una cola, con operaciones de encolar y desencolar.
    El primero en ser encolado es tambien el primero en ser desencolado.
    '''

    def __init__(self):
        '''Crea una cola vacia.'''
        self.items = []

    def encolar(self, x):
        '''Encola el elemento x.'''
        self.items.append(x)

    def desencolar(self):
        '''Elimina el primer elemento de la cola 
        y devuelve su valor. 
        Si la cola esta vacia, levanta ValueError.'''
        if self.esta_vacia():
            raise ValueError('La cola esta vacia')
        return self.items.pop(0)

    def esta_vacia(self):
        '''Devuelve 
        True si la cola esta vacia, 
        False si no.'''
        return len(self.items) == 0