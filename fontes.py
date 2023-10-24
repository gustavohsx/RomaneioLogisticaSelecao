from tkinter import font

class Fontes:


    def __init__(self):
        self._titulo_pagina_inicial = font.Font(family="Helvetica", size=20, weight="bold")
        self._label10 = font.Font(family="Helvetica", size=10)
        self._label12 = font.Font(family="Helvetica", size=12)
        self._label14 = font.Font(family="Helvetica", size=14)


    def tituloPaginaInicial(self):
        return self._titulo_pagina_inicial

    def label10(self):
        return self._label10
    
    def label12(self):
        return self._label12
    
    def label14(self):
        return self._label14