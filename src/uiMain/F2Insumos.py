import os
import tkinter as tk
from tkinter.font import Font

def surtir():
    ventana= tk.Tk()
    ventana.geometry("800x500")
    framePrincipal =  tk.Frame(ventana, bg="blue")
    framePrincipal.pack(fill="both", expand=True, padx=7, pady=7)

    frame1 = tk.Frame(framePrincipal, height=150)
    frame1.pack(side="top", fill="x")

    tituloF2 = tk.Label(frame1, text="Surtir Insumos", bg="medium orchid", relief="ridge", font=("Arial",16, "bold"))
    tituloF2.place(relx=0.5, rely=0.6, relwidth=1, relheight=0.6, anchor="s") 
    ## relwidth y relheight reciben el porcentaje de tamaño respecto al contenedor

    descripcionF2 = tk.Label(frame1, text="Registra la llegada de nuevos insumos: Incluye una predicción de ventas del siguiente mes para hacer la compra de los insumos, actualiza la deuda con los proveedores y añade los nuevos insumos a la cantidad en Stock.", relief="ridge",wraplength=600)
    descripcionF2.place(relx=1, rely=0.8, relwidth=1, relheight=0.4, anchor="e")

    frame2 = tk.Frame(framePrincipal, bg="light gray")
    frame2.pack(anchor="s",  expand=True, fill="both")

    for sede in Sede.getlistaSedes():
        pesimismo = tk.Label(frame2, text=f"Para la "{sede.getNombre()} "\nTenemos un porcentaje de pesimismo: " {str(round(Venta.getPesimismo() * 100))} "%")
        pesimismo.place(relx=1, rely=0.8, relwidth=1, relheight=0.4, anchor="e")
        criterio = "Seleccione una de las siguientes opciones:"; 
        field = fieldFrame(ventana, criterio)
        field.pack(pady=10, padx=10)
        pesimismo = tk.Label(frame2, text="1. Estoy de acuerdo con el porcentaje de pesimismo \n2. Deseo cambiar el porcentaje de pesimismo")
    

    ventana.mainloop()

surtir()