from src.uiMain.startFrame import pasarAVentanaPrincipal
import tkinter as tk
from src.uiMain.bienvenida.imagenSistemaYSalida import ImagenSistemaYSalida

# P1 en el enunciado de la practica, contiene a P3 y P4
class InfoSistema(tk.Frame):
    def __init__(self, window, master=None):
        super().__init__(master)
        self.master = master
        self.window = window
        self.create_widgets()
        self.config(highlightbackground="black",highlightthickness=2)
        self.parteAbajo.actualizarImagenSistema(False)

    def create_widgets(self):
        # P3 en el enunciado de la practica
        self.frameArriba = tk.Frame(master = self, highlightbackground="black", highlightthickness=1,)
        mensaje = """Bienvenido a ecomoda, 
Haz click en la imagen para empezar"""

        self.saludo = tk.Label(self.frameArriba, text=mensaje, justify="center", font=("Arial", 18, "bold"))
        self.frameArriba.bind('<Configure>', lambda e: self.saludo.config(wraplength=self.frameArriba.winfo_width()*0.9))
        self.saludo.pack(expand=True)
        
        self.frameArriba.grid(row = 0, column = 0, padx=10, pady=10, sticky="nswe")

        self.parteAbajo = ImagenSistemaYSalida(self.window ,master = self)
        self.parteAbajo.grid(row = 2, column = 0, padx=10, pady=10, sticky="nswe") # Se deja una fila para la descripción
        
        self.rowconfigure(0,weight=10)
        self.rowconfigure(2,weight=10)
        self.columnconfigure(0,weight=10)
    
    def ponerDescripcion(self):
        descripcion=tk.Label(master=self,wraplength=250,text="Este es un sistema que le permite gestionar su tienda y fabrica de ropa, en cuanto a todo tipo de recursos, empleados, dinero, ventas, insumos, productos y más.")
        descripcion.grid(row=1,column=0,sticky="nswe")
        self.rowconfigure(1,weight=5)