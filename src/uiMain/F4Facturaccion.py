import os
import tkinter as tk
from tkinter.font import Font

from src.uiMain.fieldFrame import FieldFrame

def Facturar(ventana:tk.Frame):
    framePrincipal =  tk.Frame(ventana)
    framePrincipal.pack(fill="both", expand=True, padx=7, pady=7)

    frame1 = tk.Frame(framePrincipal, height=150)
    frame1.pack(side="top", fill="x")

    tituloF4 = tk.Label(frame1, text="Facturación", bg="medium orchid", relief="ridge", font=("Arial",16, "bold"))
    tituloF4.place(relx=0.5, rely=0.6, relwidth=1, relheight=0.6, anchor="s") 
    ## relwidth y relheight reciben el porcentaje de tamaño respecto al contenedor

    descripcionF4 = tk.Label(frame1, text="Se encarga de registrar cada una de las ventas, generando la factura al cliente con los datos necesarios.", relief="ridge")
    descripcionF4.place(relx=1, rely=0.8, relwidth=1, relheight=0.4, anchor="e")

    frame2 = tk.Frame(framePrincipal, bg="pink")
    frame2.pack(anchor="s",  expand=True, fill="both")
    
    criterios = ["Criterio 1", "Criterio 2"]
    valores = ["Valor 1", "Valor 2"]
    habilitado = [True, False]
    # Creamos el FieldFrame con los botones
    field_frame = FieldFrame(frame2, "Título Criterios", criterios, "Título Valores", valores, habilitado)
    field_frame.pack()