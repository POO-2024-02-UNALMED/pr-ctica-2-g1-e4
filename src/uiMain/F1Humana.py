import os
import tkinter as tk
from tkinter.font import Font
from src.gestorAplicacion.administracion.empleado import Empleado
from src.uiMain import main
from src.uiMain.fieldFrame import FieldFrame
from src.gestorAplicacion.sede import Sede

class F1Humana(tk.Frame):

    def __init__(self,master):
        super().__init__(master)
        self.posiblesDespedidos=[]
        self.sede=None
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
        self.descripcionF1.grid(row=1, column=0, sticky="nswe",columnspan=4)


        infoMalos = Empleado.listaInicialDespedirEmpleado(main.Main.fecha)

        self.posiblesDespedidos = infoMalos[0]
        self.procesoListaInicial = infoMalos[1]

        self.pantallaEleccionDespedir()

    def pantallaEleccionDespedir(self, limpiarFrame=False):
        if limpiarFrame:
            self.frame1.destroy()
            self.frame1 = tk.Frame(self.framePrincipal)
            self.frame1.grid(row=1, column=0, sticky="nswe",columnspan=4)

        empleadosMalosString=""
        
        empleadosMalosString += """Estos empleados tienen un rendimiento menor al esperado, y no puedieron ser transferidos ni cambiados de cargo.\n"""

        empleadosMalosString += """Puede elegir despedir a estos empleados si lo desea, insertando SI en el campo de texto, o puede añadir mas empleados a la
    lista de despedibles"""

        self.labelPreConsulta=tk.Label(self.frame1, text=empleadosMalosString, relief="ridge", font=("Arial", 10))
        self.labelPreConsulta.grid(row=2, column=0, sticky="nswe",columnspan=4)

        nombres=[]
        for empleado in self.posiblesDespedidos:
            nombres.append(empleado.getNombre())

        self.seleccionador=FieldFrame(self.frame1, "Nombre del empleado a despedir", nombres, "¿Despedir?", ancho_entry=5, tamañoFuente=10)
        self.seleccionador.grid(row=3, column=1,columnspan=2)

        self.opcionAñadir=tk.Button(self.frame1, text="Añadir empleado a la lista de despedibles", font=("Arial", 12, "bold"), command=self.pantallaAñadirDespedido)
        self.opcionAñadir.grid(row=4, column=1,columnspan=2)
        
        self.aceptarDespedidos=tk.Button(self.frame1, text="Aceptar", font=("Arial", 12, "bold"))
        self.resetDespedidos=tk.Button(self.frame1, text="Borrar", font=("Arial", 12, "bold"), command=self.seleccionador.borrar)

        self.aceptarDespedidos.grid(row=5, column=1)
        self.resetDespedidos.grid(row=5, column=2)



        self.frame1.rowconfigure(0, weight=1)
        self.frame1.rowconfigure(1, weight=5)
        self.frame1.rowconfigure(2, weight=10)
        self.frame1.rowconfigure(3, weight=10)
        self.frame1.columnconfigure(0, weight=10)
        self.frame1.columnconfigure(1, weight=6)
        self.frame1.columnconfigure(2, weight=6)
        self.frame1.columnconfigure(3, weight=10)
        
        self.framePrincipal.columnconfigure(0, weight=1)
        self.framePrincipal.rowconfigure(0, weight=1)
    

    def pantallaAñadirDespedido(self):
        self.frame1.destroy()

        self.frame1 = tk.Frame(self.framePrincipal, height=150)
        self.frame1.grid(row=1, column=0, sticky="nswe", columnspan=2)

        self.descripcionAñadirDespedido = tk.Label(self.frame1, text="""Inserte los datos de el empleado a añadir a la lista, el panel de la derecha le ayudará, presione Enter al
terminar de escribir un valor""", relief="ridge", font=("Arial", 10))
        self.descripcionAñadirDespedido.grid(row=0, column=0, sticky="nswe", columnspan=2)

        self.datosDespedido=FieldFrame(self.frame1, "Dato del empleado" ,["sede","nombre"],"valor", ["",""],[True,False],ancho_entry=25, tamañoFuente=10)
        self.datosDespedido.configurarCallBack("sede", "<Return>", self.actualizarDatosAñadirSede)
        self.datosDespedido.grid(row=1, column=0)

        posiblesSedes="Posibles sedes:\n"

        for sede in Sede.getListaSedes():
            posiblesSedes+=sede.getNombre()+"\n"
        
        self.pistas=tk.Label(self.frame1, text=posiblesSedes, font=("Arial", 10))
        self.pistas.grid(row=1, column=1)
        self.aceptar=tk.Button(self.frame1, text="Aceptar", font=("Arial", 12, "bold"), command=self.enviarEmpleadoNuevo)
        self.botonBorrarSeleccion=tk.Button(self.frame1, text="Borrar", font=("Arial", 12, "bold"), command=self.datosDespedido.borrar)

        self.aceptar.grid(row=2, column=0)
        self.botonBorrarSeleccion.grid(row=2, column=1)
        

        self.frame1.rowconfigure(0, weight=1)
        self.frame1.rowconfigure(1, weight=10)
        self.frame1.columnconfigure(0, weight=2)
        self.frame1.columnconfigure(1, weight=1)
    
    def actualizarDatosAñadirSede(self, evento):
        if Sede.sedeExiste(self.datosDespedido.getValue("sede")):
            self.datosDespedido.habilitarEntry("nombre", True)
            self.datosDespedido.configurarCallBack("sede", "<Return>", self.actualizarDatosAñadirEmpleado)
            empleadosPosibles="Empleados posibles"
            for sede in Sede.getListaSedes():
                if sede.getNombre()==self.datosDespedido.getValue("sede"):
                    self.sede=sede
                    break
            for empleado in sede.getListaEmpleados():
                empleadosPosibles+="\n"+empleado.getNombre()
            self.pistas.config(text=empleadosPosibles)

        else:
            self.datosDespedido.habilitarEntry("sede", True)
            self.datosDespedido.habilitarEntry("nombre", False)
            tk.messageBox.showwarning("La sede no existe", "Intente otra vez.")

    def actualizarDatosAñadirEmpleado(self, evento):
        if self.sede.getEmpleado(self.datosDespedido.getValue("nombre")) is None:
            tk.messageBox.showwarning("El empleado no trabaja aquí", "Intente otra vez.")

    def enviarEmpleadoNuevo(self):
        self.posiblesDespedidos.append(self.sede.getEmpleado(self.datosDespedido.getValue("nombre")))
        self.pantallaEleccionDespedir(True)