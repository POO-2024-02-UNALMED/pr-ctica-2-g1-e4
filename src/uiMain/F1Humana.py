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


        ## relwidth y relheight reciben el porcentaje de tamaño respecto al contenedor

        self.descripcionF1 = tk.Label(self.frame1, wraplength=700 ,text="""Este área analiza la lista de todos los empleados y permite modificarla:
Se puede contratar a un nuevo empleado, establecer su salario y el rol o las funciones que cumple en la empresa.
También se puede despedir a un empleado ya existente en el equipo de trabajo.
        
Con ese fin, analizamos el rendimiento de los empleados de la empresa, y llegamos a la siguiente lista de empleados insuficientes,
estos pudieron ser cambiados de area o sede, y si estan marcados con ¿despedir?, podrá elegirlos para despedirlos en la siguiente pantalla.""".replace("\n"," "), relief="ridge", font=("Arial", 10))
        self.descripcionF1.grid(row=1, column=0, sticky="nswe",columnspan=5)

        if main.Main.fecha is not None:
            infoMalos = Empleado.listaInicialDespedirEmpleado(main.Main.fecha)
        else:
            print("Muerte a los bugs! El usuario pasó sin fecha valida")
            return

        self.posiblesDespedidos = infoMalos[0]
        self.procesoListaInicial = infoMalos[1]
        self.empleadosInsuficientes = infoMalos[2]
        self.rendimientoInsufuciencias = infoMalos[3]
        self.acciones=infoMalos[4]


        self.tituloNombre=tk.Label(self.frame1, text="Nombre", font=("Arial", 10))
        self.tituloArea=tk.Label(self.frame1, text="Area", font=("Arial", 10))
        self.tituloRendimiento=tk.Label(self.frame1, text="Rendimiento", font=("Arial", 10))
        self.tituloRendimientoEsperado=tk.Label(self.frame1, text="Rendimiento esperado", font=("Arial", 10))
        self.tituloAccion=tk.Label(self.frame1, text="Acción", font=("Arial", 10))
        
        self.tituloNombre.grid(row=2, column=0)
        self.tituloArea.grid(row=2, column=1)
        self.tituloRendimiento.grid(row=2, column=2)
        self.tituloRendimientoEsperado.grid(row=2, column=3)
        self.tituloAccion.grid(row=2, column=4)
        self.widgetsTablaInsuficientes=[]
        row=3
        for i, empleado in enumerate(self.posiblesDespedidos):
            nombre = tk.Label(self.frame1, text=empleado.getNombre(), font=("Arial", 10))
            area = tk.Label(self.frame1, text=empleado.getAreaActual().name, font=("Arial", 10))
            rendimiento = tk.Label(self.frame1, text=f"{int(self.rendimientoInsufuciencias[i])}", font=("Arial", 10))
            rendimientoDeseado = tk.Label(self.frame1, text=f"{int(empleado.sede.getRendimientoDeseado(empleado.getAreaActual(), main.Main.fecha))}", font=("Arial", 10))
            textoAccion = ""
            match self.acciones[i]:
                case "transferencia-sede":
                    textoAccion = "Transferido"
                case "traslado-area":
                    textoAccion = "Traslado"
                case "sugerencia-despido":
                    textoAccion = "¿Despedir?"

            accion = tk.Label(self.frame1, text=textoAccion, font=("Arial", 10))
            
            nombre.grid(row=row, column=0)
            area.grid(row=row, column=1)
            rendimiento.grid(row=row, column=2)
            rendimientoDeseado.grid(row=row, column=3)
            accion.grid(row=row, column=4)
            
            self.widgetsTablaInsuficientes.append((nombre, area, rendimiento, rendimientoDeseado, accion))
            row += 1
        
        self.botonSeguirPreInteraccion=tk.Button(self.frame1, text="Siguiente", font=("Arial", 12, "bold"), command=lambda : self.pantallaEleccionDespedir(True))
        self.botonSeguirPreInteraccion.grid(row=row, column=1, columnspan=2)

        self.frame1.rowconfigure(0, weight=1)
        self.frame1.rowconfigure(1, weight=10)
        self.frame1.columnconfigure(0, weight=1)# Empleado insuficiente
        self.frame1.columnconfigure(1, weight=1)# area
        self.frame1.columnconfigure(2, weight=1)# rendimiento
        self.frame1.columnconfigure(3, weight=1)# rendimiento esperado
        self.frame1.columnconfigure(4, weight=1)# acción
        for i in range(0,row):
            self.frame1.rowconfigure(i, weight=1)
        
        self.framePrincipal.columnconfigure(0, weight=1)

    



    def pantallaEleccionDespedir(self, limpiarFrame=False):
        if limpiarFrame:
            self.frame1.destroy()
            self.frame1 = tk.Frame(self.framePrincipal)
            self.frame1.grid(row=0, column=0, sticky="nswe",columnspan=4)

        empleadosMalosString=""
        
        empleadosMalosString += """Estos empleados tienen un rendimiento menor al esperado, y no puedieron ser transferidos ni cambiados de cargo.\n"""

        empleadosMalosString += """Puede elegir despedir a estos empleados si lo desea, insertando SI en el campo de texto, o puede añadir mas empleados a la
    lista de despedibles"""

        self.labelPreConsulta=tk.Label(self.frame1, text=empleadosMalosString, relief="ridge", font=("Arial", 10))
        self.labelPreConsulta.grid(row=1, column=0, sticky="nswe",columnspan=4)

        nombres=[]
        for empleado in self.posiblesDespedidos:
            nombres.append(empleado.getNombre())

        self.seleccionador=FieldFrame(self.frame1, "Nombre del empleado a despedir", nombres, "¿Despedir?", ancho_entry=5, tamañoFuente=10)
        self.seleccionador.grid(row=2, column=1,columnspan=2)

        self.opcionAñadir=tk.Button(self.frame1, text="Añadir empleado a la lista de despedibles", font=("Arial", 12, "bold"), command=self.pantallaAñadirDespedido)
        self.opcionAñadir.grid(row=3, column=1,columnspan=2)
        
        self.aceptarDespedidos=tk.Button(self.frame1, text="Aceptar", font=("Arial", 12, "bold"), command=self.despedir)
        self.resetDespedidos=tk.Button(self.frame1, text="Borrar", font=("Arial", 12, "bold"), command=self.seleccionador.borrar)

        self.aceptarDespedidos.grid(row=4, column=1)
        self.resetDespedidos.grid(row=4, column=2)



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
        self.framePrincipal.rowconfigure(1, weight=10)
    
    def despedir(self):
        empleadosADespedir=[]
        for empleado in self.posiblesDespedidos:
            if self.seleccionador.getValue(empleado.getNombre()).lower()=="si":
                empleadosADespedir.append(empleado)
        if main.Main.fecha is not None:
            Empleado.despedirEmpleados(empleadosADespedir, False, main.Main.fecha)
        else:
            print("Muerte a los bugs! El usuario pasó sin fecha valida")
    

    def pantallaAñadirDespedido(self):
        self.frame1.destroy()

        self.frame1 = tk.Frame(self.framePrincipal, height=150)
        self.frame1.grid(row=1, column=0, sticky="nswe")

        self.descripcionAñadirDespedido = tk.Label(self.frame1, text="""Inserte los datos de el empleado a añadir a la lista, el panel de la derecha le ayudará, presione Enter al
terminar de escribir un valor""", relief="ridge", font=("Arial", 10))
        self.descripcionAñadirDespedido.grid(row=0, column=0, sticky="nswe", columnspan=4)

        self.datosDespedido=FieldFrame(self.frame1, "Dato del empleado" ,["sede","nombre"],"valor", ["",""],[True,False],ancho_entry=25, tamañoFuente=10)
        self.datosDespedido.configurarCallBack("sede", "<Return>", self.actualizarDatosAñadirSede)
        self.datosDespedido.grid(row=1, column=0, columnspan=2)

        posiblesSedes="Posibles sedes:\n"

        for sede in Sede.getListaSedes():
            posiblesSedes+=sede.getNombre()+"\n"
        
        self.pistas=tk.Label(self.frame1, text=posiblesSedes, font=("Arial", 10))
        self.pistas.grid(row=1, column=3)
        self.aceptar=tk.Button(self.frame1, text="Aceptar", font=("Arial", 12, "bold"), command=self.enviarEmpleadoNuevo)
        self.botonBorrarSeleccion=tk.Button(self.frame1, text="Borrar", font=("Arial", 12, "bold"), command=self.datosDespedido.borrar)

        self.aceptar.grid(row=2, column=0)
        self.botonBorrarSeleccion.grid(row=2, column=1)
        

        self.frame1.rowconfigure(0, weight=1)
        self.frame1.rowconfigure(1, weight=10)
        self.frame1.columnconfigure(0, weight=2)
        self.frame1.columnconfigure(1, weight=2)
        self.frame1.columnconfigure(3, weight=4)

        self.framePrincipal.rowconfigure(0, weight=1)
        self.framePrincipal.rowconfigure(1, weight=10)
    
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
        if self.sede is not None and self.sede.getEmpleado(self.datosDespedido.getValue("nombre")) is not None:
            self.posiblesDespedidos.append(self.sede.getEmpleado(self.datosDespedido.getValue("nombre")))
        self.pantallaEleccionDespedir(True)