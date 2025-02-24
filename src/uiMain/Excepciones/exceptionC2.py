from tkinter import messagebox
from src.uiMain.Excepciones.errorAplicacion import ErrorAplicacion

class ExceptionC2(ErrorAplicacion):
    def __init__(self, mensaje):
        self.mensajeCompleto = f" Error: {mensaje}"
        super().__init__(self.mensajeCompleto)

class ExcepcionCodigoTarjetaregalo(ExceptionC2):
    def __init__(self, codigo):
        self.mensajeCodigo = f" El código {codigo} no se encuentra habilitado. ¿Desea intentar nuevamente?"
        super().__init__(self.mensajeCodigo) #Ya

class ExcepcionPrendaNoExistente(ExceptionC2):
    def __init__(self, prenda):
        self.mensajePrenda = f" La prenda {prenda} no es vendida en nuestra empresa. Intente nuevamente"
        super().__init__(self.mensajePrenda) #Ya

class ExcepcionEmpleadoNoEncontrado(ExceptionC2):
    def __init__(self):
        self.mensajeEmpleado = f"Empleado no valido","Verifique que el empleado trabaja en la empresa."
        super().__init__(self.mensajeEmpleado) #Puede que falten algunas

class ExcepcionAgregarOtraPrenda(ExceptionC2):
    def __init__(self):
        self.mensajeCompra = f"¿Desea agregar más prendas a la compra?"
        super().__init__(self.mensajeCompra) #Ya