import tkinter as tk
import os
from PIL import Image, ImageTk


class Aplication(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack(expand=1,fill="both")
        self.create_widgets()

    def create_widgets(self):
        self.titulo = tk.Label(self)
        self.titulo["font"] = ("Arial", 30)
        self.titulo["text"] = "Inicio"
        self.titulo.grid(row = 0, column = 0,columnspan=2, sticky="w")

        self.infoSistema = infoSistema(window = self.master, master = self)
        self.infoSistema.grid(row = 1, column = 1, sticky="sewn")


        self.infoDesarrolladores = infoDesarrolladores(self.master, master = self)
        self.infoDesarrolladores.grid(row = 1, column = 3,sticky="sewn")

        self.columnconfigure(0,weight=1)
        self.columnconfigure(1,weight=10)
        self.columnconfigure(2,weight=1)
        self.columnconfigure(3,weight=10)
        self.columnconfigure(4,weight=1)

        self.rowconfigure(0,weight=1)
        self.rowconfigure(1,weight=9)
        self.rowconfigure(2,weight=1)

        

class infoDesarrolladores(tk.Frame):
    def __init__(self,window, master=None):
        super().__init__(master)
        self.master = master
        self.window = window
        self.config(highlightbackground="black",highlightthickness=2)
        self.create_widgets()

    def create_widgets(self):
        hojaDeVida = """Oye, te hablo desde la prisión
En el mundo en que yo vivo Siempre hay cuatro esquinas
Pero entre esquina y esquina Siempre habrá lo mismo
Para mi no existe el cielo Ni Luna ni estrellas
Para mi no alumbra el Sol Pa' mi todo es tinieblas"""
        self.desarrolladores = tk.Label(master = self, text=hojaDeVida)
        self.desarrolladores.grid(row = 0, column = 0, padx=10, pady=10)
        self.bettyYElOtro = tk.PhotoImage(master = self.window, file = f"{os.getcwd()}\\src\\uiMain\\imagenes\\bettyYElOtro.png")
        self.abajo = tk.Label(master = self, image =self.bettyYElOtro) 
        self.abajo.grid(row = 1, column = 0)

        self.rowconfigure(0,weight=10)
        self.rowconfigure(1,weight=10)

        self.columnconfigure(0,weight=10)

class infoSistema(tk.Frame):
    def __init__(self, window, master=None):
        super().__init__(master)
        self.master = master
        self.window = window
        self.create_widgets()
        self.config(highlightbackground="black",highlightthickness=2)

    def create_widgets(self):
        # P3 en el enunciado de la practica
        frameArriba = tk.Frame(master = self, highlightbackground="black",highlightthickness=2)
        mensaje = """Bienvenido a ecomoda, donde aplicamos teoría y practica:
teoría es cuando sabemos todo pero nada funciona, y la practica es cuando
todo funciona pero no se sabe porqué. En ecomoda, juntamos la teoría y la practica: Nada
funciona, y no sabemos porqué."""
        self.saludo = tk.Label(frameArriba, text=mensaje)
        self.saludo.grid(row = 0, column = 0, sticky="nswe")
        
        frameArriba.grid(row = 0, column = 0, padx=10, pady=10, sticky="nswe")

        self.parteAbajo = p4FotosEInicio(self.window ,master = self)
        self.parteAbajo.grid(row = 1, column = 0, padx=10, pady=10, sticky="nswe")

        self.rowconfigure(0,weight=10)
        self.rowconfigure(1,weight=10)
        self.columnconfigure(0,weight=10)
        
class p4FotosEInicio(tk.Frame):
    def __init__(self,window, master=None):
        super().__init__(master)
        self.master = master
        self.window = window
        self.create_widgets()
        self.config(highlightbackground="black",highlightthickness=2, padx=10, pady=10)

    def create_widgets(self):
        self.perroCosiendo = tk.PhotoImage(master=self.window, file = f"{os.getcwd()}\\src\\uiMain\\imagenes\\perroCosiendo.png")
        self.foto = tk.Label(master = self, image=self.perroCosiendo)
        self.foto.grid(row = 0, column = 0)
        self.inicio = tk.Button(master = self,text="Seguir a la ventana principal", command=self.window.destroy)
        self.inicio.grid(row = 1, column = 0)

def bienvenida():
    window = tk.Tk()
    window.geometry("800x600")
    app = Aplication(window)
    window.mainloop()