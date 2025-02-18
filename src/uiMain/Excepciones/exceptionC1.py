from tkinter import messagebox
from src.uiMain.Excepciones.errorAplicacion import ErrorAplicacion
class ExceptionC1(ErrorAplicacion):
    def __init__(self, mensaje):
        super().__init__(mensaje)

    def enteroNoValido(self):
       messagebox.showwarning("Alerta", f"{self}")
       raise self
    def contenidoVacio(self):
        messagebox.showwarning("Alerta", f"{self}")
        raise self
    
   # def stringNoEntero(self, string):

   

    


    
    





    
