import tkinter as tk
import os
import random
from src.uiMain.startFrame import pasarAVentanaPrincipal

desarrolladores=[
    """ANDREA MERINO""",
    """JUANITA ROSERO:""",
    """GELSY JACKELINE""",
    """ANDRES DAVID""",
    """LUIS ESTEBAN"""
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
        self.fotosDesarrolladores=[
            [
            tk.PhotoImage(master=self, file=f"{os.getcwd()}\\src\\uiMain\\imagenes\\andrea\\1.png"),
            tk.PhotoImage(master=self, file=f"{os.getcwd()}\\src\\uiMain\\imagenes\\andrea\\2.png"),
            tk.PhotoImage(master=self, file=f"{os.getcwd()}\\src\\uiMain\\imagenes\\andrea\\3.png"),
            tk.PhotoImage(master=self, file=f"{os.getcwd()}\\src\\uiMain\\imagenes\\andrea\\4.png"),
            ],
            [
            tk.PhotoImage(master=self, file=f"{os.getcwd()}\\src\\uiMain\\imagenes\\luis\\1.png"),
            tk.PhotoImage(master=self, file=f"{os.getcwd()}\\src\\uiMain\\imagenes\\luis\\2.png"),
            tk.PhotoImage(master=self, file=f"{os.getcwd()}\\src\\uiMain\\imagenes\\luis\\3.png"),
            tk.PhotoImage(master=self, file=f"{os.getcwd()}\\src\\uiMain\\imagenes\\luis\\4.png"),
            ],
            [
            tk.PhotoImage(master=self, file=f"{os.getcwd()}\\src\\uiMain\\imagenes\\jackelin\\1.png"),
            tk.PhotoImage(master=self, file=f"{os.getcwd()}\\src\\uiMain\\imagenes\\jackelin\\2.png"),
            tk.PhotoImage(master=self, file=f"{os.getcwd()}\\src\\uiMain\\imagenes\\jackelin\\3.png"),
            tk.PhotoImage(master=self, file=f"{os.getcwd()}\\src\\uiMain\\imagenes\\jackelin\\4.png"),
            ],
            [
            tk.PhotoImage(master=self, file=f"{os.getcwd()}\\src\\uiMain\\imagenes\\juanita\\1.png"),
            tk.PhotoImage(master=self, file=f"{os.getcwd()}\\src\\uiMain\\imagenes\\juanita\\2.png"),
            tk.PhotoImage(master=self, file=f"{os.getcwd()}\\src\\uiMain\\imagenes\\juanita\\3.png"),
            tk.PhotoImage(master=self, file=f"{os.getcwd()}\\src\\uiMain\\imagenes\\juanita\\4.png"),
            ],
            [
            tk.PhotoImage(master=self, file=f"{os.getcwd()}\\src\\uiMain\\imagenes\\andres\\1.png"),
            tk.PhotoImage(master=self, file=f"{os.getcwd()}\\src\\uiMain\\imagenes\\andres\\2.png"),
            tk.PhotoImage(master=self, file=f"{os.getcwd()}\\src\\uiMain\\imagenes\\andres\\3.png"),
            tk.PhotoImage(master=self, file=f"{os.getcwd()}\\src\\uiMain\\imagenes\\andres\\4.png"),
            ]
        ]

    def cambiarHojaDeVida(self):
        if (self.desarrollador == 4):
            self.desarrollador = 0
        else:
            self.desarrollador += 1
        
        hojaDeVida = hojasDeVida[self.desarrollador]
        nombre = desarrolladores[self.desarrollador]
        self.nombreDesarrollador.config(text=nombre)
        self.hojaDeVida.config(text=hojaDeVida)
        fotosDesarrollador = self.fotosDesarrolladores[self.desarrollador]


        

    def create_widgets(self):

        self.p5HojaDeVida = tk.Frame(master = self, highlightbackground="black",highlightthickness=2)
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

        self.contenedorAbajoP6 = tk.Frame(master = self, highlightbackground="black",highlightthickness=2)
        self.bettyYElOtro = tk.PhotoImage(master = self.window, file = f"{os.getcwd()}\\src\\uiMain\\imagenes\\bettyYElOtro.png")
        self.labelsImagenesDesarrollador=[]


        self.contenedorAbajoP6.grid(row = 1, column = 0, padx=10, pady=10, sticky="nswe")
        self.contenedorAbajoP6.rowconfigure(0,weight=10)
        self.contenedorAbajoP6.columnconfigure(0,weight=10)

        self.rowconfigure(0,weight=10)
        self.rowconfigure(1,weight=15)

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
        self.frameArriba = tk.Frame(master = self, highlightbackground="black",highlightthickness=2)
        mensaje = """Bienvenido a ecomoda, donde aplicamos teoría y practica:
teoría es cuando sabemos todo pero nada funciona, y la practica es cuando
todo funciona pero no se sabe porqué. En ecomoda, juntamos la teoría y la practica: Nada
funciona, y no sabemos porqué."""

        self.saludo = tk.Label(self.frameArriba, text=mensaje, justify="center")
        self.frameArriba.bind('<Configure>', lambda e: self.saludo.config(wraplength=self.frameArriba.winfo_width()*0.9))
        self.saludo.pack(expand=True)
        
        self.frameArriba.grid(row = 0, column = 0, padx=10, pady=10, sticky="nswe")

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

    def pasarAPrincipal(self):
        self.window.destroy()
        pasarAVentanaPrincipal()


    def create_widgets(self):
        self.archivoImagenSistema = tk.PhotoImage(f"{os.getcwd()}\\src\\uiMain\\imagenes\\logoEcomoda.png")
        self.imagenSistema =tk.PhotoImage(master=self,file=self.archivoImagenSistema)
        img_resized = self.imagenSistema.subsample(2, 2)  

        # Crear el label con la imagen redimensionada
        foto = tk.Label(master=self, image=img_resized)
        foto.image = img_resized  # Mantener la referencia de la imagen
        foto.grid(row = 0, column = 0)

        self.inicio = tk.Button(master = self,text="Seguir a la ventana principal", command= lambda : self.pasarAPrincipal())
        self.inicio.grid(row = 1, column = 0)

        self.columnconfigure(0,weight=10)
        self.rowconfigure(0,weight=10)
        self.rowconfigure(1,weight=2)

#def cambiarTamano(event, imagen:tk.PhotoImage,display:tk.Canvas ,contenedor:tk.Frame):
    #imagen = imagen.resize((contenedor.winfo_width(),contenedor.winfo_height()))
    #display.delete("IMG")
    #display.create_image(0, 0, image=tk.PhotoImage(imagen), anchor="nw", tags="IMG")
    

def bienvenida():
    window = tk.Tk()
    window.geometry("800x600")
    app = Aplication(window)
    window.mainloop()