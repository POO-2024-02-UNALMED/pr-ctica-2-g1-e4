import tkinter as tk
from tkinter import ttk
import os
import random
import math
from PIL import Image, ImageTk, ImageOps
from src.uiMain.bienvenida.infoSistema import infoSistema
from src.uiMain.bienvenida.infoDesarrolladores import infoDesarrolladores
# Si vscode o python marcan esta linea como error, presionar windows+R, escribir cmd, click en ok, en la ventana negra escribir
# pip install pillow y dar enter. Al terminar el proceso volver a ejecutar el programa

class Aplication(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack(expand=1,fill="both")
        self.create_widgets()


    def create_widgets(self):
        self.barraMenus = tk.Menu(self.master)
        self.master.config(menu=self.barraMenus)
        self.inicioMenu = tk.Menu(self.barraMenus, tearoff=0,)
        self.barraMenus.add_cascade(label="Inicio", menu=self.inicioMenu)
        self.inicioMenu.add_command(label="Salir" ,command=lambda: self.salirDelPrograma())
        self.inicioMenu.add_separator()
        self.inicioMenu.add_command(label="Descripción", command=lambda: self.infoSistema.ponerDescripcion())

        self.infoSistema = infoSistema(window = self.master, master = self)
        self.infoSistema.grid(row = 1, column = 1, sticky="sewn")


        self.infoDesarrolladores = infoDesarrolladores(self.master, master = self)
        self.infoDesarrolladores.grid(row = 1, column = 3,sticky="sewn")

        self.columnconfigure(0,weight=1)
        self.columnconfigure(1,weight=15)
        self.columnconfigure(2,weight=1)
        self.columnconfigure(3,weight=5)
        self.columnconfigure(4,weight=1)

        self.rowconfigure(0,weight=1)
        self.rowconfigure(1,weight=9)
        self.rowconfigure(2,weight=1)
    
    def salirDelPrograma(self):
        self.master.destroy()

    def imagenDeTamaño(path:str, masterForImage:tk.Widget):
        archivo = tk.PhotoImage(master = masterForImage, file = path)
        tamañoOriginal = archivo.width()*archivo.height()
        divisor = math.floor(tamañoOriginal/(masterForImage.winfo_width()*masterForImage.winfo_height()))*2
        archivo = archivo.subsample(divisor)
        return archivo
            
    def bienvenida():
        window = tk.Tk()
        window.geometry("800x600")
        app = Aplication(window)
        window.mainloop()

def pasarAVentanaBienvenida():
    window = Aplication.bienvenida()