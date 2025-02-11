import os
import tkinter as tk
from tkinter.font import Font
import winsound
import pygame

# Inicializar pygame para el audio
pygame.mixer.init()

# Función para reproducir el audio
def reproducir_audio():
    ruta_audio = os.path.join("src", "uiMain", "imagenes", "EcomodaALaOrden.mp3")
    pygame.mixer.music.load(ruta_audio)  # Cambia la ruta del archivo de audio
    pygame.mixer.music.play()

ventana = tk.Tk()
ventana.title("Ecomoda")
ventana.geometry("800x500")
# Llamar a la función de audio al abrir la ventana
reproducir_audio()

opciones = tk.Frame(ventana, height=25)
opciones.pack(side= "top", fill="x", padx=15, pady=2)

archivoButton = tk.Button(opciones, text="Archivo")
archivoButton.place(relx=0, rely=0.5, relwidth=0.1, relheight=1, anchor="w")

procesosButton = tk.Button(opciones, text="Procesos y Consultas")
procesosButton.place(relx=0.1, rely=0.5, relwidth=0.2, relheight=1, anchor="w")

ayudaButton = tk.Button(opciones, text="Ayuda")
ayudaButton.place(relx=0.3, rely=0.5, relwidth=0.1, relheight=1, anchor="w")

inicio =  tk.Frame(ventana, bg="blue")
inicio.pack(fill="both", expand=True, padx=7, pady=7)

primerInicio = tk.Frame(inicio, height=150)
primerInicio.pack(side="top", fill="x")

#lbl_font = Font(family="Roboto Cn", size=17) 

label1 = tk.Label(primerInicio, text="Sistema Operativo de Ecomoda", bg="medium orchid", relief="ridge", font=("Arial",16, "bold"))
label1.place(relx=0.5, rely=0.6, relwidth=1, relheight=0.6, anchor="s") 
## relwidth y relheight reciben el porcentaje de tamaño respecto al contenedor

label2 = tk.Label(primerInicio, text="Realiza un proceso de facturación, surte insumos, produce prendas, gestiona a tus empleados y revisa el estado financiero de tu empresa :)", relief="ridge")
label2.place(relx=1, rely=0.8, relwidth=1, relheight=0.4, anchor="e")

pedirFecha = tk.Frame(inicio, bg="light gray")
pedirFecha.pack(fill="both", expand=True, anchor="s")

label3 = tk.Label(
    pedirFecha, 
    text="\nPuedes hacerlo a través de la opción: Procesos y Consultas >>", 
    relief="ridge", 
    anchor="n",  # Asegura que el texto esté alineado arriba
    justify="center",  # Centra el texto horizontalmente
)
label3.place(relx=0.5, rely=0, relwidth=1, relheight=0.7, anchor="n")

logo = tk.PhotoImage(master=label3, file=f"{os.getcwd()}\\src\\uiMain\\imagenes\\logoEcomoda.png")

# Redimensionar la imagen usando subsample()
# La imagen será reducida al tamaño deseado sin recortes
logo_resized = logo.subsample(2, 2)  

# Crear el label con la imagen redimensionada
foto = tk.Label(master=label3, image=logo_resized, bg="light gray")
foto.image = logo_resized  # Mantener la referencia de la imagen
foto.place(relx=0.5, rely=0.24, anchor="n")

label4 = tk.Label(pedirFecha, text="Para iniciar ingresa la fecha de hoy ", relief="ridge", anchor="w")
label4.place(relx=0.5, rely=0.7, relwidth=1, relheight=0.3, anchor="n")
label4.config(padx=200)  

entradaDia =tk.Entry(pedirFecha, bg="plum3")
entradaDia.place(relx=0.55, rely=0.8, relwidth=0.06, relheight=0.1, anchor="n")
entradaDia.insert(0,"d/ ")
entradaMes =tk.Entry(pedirFecha, bg="plum3")
entradaMes.place(relx=0.615, rely=0.8, relwidth=0.06, relheight=0.1, anchor="n")
entradaMes.insert(0,"m/ ")
entradaAño =tk.Entry(pedirFecha, bg="plum3")
entradaAño.place(relx=0.6849, rely=0.8, relwidth=0.07, relheight=0.1, anchor="n")
entradaAño.insert(0,"a/ 20")

ventana.mainloop()