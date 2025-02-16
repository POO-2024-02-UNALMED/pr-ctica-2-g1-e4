import os
import tkinter as tk
from tkinter.font import Font
from src.gestorAplicacion.administracion.empleado import Empleado
from src.uiMain import main
from src.uiMain.fieldFrame import FieldFrame

def contratar_despedir(ventana:tk.Frame):
    framePrincipal =  tk.Frame(ventana, bg="blue")
    framePrincipal.pack(fill="both", expand=True, padx=7, pady=7)

    frame1 = tk.Frame(framePrincipal, height=150)
    frame1.grid(row=0, column=0, sticky="nswe")

    tituloF1 = tk.Label(frame1, text="Gestión Humana", bg="medium orchid", relief="ridge", font=("Arial",16, "bold"))
    tituloF1.grid(row=0, column=0, sticky="nswe")
    ## relwidth y relheight reciben el porcentaje de tamaño respecto al contenedor

    descripcionF1 = tk.Label(frame1, text="Este área analiza la lista de todos los empleados y permite modificarla:\nSe puede contratar a un nuevo empleado, establecer su salario y el rol o las funciones que cumple en la empresa.\nTambién se puede despedir a un empleado ya existente en el equipo de trabajo", relief="ridge")
    descripcionF1.grid(row=1, column=0, sticky="nswe")


    infoMalos = Empleado.listaInicialDespedirEmpleado(main.Main.fecha)

    posiblesDespedidos = infoMalos[0]
    mensajes = infoMalos[1]

    empleadosMalosString=""

    for mensaje in mensajes:
        empleadosMalosString += mensaje + "\n"
    
    empleadosMalosString += """Estos empleados tienen un rendimiento menor al esperado, y no puedieron ser transferidos ni cambiados de cargo: \n"""

    for i in range(len(posiblesDespedidos)):
        empleadosMalosString += posiblesDespedidos[i].getNombre()+"\n"

    empleadosMalosString += """\nPuede elegir despedir a estos empleados si lo desea, insertando SI en el campo de texto, o puede añadir mas empleados a la
lista de despedibles"""

    empleadosMalRendidos=tk.Label(frame1, text=empleadosMalosString, relief="ridge")
    empleadosMalRendidos.grid(row=2, column=0, sticky="nswe")

    nombres=[]
    for empleado in posiblesDespedidos:
        nombres.append(empleado.getNombre())

    seleccionador=FieldFrame(frame1, "Nombre del empleado a despedir", nombres, "¿Despedir?")
    seleccionador.grid(row=3, column=0, sticky="nswe")

    frame1.rowconfigure(0, weight=1)
    frame1.rowconfigure(1, weight=5)
    frame1.rowconfigure(2, weight=10)
    frame1.rowconfigure(3, weight=10)
    frame1.columnconfigure(0, weight=1)
    
    framePrincipal.columnconfigure(0, weight=1)
    framePrincipal.rowconfigure(0, weight=1)
    
    return framePrincipal
