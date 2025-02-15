import tkinter as tk
import os
import random
from tkinter import ttk
from PIL import Image, ImageTk, ImageOps

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
    """
    Tengo 18 años, nací en Tuluá - Valle del Cauca. Soy estudiante de ingeniería de sistemas, apasionado por la tecnología y la programación.
    En el pasado he desarrollado videojuegos, apps web y progresivas.
    2 Años como freelancer en fiverr.
    Personaje: Nicolas mora""",
    """
    Tengo 19 años. Nací en Cúcuta - N/S. Soy estudiante de ingeniería de sistemas, apasionado por el conocimiento, los números y el deporte.
    Me gusta estudiar de forma autónoma inglés, matemáticas y algunos lenguajes de programación.
    Como también, procuro trabajar en mis tiempos libres y vacaciones para ayudar a costear mi vida de foráneo.
    Personaje: Hermes pinzon"""
]

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
        self.hojaDeVida = ttk.Label(master = self.p5HojaDeVida, text=hojaDeVida, wraplength=320,width=30)

        self.hojaDeVida.grid(row = 1, column = 0, sticky="nswe")
        self.nombreDesarrollador.grid(row=0, column=0, padx=10, pady=10)

        # ponemos listeners
        cambiarHoja = lambda e : self.cambiarHojaDeVida()
        self.p5HojaDeVida.bind("<Button-1>", cambiarHoja)
        self.nombreDesarrollador.bind("<Button-1>", cambiarHoja)
        self.hojaDeVida.bind("<Button-1>", cambiarHoja)

        self.p5HojaDeVida.grid(row = 0, column = 0, padx=10, pady=10, sticky="nswe")
        self.p5HojaDeVida.rowconfigure(0,weight=1)
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
        self.window.bind("<Map>", lambda e: self.actualizarImagenes())

        self.contenedorAbajoP6.grid(row = 1, column = 0, padx=10, pady=10, sticky="nswe")
        self.contenedorAbajoP6.rowconfigure(0,weight=3)
        self.contenedorAbajoP6.rowconfigure(1,weight=3)
        self.contenedorAbajoP6.columnconfigure(0,weight=3)
        self.contenedorAbajoP6.columnconfigure(1,weight=3)

        self.rowconfigure(0,weight=10)
        self.rowconfigure(1,weight=20)

        self.columnconfigure(0,weight=10)

    
    def actualizarImagenes(self):
        for i in range(4):
            label:tk.Canvas = self.labelsImagenesDesarrollador[i]
            imagenOriginal=Image.open(f"{os.getcwd()}\\src\\uiMain\\imagenes\\{carpetaDesarrolladores[self.desarrollador]}\\{i+1}.png")
            multiplicador=1
            tamaños=(round(self.contenedorAbajoP6.winfo_width()/2*multiplicador),round(self.contenedorAbajoP6.winfo_height()/2*multiplicador))
            if tamaños[0]>0:
                self.imagenesDesarrollador[i]=ImageTk.PhotoImage(ImageOps.contain(imagenOriginal, tamaños))
                label.delete("imagen")
                label.create_image(label.winfo_width()//2, label.winfo_height()//2, anchor="center", image=self.imagenesDesarrollador[i], tags="imagen")