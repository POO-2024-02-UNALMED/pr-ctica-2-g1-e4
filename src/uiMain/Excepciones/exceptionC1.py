from tkinter import messagebox
from src.uiMain.Excepciones.errorAplicacion import ErrorAplicacion

class ExceptionC1(ErrorAplicacion):
    def __init__(self, mensaje):
        self.mensajeValoresNovalidos=f" Error de entrada de dato: {mensaje} "
        super().__init__( self.mensajeValoresNovalidos)

class ExcepcionValorNoValido(ExceptionC1):
     def __init__(self, valor):
        self.mensajeValor=f" La(s) entrada(s) {valor} no contiene(n) un valor válido, por favor, intentar de nuevo "
        super().__init__( self.mensajeValor) #Faltan algunas

class ExcepcionContenidoVacio(ExceptionC1):
    def __init__(self, entradas):
        self.mensajeEntradas=f" Necesita llenar la(s) entrada(s) {entradas} para continuar"
        super().__init__( self.mensajeEntradas) #Ya funcionAAAAAAAAAAAAAAAAAAAAAAAAAAAAA

class ExcepcionStringNoNumero(ExceptionC1):
    def __init__(self, entero):
        self.mensajeEntero=f" La entrada {entero} no es válida, debe llenar este campo solo con String"
        super().__init__(self.mensajeEntero) #Faltan algunas
        
class ExcepcionNumeroNoString(ExceptionC1):
    def __init__(self, string):
        self.mensajeEntero=f" La entrada {string} no es válida, debe llenar este campo solo con números"
        super().__init__( self.mensajeEntero) #Faltan algunas




    


    
    





    
