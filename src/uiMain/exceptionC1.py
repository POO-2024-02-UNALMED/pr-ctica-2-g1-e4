from tkinter import Tk
from tkinter import messagebox
class ExceptionC1(ErrorAplicacion):
    def __init__(self, mensaje):
        super().__init__(mensaje)

    def fechaNoValidada(self):
       messagebox.showwarning("Alerta", f"{self}")
       raise self
    
    def contenidoVacio(self, dia, mes, año, fechaValida):
        if fechaValida == True:
            if not dia.strip() or not mes.strip() or not año.strip():
                messagebox.showwarning("Alerta", "Debes ingresar una fecha correcta antes de continuar.")
                raise ExceptionC1("No se ingresó una fecha válida.")
            fechaValida = False

        return fechaValida     


    
