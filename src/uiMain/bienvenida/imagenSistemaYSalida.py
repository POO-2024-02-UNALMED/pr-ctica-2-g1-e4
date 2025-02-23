from PIL import Image, ImageTk, ImageOps
from src.uiMain.startFrame import pasarAVentanaPrincipal
import tkinter as tk
import os

# Donde se muestran fotos del sistema y el botón para seguir a main. Es p4 en el enunciado de la práctica.
class ImagenSistemaYSalida(tk.Frame):
    def __init__(self, window, master=None):
        super().__init__(master)
        self.master = master
        self.window = window
        self.imagenSistema:int=0
        self.archivoImagenSistema = None
        self.archivoImagenSistemaOriginal= None # Para la mayoría de recursos de tkinter, como imagenes,
        self.foto=None
        # hay que manejarse con referencias, si no se hace, python las elimina y no se muestran
        self.create_widgets()
        self.config(highlightbackground="black", highlightthickness=1)

    def pasarAPrincipal(self):
        self.window.destroy()
        pasarAVentanaPrincipal()

    def actualizarImagenSistema(self,cambiarImagen:bool):
        if cambiarImagen:
            if (self.imagenSistema==4):
                self.imagenSistema=0
            else:
                self.imagenSistema+=1
        
        pathImagenSistema= f"{os.getcwd()}\\src\\uiMain\\imagenes\\sistema\\{self.imagenSistema}.png"
        
        self.archivoImagenSistemaOriginal = Image.open(pathImagenSistema)
        self.archivoImagenSistema = ImageTk.PhotoImage(ImageOps.contain(self.archivoImagenSistemaOriginal, (self.winfo_width(),self.winfo_height())))
        self.foto.delete("imagen")
        self.foto.create_image(self.winfo_width()//2, self.winfo_height()//2, anchor="center", image=self.archivoImagenSistema, tags="imagen")

    def create_widgets(self):
        self.foto = tk.Canvas(master = self, highlightthickness=0,width=self.winfo_width())
        self.foto.grid(row = 0, column = 0,sticky="nswe")
        self.foto.bind("<Enter>", lambda e:  self.actualizarImagenSistema(True))
        self.window.bind("<Map>", lambda e: self.actualizarImagenSistema(False))
        self.bind("<Configure>", lambda e: self.actualizarImagenSistema(False))
        self.foto.bind("<Button-1>", lambda e: self.pasarAPrincipal())
        self.columnconfigure(0,weight=3)
        self.rowconfigure(0,weight=10)
    