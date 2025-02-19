from tkinter import messagebox
from src.uiMain.Excepciones.errorAplicacion import ErrorAplicacion
class ExceptionC1(ErrorAplicacion):
    def __init__(self, mensaje):
        self.mensajeValoresNovalidos=f" Error de entrada de dato: {mensaje} "
        super().__init__( self.mensajeValoresNovalidos)

class ExcepcionEnteroNoValido(ExceptionC1):
     def __init__(self, valor):
        self.mensajeValor=f" La entrada {valor} no contiene un valor válido, por favor, intetar de nuevo "
        super().__init__( self.mensajeValor)

class ExcepcionContenidoVacio(ExceptionC1):
    def __init__(self, entradas):
        self.mensajeEntradas=f" Necesita llenar la(s) entrada(s) {entradas} para continuar"
        super().__init__( self.mensajeEntradas)

class ExcepcionStringNoEntero(ExceptionC1):
    def __init__(self, entero):
        self.mensajeEntero=f" La entrada {entero} no es válida, debe llenar este campo solo con String"
        super().__init__( self.mensajeEntero)

    def enteroNoValido(self):
       messagebox.showwarning("Alerta", f"{self}")
       raise self
    def contenidoVacio(self):
        messagebox.showwarning("Alerta", f"{self}")
        raise self
    
   # def stringNoEntero(self, string):



    


    
    





    
