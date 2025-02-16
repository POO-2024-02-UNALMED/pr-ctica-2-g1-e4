# Dibuja la ventana y la parte externa, y la parte interna la saca de las clases F.
# O en el caso respectivo, no dibuja una funcionalidad, sino frameInicial.
import os
import tkinter as tk
from tkinter.font import Font
import sys
from src.uiMain.F2Insumos import surtir
from src.uiMain.F4Facturaccion import Facturar
from src.uiMain.main import Main
from src.uiMain.frameInicial import frameInicial
from src.uiMain.F3Financiera import deudas
from src.uiMain.F1Humana import F1Humana
from src.uiMain.F5Produccion import producir

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
        numbre = ""
        super().__init__()
        self.title("Ecomoda")
        self.geometry("800x500")
        # Llamar a la función de audio al abrir la ventana
        #reproducir_audio()

        self.barraMenus = tk.Menu(self)
        self.config(menu=self.barraMenus)

        self.archivoMenu = tk.Menu(self.barraMenus, tearoff=0)
        self.barraMenus.add_cascade(label="Archivo", menu=self.archivoMenu)
        self.archivoMenu.add_command(label="Salir", command = lambda : self.pasarABienvenida())

        self.procesosMenu= tk.Menu(self.barraMenus, tearoff=0)
        self.barraMenus.add_cascade(label="Procesos y Consultas", menu=self.procesosMenu)
        self.procesosMenu.add_command(label="Despedir y reemplazar empleados", command = lambda :self.iniciarGestionHumana())
        self.procesosMenu.add_command(label="Pedir insumos", command = lambda : self.eliminarF2())
        self.procesosMenu.add_command(label="Ver el desglose economico de la empresa", command = lambda : self.eliminarF3())
        self.procesosMenu.add_command(label="Facturacion", command = lambda : self.eliminarF4())
        self.procesosMenu.add_command(label="Producir prendas", command= lambda : self.iniciarProduccion())
    

        self.ayudaMenu = tk.Menu(self.barraMenus, tearoff=0)
        self.barraMenus.add_cascade(label="Ayuda", menu=self.ayudaMenu)
        self.ayudaMenu.add_command(label="Acerca de")

        self.areaPrincipal = frameInicial(self)
        self.areaPrincipal.pack(fill="both", expand=True, padx=7, pady=7)
        
    def iniciarGestionHumana(self):
        self.areaPrincipal.destroy()
        self.cambiarFrame(F1Humana(self))
    
    def eliminarF2(self):
        self.areaPrincipal.destroy()
        self.cambiarFrame(surtir(self))
        
    def eliminarF4(self):
        self.areaPrincipal.destroy()
        self.cambiarFrame(Facturar(self))
        
    def eliminarF3(self):
        self.areaPrincipal.destroy()
        self.cambiarFrame(deudas(self))

    def iniciarProduccion(self):
        self.areaPrincipal.destroy()
        self.cambiarFrame(producir(self))
        
    def cambiarFrame(self, reemplazo:tk.Frame):
        self.areaPrincipal = reemplazo
        reemplazo.pack(fill="both", expand=True, padx=7, pady=7)

    def pasarABienvenida(self):
        if isinstance(self.areaPrincipal, frameInicial):
            import src.uiMain.bienvenida.bienvenida as bienvenida
            self.destroy()
            bienvenida.pasarAVentanaBienvenida()
        else:
            self.areaPrincipal.destroy()
            self.cambiarFrame(frameInicial(self))

def pasarAVentanaPrincipal():
    ventana = startFrame()
    ventana.mainloop()