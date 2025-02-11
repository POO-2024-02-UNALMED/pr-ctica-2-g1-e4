import os
import tkinter as tk
from tkinter.font import Font

ventana = tk.Tk()
ventana.title("Ecomoda")
ventana.geometry("800x500")

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

lbl_font = Font(family="Roboto Cn", size=14) 

label1 = tk.Label(primerInicio, text="Sistema Operativo de Ecomoda", bg="medium purple", relief="ridge", font=lbl_font)
label1.place(relx=0.5, rely=0.6, relwidth=1, relheight=0.6, anchor="s") ## relwidth: sirve para saber con respecto al frame que tan grande será

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
logo_resized = logo.subsample(2, 2)  # Ajusta los valores (3, 3) según el tamaño deseado

# Crear el label con la imagen redimensionada
foto = tk.Label(master=label3, image=logo_resized, bg="light gray")
foto.image = logo_resized  # Mantener la referencia de la imagen
foto.place(relx=0.5, rely=0.24, anchor="n")

label4 = tk.Label(pedirFecha, text="Para iniciar ingresa la fecha de hoy ", relief="ridge")
label4.place(relx=0.5, rely=0.7, relwidth=1, relheight=0.3, anchor="n")

ventana.mainloop()