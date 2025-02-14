import os
import tkinter as tk
from tkinter.font import Font

def contratar_despedir(ventana:tk.Frame):
    framePrincipal =  tk.Frame(ventana, bg="blue")
    framePrincipal.pack(fill="both", expand=True, padx=7, pady=7)

    frame1 = tk.Frame(framePrincipal, height=150)
    frame1.pack(side="top", fill="x")

    tituloF1 = tk.Label(frame1, text="Gestión Humana", bg="medium orchid", relief="ridge", font=("Arial",16, "bold"))
    tituloF1.place(relx=0.5, rely=0.6, relwidth=1, relheight=0.6, anchor="s") 
    ## relwidth y relheight reciben el porcentaje de tamaño respecto al contenedor

    descripcionF1 = tk.Label(frame1, text="Este área analiza la lista de todos los empleados y permite modificarla:\nSe puede contratar a un nuevo empleado, establecer su salario y el rol o las funciones que cumple en la empresa.\nTambién se puede despedir a un empleado ya existente en el equipo de trabajo", relief="ridge")
    descripcionF1.place(relx=1, rely=0.8, relwidth=1, relheight=0.4, anchor="e")

    frame2 = tk.Frame(framePrincipal, bg="light gray")
    frame2.pack(anchor="s",  expand=True, fill="both")