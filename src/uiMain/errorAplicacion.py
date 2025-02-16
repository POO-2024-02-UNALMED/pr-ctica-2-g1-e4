import tkinter as tk
from tkinter import messagebox
class ErrorAplicacion(Exception):
    def __init__(self, mensaje):
        mensajefijo = "Manejo de errores de la Aplicación: "
        super().__init__(mensajefijo + mensaje)  
        self.mensaje_completo = mensajefijo + mensaje

    def __str__(self):
        return self.mensaje_completo  



    
