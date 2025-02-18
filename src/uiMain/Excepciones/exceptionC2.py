from tkinter import messagebox
from src.uiMain.Excepciones.errorAplicacion import ErrorAplicacion

class ExceptionC2(ErrorAplicacion):
    def __init__(self, mensaje):
        super().__init__(mensaje)

    def codigoTarjetaRegalo(self, codigo):
        messagebox.askyesno("Notificación", f" El código {codigo} no se encuentra habilitado. ¿Desea intentar nuevamente?")
        raise self #Posible excepción
    