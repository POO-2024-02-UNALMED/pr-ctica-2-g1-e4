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

    descripcionF4 = tk.Label(frame1, text="Se encarga de registrar cada una de las ventas, generando la factura al cliente con los datos necesarios.", relief="ridge", font=("Arial",10), wraplength=600)
    descripcionF4.place(relx=1, rely=0.8, relwidth=1, relheight=0.4, anchor="e")

    frame2 = tk.Frame(framePrincipal)
    frame2.pack(anchor="s",  expand=True, fill="both")
    
    criterios = ["Cliente","Sede", "Asesor","Empleado Caja","Cantidad Camisas", "Cantidad Pantalones"]
    valores = ["","Sede Principal", "Si/No","","","0","0"]
    habilitado = [True, True,True,True,True,True]
    # Creamos el FieldFrame con los botones
    field_frame = FieldFrame(frame2, "Detalles Venta", criterios, "Campos", valores, habilitado)
    field_frame.place(relx=1, rely=0.5, relwidth=1, relheight=1, anchor="e")
    boton1 = tk.Button(frame2, text="Aceptar", command = lambda: Siguiente)
    boton1.place(relx=0.5, rely=0.9, relwidth=0.1, relheight=0.1, anchor="s")

def Siguiente(event):
    pass