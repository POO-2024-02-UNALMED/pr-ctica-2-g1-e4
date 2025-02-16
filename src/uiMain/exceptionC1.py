from tkinter import Tk
from tkinter import messagebox
class ExceptionC1(ErrorAplicacion):
    def __init__(self, mensaje):
        super().__init__(mensaje)

    def fechaNoValidada(self):
       messagebox.showwarning("Alerta", f"{self}")
       raise self
    
    def contenidoVacio(self):
        messagebox.showerror("Error", f"{self}")
        raise self




    
