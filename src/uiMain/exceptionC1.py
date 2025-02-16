from tkinter import Tk
from tkinter import messagebox
from src.gestorAplicacion.fecha import Fecha

class ExceptionC1(ErrorAplicacion):
    def __init__(self, mensaje):
        super().__init__(mensaje)

    def fechaNoValidada(self):
       messagebox.showwarning("Alerta", f"{self}")
       raise self
    
