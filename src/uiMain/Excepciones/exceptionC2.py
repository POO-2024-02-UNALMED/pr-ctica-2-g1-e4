from tkinter import messagebox
from src.uiMain.Excepciones.errorAplicacion import ErrorAplicacion

class ExceptionC2(ErrorAplicacion):
    def __init__(self, mensaje):
        self.mensajeCompleto = f" Error: {mensaje}"
        super().__init__(self.mensajeCompleto)

class ExcepcionCodigoTarjetaregalo(ExceptionC2):
    def __init__(self, codigo):
        self.mensajeCodigo = f" El código {codigo} no se encuentra habilitado. ¿Desea intentar nuevamente?"
        super().__init__(self.mensajeCodigo)

class ExcepcionPrendaNoExistente(ExceptionC2):
    def __init__(self, prenda):
        self.mensajePrenda = f" La prenda {prenda} no es vendida en nuestra empresa. ¿Desea elegir una prenda nuevamente?"
        super().__init__(self.mensajePrenda)
    