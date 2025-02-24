import tkinter as tk
from tkinter import messagebox

class ErrorAplicacion(Exception):
    def __init__(self, mensaje):
        mensajefijo = "Manejo de errores de la Aplicación: "
        self.mensaje_completo = mensajefijo + mensaje
        super().__init__(self.mensaje_completo)  
        
