import os
import tkinter as tk
from tkinter.font import Font
from src.gestorAplicacion.administracion.empleado import Empleado
from src.uiMain import main
from src.uiMain.fieldFrame import FieldFrame

class F1Humana(tk.Frame):

    def __init__(self,master):
        super().__init__(master)
        self.posiblesDespedidos=[]
        self.createWidgets()
        

    def createWidgets(self):
        self.framePrincipal =  tk.Frame(self, bg="blue")
        self.framePrincipal.pack(fill="both", expand=True, padx=7, pady=7)

        self.tituloF1 = tk.Label(self.framePrincipal, text="Gestión Humana", bg="medium orchid", relief="ridge", font=("Arial",16, "bold"))
        self.tituloF1.grid(row=0, column=0, sticky="nswe")

        self.frame1 = tk.Frame(self.framePrincipal, height=150)
        self.frame1.grid(row=1, column=0, sticky="nswe")

        self.framePrincipal.rowconfigure(0, weight=1)
        self.framePrincipal.rowconfigure(1, weight=10)

        ## relwidth y relheight reciben el porcentaje de tamaño respecto al contenedor

        self.descripcionF1 = tk.Label(self.frame1, text="""Este área analiza la lista de todos los empleados y permite modificarla:
Se puede contratar a un nuevo empleado, establecer su salario y el rol o las funciones que cumple en la empresa.
También se puede despedir a un empleado ya existente en el equipo de trabajo""", relief="ridge", font=("Arial", 10))
        self.descripcionF1.grid(row=1, column=0, sticky="nswe")


        infoMalos = Empleado.listaInicialDespedirEmpleado(main.Main.fecha)

        self.posiblesDespedidos = infoMalos[0]
        self.procesoListaInicial = infoMalos[1]

        empleadosMalosString=""
        
        empleadosMalosString += """Estos empleados tienen un rendimiento menor al esperado, y no puedieron ser transferidos ni cambiados de cargo.\n"""

        empleadosMalosString += """Puede elegir despedir a estos empleados si lo desea, insertando SI en el campo de texto, o puede añadir mas empleados a la
    lista de despedibles"""

        self.labelPreConsulta=tk.Label(self.frame1, text=empleadosMalosString, relief="ridge", font=("Arial", 10))
        self.labelPreConsulta.grid(row=2, column=0, sticky="nswe")

        nombres=[]
        for empleado in self.posiblesDespedidos:
            nombres.append(empleado.getNombre())

        self.seleccionador=FieldFrame(self.frame1, "Nombre del empleado a despedir", nombres, "¿Despedir?", ancho_entry=5, tamañoFuente=10)
        self.seleccionador.grid(row=3, column=0)

        self.opcionAñadir=tk.Button(self.frame1, text="Añadir empleado a la lista de despedibles", font=("Arial", 12, "bold"), command=self.pantallaAñadirDespedido)
        self.opcionAñadir.grid(row=4, column=0)

        self.frame1.rowconfigure(0, weight=1)
        self.frame1.rowconfigure(1, weight=5)
        self.frame1.rowconfigure(2, weight=10)
        self.frame1.rowconfigure(3, weight=10)
        self.frame1.columnconfigure(0, weight=1)
        
        self.framePrincipal.columnconfigure(0, weight=1)
        self.framePrincipal.rowconfigure(0, weight=1)
    
    def pantallaAñadirDespedido(self):
        pass