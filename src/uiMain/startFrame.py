# Dibuja la ventana y la parte externa, y la parte interna la saca de las clases F.
# O en el caso respectivo, no dibuja una funcionalidad, sino principalInicial.
import os
import tkinter as tk
from tkinter.font import Font
import sys
from src.uiMain.main import Main
from src.uiMain.frameInicial import frameInicial

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
# Inicializar pygame para el audio
#pygame.mixer.init()

# Función para reproducir el audio
#def reproducir_audio():
    #ruta_audio = os.path.join("src", "uiMain", "imagenes", "EcomodaALaOrden.mp3")
    #pygame.mixer.music.load(ruta_audio)  # Cambia la ruta del archivo de audio
    #pygame.mixer.music.play()

ventana = tk.Tk()
ventana.title("Ecomoda")
ventana.geometry("800x500")
# Llamar a la función de audio al abrir la ventana
#reproducir_audio()


opciones = tk.Frame(ventana, height=25)
opciones.pack(side= "top", fill="x", padx=15, pady=2)


barraMenus = tk.Menu(ventana)
ventana.config(menu=barraMenus)


ayudaMenu = tk.Menu(barraMenus, tearoff=0)
barraMenus.add_cascade(label="Ayuda", menu=ayudaMenu)

procesosMenu= tk.Menu(barraMenus, tearoff=0)
barraMenus.add_cascade(label="Procesos y Consultas", menu=procesosMenu)

archivoMenu = tk.Menu(barraMenus, tearoff=0)
barraMenus.add_cascade(label="Archivo", menu=archivoMenu)


areaPrincipal = frameInicial(ventana) # Será eliminado y reemplazado par alguna funcionalidad, cuando se use una 
# de las opciones de procesosButton
areaPrincipal.pack(fill="both", expand=True, padx=7, pady=7)

ventana.mainloop()