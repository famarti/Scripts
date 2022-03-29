# -*- coding: utf-8 -*-
#hojas_ISO.py

# A4 (210mm de ancho y 297mm de largo)
# A0 miden 841mm de ancho y 1189mm de largo

def A(N):
    if N == 0:
        ancho=841
        largo=1189
        return ancho,largo
    else:
        ancho = A(N-1)[1]//2
        largo = A(N-1)[0]
    return ancho,largo
    