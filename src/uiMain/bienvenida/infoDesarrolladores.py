import tkinter as tk
import os
import random
from tkinter import ttk
from PIL import Image, ImageTk, ImageOps

desarrolladores=[
    """Andrea Merino""",
    """Juanita Rosero""",
    """Gelsy Jackelin Lozano""",
    """Andres David Calderón""",
    """Luis Esteban Rincón"""
]
carpetaDesarrolladores=[
    "andrea",
    "juanita",
    "jackelin",
    "andres",
    "luis"
]
hojasDeVida=[
    """
    Representada Por: Beatriz pinzón
    Edad: 17 años
    Ciudad Natal: Medellin
    Programa: Ingeniería de Sistemas
    Gustos: La programación y el arte.
        """,
    """
    Representada Por: Armando Mendoza
    Edad: 18 años
    Ciudad Natal: Pasto
    Programa: Ingeniería de Sistemas
    Gustos: Bailar y los desafíos.   
    """,
    """
    Representada Por: Mariana valdez
    Edad: 18 años
    Ciudad Natal: Quibdó
    Programa: Ingeniería de Sistemas
    Gustos: Leer, nadar, escribir y dibujar
    """,
    """
    Representado Por: Nicolas mora
    Edad: 18 años
    Ciudad Natal: Tuluá
    Programa: Ingeniería de Sistemas
    Gustos:La tecnología y la programación.
    """,
    #Logros: En el pasado he desarrollado videojuegos, apps web y progresivas. 2 Años como freelancer en fiverr.
    """
    Representado Por: Mario Calderón
    Edad: 19 años
    Ciudad Natal: Cúcuta
    Programa: Ingeniería de Sistemas
    Gustos: El conocimiento y el deporte.
    """
    #Logros: Me gusta estudiar de forma autónoma inglés, matemáticas y algunos lenguajes de programación. Como también, procuro trabajar en mis tiempos libres y vacaciones para ayudar a costear mi vida de foráneo.
]
class infoDesarrolladores(tk.Frame):
    def __init__(self,window, master=None):
        self.mostrando=False
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
            self.labelsImagenesDesarrollador.append(tk.Canvas(master = self.contenedorAbajoP6, highlightthickness=0, width=self.winfo_width()/4, height=self.winfo_height()/4))
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
        # Get container width and height for images
        container_width = self.contenedorAbajoP6.winfo_width()
        container_height = self.contenedorAbajoP6.winfo_height()

        for i in range(4):
            label: tk.Canvas = self.labelsImagenesDesarrollador[i]
            imagenOriginal = Image.open(f"{os.getcwd()}\\src\\uiMain\\imagenes\\{carpetaDesarrolladores[self.desarrollador]}\\{i+1}.png")
            
            # Adjust the scaling factor
            multiplicador = 1  
            new_width = round(container_width / 2 * multiplicador)  
            new_height = round(container_height / 2 * multiplicador)

            # Ensure the new size is valid (avoid division by zero or negative size)
            if new_width <= 0 or new_height <= 0:
                continue
            
            # Resize the image while maintaining aspect ratio
            image_resized = ImageOps.contain(imagenOriginal, (new_width, new_height))
            self.imagenesDesarrollador[i] = ImageTk.PhotoImage(image_resized)
            label.delete("imagen") 
            label.create_image(label.winfo_width() // 2, label.winfo_height() // 2, anchor="center", image=self.imagenesDesarrollador[i], tags="imagen")