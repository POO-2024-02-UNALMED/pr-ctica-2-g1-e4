import tkinter as tk

class StartrFrame(tk.Frame):
    def __init__(self, marco, tituloCriterios, criterios, tituloValores, valores = None, habilitado = None):
        super().__init__(marco, width=200, height=200, bg="white")
        self.marco = marco
        self.tituloCriterios = tituloCriterios
        self.criterios = criterios
        self.tituloValores = tituloValores
        if valores is None:
            self.valores = []
        else:
            self.valores = valores
        self.entradas = []
        self.estado = "normal"
        self.habilitado = habilitado