from tkinter import font

class Fontes:


    def __init__(self):
        self.titulo_pagina_inicial = font.Font(family="Helvetica", size=20, weight="bold")


    def tituloPaginaInicial(self):
        return self.titulo_pagina_inicial