# Dibuja la ventana y la parte externa, y la parte interna la saca de las clases F.
# O en el caso respectivo, no dibuja una funcionalidad, sino principalInicial.
import os
import tkinter as tk
from tkinter.font import Font
import sys
from src.uiMain.main import Main
from src.uiMain.frameInicial import frameInicial
from src.uiMain.F3Financiera import deudas

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
# Inicializar pygame para el audio
#pygame.mixer.init()

# Función para reproducir el audio
#def reproducir_audio():
    #ruta_audio = os.path.join("src", "uiMain", "imagenes", "EcomodaALaOrden.mp3")
    #pygame.mixer.music.load(ruta_audio)  # Cambia la ruta del archivo de audio
    #pygame.mixer.music.play()

class startFrame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ecomoda")
        self.geometry("800x500")
        # Llamar a la función de audio al abrir la ventana
        #reproducir_audio()

        self.barraMenus = tk.Menu(self)
        self.config(menu=self.barraMenus)

        self.archivoMenu = tk.Menu(self.barraMenus, tearoff=0)
        self.barraMenus.add_cascade(label="Archivo", menu=self.archivoMenu)


        self.procesosMenu= tk.Menu(self.barraMenus, tearoff=0)
        self.barraMenus.add_cascade(label="Procesos y Consultas", menu=self.procesosMenu)
        self.procesosMenu.add_command(label="Despedir y reemplazar empleados")
        self.procesosMenu.add_command(label="Pedir insumos")
        self.procesosMenu.add_command(label="Ver el desglose economico de la empresa", command = lambda : self.cambiarVentana(deudas(self)))
        self.procesosMenu.add_command(label="Facturacion")
        self.procesosMenu.add_command(label="Producir prendas")
    

        self.ayudaMenu = tk.Menu(self.barraMenus, tearoff=0)
        self.barraMenus.add_cascade(label="Ayuda", menu=self.ayudaMenu)
        self.ayudaMenu.add_command(label="Acerca de")

        self.areaPrincipal = frameInicial(self)
        self.areaPrincipal.pack(fill="both", expand=True, padx=7, pady=7)

    def cambiarVentana(self,reemplazo:tk.Frame):
        self.areaPrincipal.destroy()
        self.areaPrincipal = reemplazo
        reemplazo.pack(fill="both", expand=True, padx=7, pady=7)

def pasarAVentanaPrincipal():
    ventana = startFrame()
    ventana.mainloop()