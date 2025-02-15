import tkinter as tk
from tkinter import ttk
import os
import random
from src.uiMain.startFrame import pasarAVentanaPrincipal
import math
from PIL import Image, ImageTk, ImageOps
# Si vscode o python marcan esta linea como error, presionar windows+R, escribir cmd, click en ok, en la ventana negra escribir
# pip install pillow y dar enter. Al terminar el proceso volver a ejecutar el programa

desarrolladores=[
    """ANDREA MERINO""",
    """JUANITA ROSERO:""",
    """GELSY JACKELIN""",
    """ANDRES DAVID""",
    """LUIS ESTEBAN"""
]

carpetaDesarrolladores=[
    "andrea",
    "juanita",
    "jackelin",
    "andres",
    "luis"
]

hojasDeVida=[
    """Personaje: Beatriz pinzón""",
    """Personaje: Armando""",
    """Personaje: Mariana valdez""",
    """Personaje: Nicolas mora""",
    """Personaje: Hermes pinzon"""
]
class Aplication(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack(expand=1,fill="both")
        self.create_widgets()
        self.infoDesarrolladores.actualizarImagenes()


    def create_widgets(self):
        self.titulo = tk.Label(self)
        self.titulo["font"] = ("Arial", 30, "bold")
        self.titulo["text"] = "Inicio"
        self.titulo.grid(row = 0, column = 0,columnspan=2, sticky="w", padx=5)

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

def imagenDeTamaño(path:str, masterForImage:tk.Widget):
    archivo = tk.PhotoImage(master = masterForImage, file = path)
    tamañoOriginal = archivo.width()*archivo.height()
    divisor = math.floor(tamañoOriginal/(masterForImage.winfo_width()*masterForImage.winfo_height()))*2
    archivo = archivo.subsample(divisor)
    return archivo
        

class infoDesarrolladores(tk.Frame):
    def __init__(self,window, master=None):
        super().__init__(master)
        self.master = master
        self.window = window
        self.config(highlightbackground="black",highlightthickness=2)
        self.desarrollador=0
        self.imagenesDesarrollador=[None,None,None,None]
        self.create_widgets()

    def cambiarHojaDeVida(self):
        if (self.desarrollador == 4):
            self.desarrollador = 0
        else:
            self.desarrollador += 1
        
        hojaDeVida = hojasDeVida[self.desarrollador]
        nombre = desarrolladores[self.desarrollador]
        self.nombreDesarrollador.config(text=nombre)
        self.hojaDeVida.config(text=hojaDeVida)
        self.actualizarImagenes()


        

    def create_widgets(self):

        self.p5HojaDeVida = tk.Frame(master = self, highlightbackground="black",highlightthickness=1)
        self.p5HojaDeVida.bind()
        self.desarrollador = random.randrange(0,4)
        hojaDeVida = hojasDeVida[self.desarrollador]
        self.nombreDesarrollador = tk.Label(master = self.p5HojaDeVida, text=desarrolladores[self.desarrollador])
        self.nombreDesarrollador.grid(row=0, column=0, padx=10, pady=10)
        self.hojaDeVida = tk.Label(master = self.p5HojaDeVida, text=hojaDeVida)
        self.hojaDeVida.grid(row = 1, column = 0, padx=10, pady=10)

        cambiarHoja = lambda e : self.cambiarHojaDeVida()
        self.p5HojaDeVida.bind("<Button-1>", cambiarHoja)
        self.nombreDesarrollador.bind("<Button-1>", cambiarHoja)
        self.hojaDeVida.bind("<Button-1>", cambiarHoja)

        self.p5HojaDeVida.grid(row = 0, column = 0, padx=10, pady=10, sticky="nswe")
        self.p5HojaDeVida.rowconfigure(0,weight=2)
        self.p5HojaDeVida.rowconfigure(1,weight=10)
        self.p5HojaDeVida.columnconfigure(0,weight=10)

        self.contenedorAbajoP6 = tk.Frame(master = self, highlightbackground="black",highlightthickness=1)
        self.labelsImagenesDesarrollador=[]
        rows=[0,0,1,1]
        columns=[0,1,0,1]
        for i in range(4):
            self.labelsImagenesDesarrollador.append(tk.Canvas(master = self.contenedorAbajoP6, highlightthickness=0, width=self.winfo_width()/3, height=self.winfo_height()/4))
            self.labelsImagenesDesarrollador[i].grid(row=rows[i], column=columns[i], sticky="nswe")

        self.bind("<Configure>", lambda e: self.actualizarImagenes())

        self.contenedorAbajoP6.grid(row = 1, column = 0, padx=10, pady=10, sticky="nswe")
        self.contenedorAbajoP6.rowconfigure(0,weight=3)
        self.contenedorAbajoP6.rowconfigure(1,weight=3)
        self.contenedorAbajoP6.columnconfigure(0,weight=3)
        self.contenedorAbajoP6.columnconfigure(1,weight=3)

        self.rowconfigure(0,weight=10)
        self.rowconfigure(1,weight=15)

        self.columnconfigure(0,weight=10)

    
    def actualizarImagenes(self):
        for i in range(4):
            label:tk.Canvas = self.labelsImagenesDesarrollador[i]
            imagenOriginal=Image.open(f"{os.getcwd()}\\src\\uiMain\\imagenes\\{carpetaDesarrolladores[self.desarrollador]}\\{i+1}.png")
            multiplicador=1
            self.imagenesDesarrollador[i]=ImageTk.PhotoImage(ImageOps.contain(imagenOriginal,(round(label.winfo_width()*multiplicador),round(label.winfo_height()*multiplicador))))
            label.delete("imagen")
            label.create_image(label.winfo_width()//2, label.winfo_height()//2, anchor="center", image=self.imagenesDesarrollador[i], tags="imagen")

class infoSistema(tk.Frame):
    def __init__(self, window, master=None):
        super().__init__(master)
        self.master = master
        self.window = window
        self.create_widgets()
        self.config(highlightbackground="black",highlightthickness=2)

    def create_widgets(self):
        # P3 en el enunciado de la practica
        self.frameArriba = tk.Frame(master = self, highlightbackground="black",highlightthickness=1)
        mensaje = """"""

        self.saludo = tk.Label(self.frameArriba, text=mensaje, justify="center")
        self.frameArriba.bind('<Configure>', lambda e: self.saludo.config(wraplength=self.frameArriba.winfo_width()*0.9))
        self.saludo.pack(expand=True)
        
        self.frameArriba.grid(row = 0, column = 0, padx=10, pady=10, sticky="nswe")

        self.parteAbajo = p4FotosEInicio(self.window ,master = self)
        self.parteAbajo.grid(row = 1, column = 0, padx=10, pady=10, sticky="nswe")


        self.rowconfigure(0,weight=10)
        self.rowconfigure(1,weight=10)
        self.columnconfigure(0,weight=10)

# Donde se muestran fotos del sistema
class p4FotosEInicio(tk.Frame):
    def __init__(self,window, master=None):
        super().__init__(master)
        self.master = master
        self.window = window
        self.imagenSistema=0
        self.archivoImagenSistema = None
        self.create_widgets()
        self.config(highlightbackground="black", highlightthickness=1)

    def pasarAPrincipal(self):
        self.window.destroy()
        pasarAVentanaPrincipal()

    def actualizarImagenSistema(self,cambiarDesarrollador:bool):
        if cambiarDesarrollador:
            if (self.imagenSistema==4):
                self.imagenSistema=0
            else:
                self.imagenSistema+=1
        
        pathImagenSistema= f"{os.getcwd()}\\src\\uiMain\\imagenes\\sistema\\{self.imagenSistema}.png"
        if self.winfo_width()<self.winfo_height():
            minsize = self.winfo_width()
        else:
            minsize = self.winfo_height()

        tamañoMeta=minsize
        self.archivoImagenSistema = tk.PhotoImage(master=self, file=pathImagenSistema)
        anchoOriginal = self.archivoImagenSistema.width()
        divisor = math.floor(anchoOriginal/tamañoMeta)*2
        self.archivoImagenSistema = self.archivoImagenSistema.subsample(divisor,divisor)

        self.foto.config(image = self.archivoImagenSistema )



    def create_widgets(self):
        self.foto = tk.Label(master=self, highlightthickness=0, background="#000000") 
        self.foto.grid(row = 0, column = 0)
        self.foto.bind("<Enter>", lambda e:  self.actualizarImagenSistema(True))
        self.bind("<Configure>", lambda e: self.actualizarImagenSistema(False))

        self.inicio = tk.Button(master = self,text="Seguir a la ventana principal", command= lambda : self.pasarAPrincipal())
        self.inicio.grid(row = 1, column = 0)

        self.columnconfigure(0,weight=3)
        self.rowconfigure(0,weight=10)
        self.rowconfigure(1,weight=2)


def bienvenida():
    window = tk.Tk()
    window.geometry("800x600")
    app = Aplication(window)
    window.mainloop()