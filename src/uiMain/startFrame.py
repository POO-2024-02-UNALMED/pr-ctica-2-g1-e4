# Dibuja la ventana y la parte externa, y la parte interna la saca de las clases F.
# O en el caso respectivo, no dibuja una funcionalidad, sino frameInicial.
import os
import tkinter as tk
from tkinter import ttk
from tkinter.font import Font
import sys
from src.gestorAplicacion.administracion.empleado import Empleado
from src.uiMain import fieldFrame
from src.uiMain.F4Facturaccion import Facturar
from src.uiMain.Excepciones.exceptionC1 import *
from src.uiMain.main import Main
from src.uiMain.F3Financiera import F3Financiera
from src.uiMain.F5Produccion import producir
from src.uiMain.fieldFrame import FieldFrame
from src.gestorAplicacion.fecha import Fecha
from src.gestorAplicacion.sede import Sede
from src.gestorAplicacion.administracion.rol import Rol
import math

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
# Inicializar pygame para el audio
#pygame.mixer.init() Función para reproducir el audio #def reproducir_audio(): #ruta_audio = os.path.join("src", "uiMain", "imagenes", "EcomodaALaOrden.mp3") #pygame.mixer.music.load(ruta_audio)  # Cambia la ruta del archivo de audio #pygame.mixer.music.play()

class startFrame(tk.Tk):
    balance_anterior=0
    diferencia_estimada=0
    analisis_futuro=0
    def __init__(self):
        self.pagina="ninguna"
        Main.estadoGestionHumana="ninguno"
        numbre = ""
        super().__init__()
        self.title("Ecomoda")
        self.geometry("800x500")
        # Llamar a la función de audio al abrir la ventana #reproducir_audio()

        self.barraMenus = tk.Menu(self)
        self.config(menu=self.barraMenus)
        self.archivoMenu = tk.Menu(self.barraMenus, tearoff=0)
        self.barraMenus.add_cascade(label="Archivo", menu=self.archivoMenu)
        self.archivoMenu.add_command(label="Salir", command = lambda : self.pasarABienvenida())
        self.procesosMenu= tk.Menu(self.barraMenus, tearoff=0)
        self.barraMenus.add_cascade(label="Procesos y Consultas", menu=self.procesosMenu)
        self.procesosMenu.add_command(label="Despedir y reemplazar empleados", command = lambda :self.abrirGestionHumana())
        self.procesosMenu.add_separator()
        self.procesosMenu.add_command(label="Pedir insumos", command = lambda : self.eliminarF2())
        self.procesosMenu.add_separator()
        self.procesosMenu.add_command(label="Ver el desglose economico de la empresa", command = lambda : self.eliminarF3())
        self.procesosMenu.add_separator()
        self.procesosMenu.add_command(label="Facturacion", command = lambda : self.eliminarF4())
        self.procesosMenu.add_separator()
        self.procesosMenu.add_command(label="Producir prendas", command= lambda : self.iniciarProduccion())

        self.ayudaMenu = tk.Menu(self.barraMenus, tearoff=0)
        self.barraMenus.add_cascade(label="Ayuda", menu=self.ayudaMenu)
        self.ayudaMenu.add_command(label="Acerca de", command= lambda : self.acercaDe())
        self.contenedorTandaTransferencia = None # Se llena al dar aceptar en la pantalla de transferir de sede en gestión humana.

        self.abrirFrameInicial()

    #----------------------------------- Listeners para el menú superior ------------------------------------------------------------------
    
    def abrirGestionHumana(self):
        self.areaPrincipal.destroy()
        self.pagina="gestionHumana"
        self.cambiarFrame(self.crearGestionHumana())
    # LINK src/uiMain/fieldFrame.py
    # ANCHOR eliminar f2

    def eliminarF2(self):
        self.Ok()
        self.pagina="insumos"
        self.areaPrincipal.destroy()
        self.cambiarFrame(self.crearInsumos())
        
    def eliminarF4(self):
        self.Ok()
        self.pagina="facturacion"
        self.areaPrincipal.destroy()
        self.cambiarFrame(self.Facturar())
        
    def eliminarF3(self):
        self.Ok()
        self.pagina="financiera"
        self.areaPrincipal.destroy()
        self.cambiarFrame(SistemaFinanciero(self))

    def iniciarProduccion(self):
        self.Ok()
        self.pagina="produccion"
        self.areaPrincipal.destroy()
        self.cambiarFrame(producir(self))
        
    def cambiarFrame(self, reemplazo:tk.Frame):
        self.areaPrincipal = reemplazo
        reemplazo.pack(fill="both", expand=True, padx=7, pady=7)
    
    def abrirFrameInicial(self):
        if self.pagina!="ninguna":
            self.areaPrincipal.destroy()
        self.pagina="inicial"
        self.cambiarFrame(self.crearFrameInicial())

    def pasarABienvenida(self):
        if self.pagina=="inicial":
            import src.uiMain.bienvenida.bienvenida as bienvenida
            self.destroy()
            bienvenida.pasarAVentanaBienvenida()
        else:
            self.abrirFrameInicial()
    
    def acercaDe(self):
        tk.messagebox.showinfo("Acerca de", "Andres David Calderón Jiménez \nGelsy Jackelin Lozano Blanquiceth \nAndrea Merino Mesa \nLuis Rincon \nJuanita Valentina Rosero")

#----------------------------------------------Frame Inicial------------------------------------------------------------------------

    def crearFrameInicial(self)->tk.Frame:
        self.frameInicial=tk.Frame(self, bg="red")
        self.createWidgetsFrameInicial()
        self.frameInicial.pack(fill="both", expand=True, padx=7, pady=7)
        return self.frameInicial

    def createWidgetsFrameInicial(self):

        #lbl_font = Font(family="Roboto Cn", size=17) 

        self.tituloFrameInicial = tk.Label(self.frameInicial, text="Sistema Operativo de Ecomoda", bg="medium orchid", relief="ridge", font=("Arial",16, "bold"))
        self.tituloFrameInicial.place(relx=0.5, rely=0, relwidth=1, relheight=0.15, anchor="n")
        ## relwidth y relheight reciben el porcentaje de tamaño respecto al contenedor

        self.descripcionFrameInicial = tk.Label(self.frameInicial, text="Realiza un proceso de facturación, surte insumos, produce prendas, gestiona a tus empleados y revisa el estado financiero de tu empresa :)", relief="ridge")
        self.descripcionFrameInicial.place(relx=0.5, rely=0.15, relwidth=1, relheight=0.1, anchor="n")

        self.contenedorFecha = tk.Frame(self.frameInicial, bg="light gray")
        self.contenedorFecha.place(relx=0.5, rely=0.25, relwidth=1, relheight=0.8, anchor="n")

        self.instruccionesFrameInicial = tk.Label(
            self.contenedorFecha, 
            text="\nPuedes hacerlo a través de la opción: <<Procesos y Consultas >>", 
            relief="ridge", 
            anchor="n",  # Asegura que el texto esté alineado arriba
            justify="center",  # Centra el texto horizontalmente
        )
        self.instruccionesFrameInicial.place(relx=0.5, rely=0, relwidth=1, relheight=0.8, anchor="n")
        self.logoEcomoda = tk.PhotoImage(master=self.instruccionesFrameInicial, file=f"{os.getcwd()}\\src\\uiMain\\imagenes\\logoEcomoda.png")

        # Redimensionar la imagen usando subsample()
        # La imagen será reducida al tamaño deseado sin recortes
        logo_resized = self.logoEcomoda.subsample(2, 2)  

        # Crear el label con la imagen redimensionada
        self.labelFotoEcomoda = tk.Label(master=self.instruccionesFrameInicial, image=logo_resized)
        self.labelFotoEcomoda.image = logo_resized  # Mantener la referencia de la imagen
        self.labelFotoEcomoda.place(relx=0.5, rely=0.1, relwidth=0.5, relheight=0.6, anchor="n")

        self.tituloFecha = tk.Label(self.contenedorFecha, text="Para iniciar ingresa la fecha de hoy ", relief="ridge", anchor="w")
        self.tituloFecha.place(relx=0.5, rely=0.7, relwidth=1, relheight=0.3, anchor="n")
        self.tituloFecha.config(padx=200)  

        self.entradaDia =tk.Entry(self.contenedorFecha, textvariable=tk.StringVar(self.contenedorFecha, value="d/ "), bg="plum3")
        self.entradaDia.place(relx=0.55, rely=0.8, relwidth=0.06, relheight=0.1, anchor="n")
        self.entradaMes =tk.Entry(self.contenedorFecha,  textvariable=tk.StringVar(self.contenedorFecha, value="m/ "), bg="plum3")
        self.entradaMes.place(relx=0.615, rely=0.8, relwidth=0.06, relheight=0.1, anchor="n")
        self.entradaAño =tk.Entry(self.contenedorFecha, textvariable=tk.StringVar(self.contenedorFecha, value="a/ "), bg="plum3")
        self.entradaAño.place(relx=0.6849, rely=0.8, relwidth=0.07, relheight=0.1, anchor="n")
        self.confirmacion = tk.Label(self.contenedorFecha, text="",  anchor="w")
        self.confirmacion.place(relx=0.5, rely=0.9, relwidth=1, relheight=0.05, anchor="n")

        self.enviarFecha=tk.Button(self.contenedorFecha,text="Enviar", command=lambda:  self.Ok())
        self.enviarFecha.place(relx=0.820, rely=0.8, relwidth=0.1, relheight=0.1, anchor="n")
        self.enviarFecha.bind("<Button-1>")
        
        self.frameInicial.rowconfigure(0, weight=1)
        self.frameInicial.rowconfigure(1, weight=3)
        self.frameInicial.rowconfigure(2, weight=3)



        # Función que se ejecutará al presionar el botón
    def Ok(self):
        if self.pagina!="inicial":
            return # Si es así, ninguno de los Widgets a tratar existen.

        # Leer los valores de las entradas
        FDia = self.entradaDia.get() # Obtener el texto de la entrada para el día
        FMes = self.entradaMes.get() # Obtener el texto de la entrada para el mes
        FAño = self.entradaAño.get() # Obtener el texto de la entrada para el año
        camposVacios = []  

        if not FDia:  
            camposVacios.append("Día")  
        if not FMes:  
            camposVacios.append("Mes")  
        if not FAño:  
            camposVacios.append("Año")  
        
        try:
            hayExcepcion = False
            if camposVacios: 
                hayExcepcion = True
            if hayExcepcion:
                raise ExcepcionContenidoVacio(camposVacios)
        except ExcepcionContenidoVacio as viejaMetida:
            messagebox.showwarning(title="Alerta",message=viejaMetida.mensaje_completo)
            return hayExcepcion
               
        self.ingresarFecha(FDia,FMes,FAño)
        if isinstance(self.ingresarFecha(FDia,FMes,FAño),Fecha):
            self.confirmacion.config(text="Fecha ingresada correctamente, estamos en "+Main.fecha.strCorto())
        pass

    def borrar(self):
        self.entradaDia.delete(0, tk.END)
        self.entradaMes.delete(0, tk.END)
        self.entradaAño.delete(0, tk.END)
        self.entradaDia.insert(0,"d/ ")
        self.entradaMes.insert(0,"m/ ")
        self.entradaAño.insert(0,"a/ ")    
        
    def ingresarFecha(self,diaI,mesI,añoI):
        fecha=None
        partes = diaI.split()
        numero=-1
            
        if partes[-1].isdigit():
            numero = int(partes[-1])
        dia = numero
        partes = mesI.split()
        if partes[-1].isdigit():
            numero = int(partes[-1])
        mes = numero
        partes = añoI.split()
        if partes[-1].isdigit():
            numero = int(partes[-1])
        año = numero

        try:
            hayExcepcion = False
            if dia <= 0 or dia > 31:
                hayExcepcion = True
                self.borrar()
            if hayExcepcion:
                raise ExcepcionEnteroNoValido(dia)
        except ExcepcionEnteroNoValido as moscaMuerta:
                messagebox.showwarning(title="Alerta", message=moscaMuerta.mensaje_completo)
                self.after(100, self.Ok) 
                return hayExcepcion
        try:
            hayExcepcion2 = False
            if mes <= 0 or mes > 12:
                hayExcepcion2 = True
                self.borrar()
            if hayExcepcion2:
                raise ExcepcionEnteroNoValido(mes)
        except ExcepcionEnteroNoValido as carrastrufia:
            messagebox.showwarning(title="Alerta", message=carrastrufia.mensaje_completo)
            self.after(100, self.Ok) 
            return hayExcepcion2
        try:
            hayExcepcion3 = False
            if año <= 0:
                hayExcepcion3 = True
                self.borrar()
            if hayExcepcion3:
                raise ExcepcionEnteroNoValido(año)
        except ExcepcionEnteroNoValido as mojarra:
            messagebox.showwarning(title="Alerta", message=mojarra.mensaje_completo)
            self.after(100, self.Ok) 
            return hayExcepcion3

        fecha = Fecha(dia, mes, año)
        Main.fecha=fecha
        self.fechaValida = True
        return fecha
    
#----------------------------------------------Gestión Humana-----------------------------------------------------------------
    def crearGestionHumana(self):
        self.gestionHumana=tk.Frame(self)
        self.posiblesDespedidos=[]
        self.sede=None
        self.inicialGestionHumana()
        self.empleadosADespedir=[] # Se llena al dar aceptar en la pantalla de seleccion.
        Main.estadoGestionHumana="despedir"
        self.cantidadADespedir=0
        return self.gestionHumana
        
    def inicialGestionHumana(self):
        self.framePrincipal =  tk.Frame(self.gestionHumana, bg="blue")
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

        if Main.fecha is not None:
            infoMalos = Main.listaInicialDespedirEmpleado()
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
        for i, empleado in enumerate(self.empleadosInsuficientes):
            nombre = tk.Label(self.frame1, text=Empleado.getNombre(empleado), font=("Arial", 10))
            area = tk.Label(self.frame1, text=Empleado.getNombre(Empleado.getAreaActual(empleado)), font=("Arial", 10))
            rendimiento = tk.Label(self.frame1, text=f"{int(self.rendimientoInsufuciencias[i])}", font=("Arial", 10))
            rendimientoDeseado = tk.Label(self.frame1, text=f"{int(Sede.getRendimientoDeseado(Empleado.getSede(empleado),Empleado.getAreaActual(empleado), Main.fecha))}", font=("Arial", 10))
            textoAccion = ""
            match self.acciones[i]:
                case "transferencia-sede":
                    textoAccion = "Transferido a otra sede"
                case "traslado-area":
                    textoAccion = "Trasladado a otra area"
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
        self.botonSeguirPreInteraccion.grid(row=row, column=0, columnspan=5)

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
        self.framePrincipal.rowconfigure(0, weight=1)
        self.framePrincipal.rowconfigure(1, weight=10)

    def pantallaEleccionDespedir(self, limpiarFrame=False):
        if limpiarFrame:
            self.frame1.destroy()
            self.frame1 = tk.Frame(self.framePrincipal)
            self.frame1.grid(row=1, column=0, sticky="nswe",columnspan=4)

        empleadosMalosString=""
        
        empleadosMalosString += """Los empleados de la derecha no rinden correctamente y no pudieron ser cambiados ni de area ni de sede. .\n"""

        empleadosMalosString += """También puede añadir a otros empleados, para buscar mas empleados, haga click en "Añadir empleado a la lista guía" """

        self.labelPreConsulta=tk.Label(self.frame1, text=empleadosMalosString, relief="ridge", font=("Arial", 10))
        self.labelPreConsulta.grid(row=1, column=0, sticky="nswe",columnspan=4)

        nombres=""
        for empleado in self.posiblesDespedidos:
            nombres+=Empleado.getNombre(empleado)+"\n"

        self.cantidadADespedir=len(self.posiblesDespedidos)

        self.seleccionadorDespedidos()

        self.malRendidos=tk.Label(self.frame1, text=nombres, font=("Arial", 10))
        self.malRendidos.grid(row=2, column=1,sticky="nswe")

        self.opcionAñadir=tk.Button(self.frame1, text="Añadir empleado a la lista guía", font=("Arial", 12, "bold"), command=self.pantallaAñadirDespedido)
        self.opcionAñadir.grid(row=3, column=0,columnspan=2)

        self.frame1.rowconfigure(0, weight=1)
        self.frame1.rowconfigure(1, weight=5)
        self.frame1.rowconfigure(2, weight=10)
        self.frame1.rowconfigure(3, weight=10)
        self.frame1.columnconfigure(0, weight=10)
        self.frame1.columnconfigure(1, weight=10)
        self.framePrincipal.columnconfigure(0, weight=1)
        self.framePrincipal.rowconfigure(0, weight=1)
        self.framePrincipal.rowconfigure(1, weight=10)
    
    def seleccionadorDespedidos(self):
        valores=[self.cantidadADespedir]
        criterios=["Cantidad de despedidos"]
        for i in range(self.cantidadADespedir):
            criterios.append(f"Nombre del despedido {i+1}")
            valores.append("")
        self.seleccionador=FieldFrame(self.frame1, "Dato", criterios, "valor",valores=valores, ancho_entry=20, tamañoFuente=10,aceptar=True, borrar=True, callbackAceptar=self.despedir)
        self.seleccionador.configurarCallBack("Cantidad de despedidos", "<Return>", lambda e:self.actualizarCantidadDespedidos())
        self.seleccionador.grid(row=2, column=0,columnspan=1)
    
    def actualizarCantidadDespedidos(self):
        self.cantidadADespedir=int(self.seleccionador.getValue("Cantidad de despedidos"))
        self.seleccionador.destroy()
        self.seleccionadorDespedidos()
    
    def despedir(self):
        self.empleadosADespedir=[]
        seleccionados=self.seleccionador.valores.copy()
        del seleccionados[0]
        for empleado in seleccionados:
            self.empleadosADespedir.append(empleado)
        existen=Main.despedirEmpleados(self.empleadosADespedir)
        if existen:
            Main.estadoGestionHumana="cambio-sede"
            self.reemplazarPorCambioSede()
        else:
            tk.messagebox.showwarning("Empleado no valido","Verifique que el empleado trabaja en la empresa.")

    # Parte de la interacción 1
    def pantallaAñadirDespedido(self):
        self.frame1.destroy()

        self.frame1 = tk.Frame(self.framePrincipal, height=150)
        self.frame1.grid(row=1, column=0, sticky="nswe")

        self.descripcionAñadirDespedido = tk.Label(self.frame1, text="""Inserte los datos de el empleado a añadir a la lista, el panel de la derecha le ayudará, presione Enter al terminar de escribir un valor""", relief="ridge", font=("Arial", 10))
        self.descripcionAñadirDespedido.grid(row=0, column=0, sticky="nswe", columnspan=4)

        self.datosDespedido=FieldFrame(self.frame1, "Dato del empleado" ,["sede","nombre"],"valor", ["",""],[True,False],ancho_entry=25, tamañoFuente=10)
        self.datosDespedido.configurarCallBack("sede", "<Return>", self.actualizarDatosAñadirSede)
        self.datosDespedido.grid(row=1, column=0, columnspan=2)

        self.pistas=tk.Label(self.frame1, text=Main.posiblesSedes(), font=("Arial", 10))
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
        if Main.verificarSedeExiste(self.datosDespedido.getValue("sede")):
            self.datosDespedido.habilitarEntry("nombre", True)
            self.datosDespedido.configurarCallBack("nombre", "<Return>", lambda e: self.actualizarDatosAñadirEmpleado())
            empleadosPosibles="Empleados posibles"
            self.sede = Main.sedePorNombre(self.datosDespedido.getValue("sede"))
            for empleado in self.sede.getListaEmpleados():
                empleadosPosibles+="\n"+empleado.getNombre()
            self.pistas.config(text=empleadosPosibles)

        else:
            self.datosDespedido.habilitarEntry("sede", True)
            self.datosDespedido.habilitarEntry("nombre", False)
            tk.messagebox.showwarning("La sede no existe", "Intente otra vez, luego de verificar el nombre de la sede")

    def actualizarDatosAñadirEmpleado(self):
        if self.sede.getEmpleado(self.datosDespedido.getValue("nombre")) is None:
            tk.messagebox.showwarning("El empleado no trabaja aquí", "Intente otra vez, luego de verificar el nombre del empleado")

    def enviarEmpleadoNuevo(self):
        if self.sede is not None and self.sede.getEmpleado(self.datosDespedido.getValue("nombre")) is not None:
            self.posiblesDespedidos.append(self.sede.getEmpleado(self.datosDespedido.getValue("nombre")))
        self.pantallaEleccionDespedir(True)

    def reemplazarPorCambioSede(self):
        self.frame1.destroy()
        self.frame1 = tk.Frame(self.framePrincipal)
        self.frame1.grid(row=1, column=0, sticky="nswe")
        self.descripcionCambioSede = tk.Label(self.frame1, text=f"""Se han despedido {len(self.empleadosADespedir)} empleados, verificamos si se pueden reemplazar
        con gente de otras sedes""", relief="ridge", font=("Arial", 10))
        self.descripcionCambioSede.grid(row=0, column=0 ,sticky="nswe")
        Main.prepararCambioSede()
        tanda = Main.getTandaReemplazo()
        if tanda is not None:
            self.dibujarTandaDeReemplazo(tanda)

        self.frame1.columnconfigure(0, weight=3)
    
    def dibujarTandaDeReemplazo(self, tanda):
        candidatos,sedeDonadora,rol,cantidad = tanda

        if self.contenedorTandaTransferencia is not None:
            self.contenedorTandaTransferencia.destroy()

        self.contenedorTandaTransferencia=tk.Frame(self.frame1)
        self.contenedorTandaTransferencia.grid(row=1, column=0, sticky="nswe")
        textoReemplazo=f"""Nececitamos reemplazar {cantidad} de {rol.name}\n"""
        if Main.estadoGestionHumana=="contratacion":
            textoReemplazo+="""Por medio de contratación"""
        else:
            textoReemplazo+=f"""Por medio de transferencia desde la sede {sedeDonadora.getNombre()}."""
        
        textoReemplazo+="""\n He aquí los candidatos, escriba el nombre del seleccionado en cada casilla:"""
        for candidato in candidatos:
            textoReemplazo+=f"\n{candidato.getNombre()} con {candidato.experiencia} años de experiencia"
            if rol==Rol.MODISTA:
                textoReemplazo+=f" y {candidato.pericia} de pericia"

        self.tituloTanda=tk.Label(self.contenedorTandaTransferencia, text=textoReemplazo, font=("Arial", 10))
        self.tituloTanda.grid(row=0, column=0, sticky="nswe", columnspan=4)

        self.seleccionadorReemplazo=FieldFrame(self.contenedorTandaTransferencia,"Reemplazo numero", [f"Reemplazo {i}" for i in range(1,cantidad+1)], "Nombre", aceptar=True, borrar=True,callbackAceptar=self.terminarTanda)
        self.seleccionadorReemplazo.grid(row=1, column=0, sticky="nswe", columnspan=4)

        self.contenedorTandaTransferencia.rowconfigure(0, weight=1)
        self.contenedorTandaTransferencia.rowconfigure(1, weight=3)
        self.contenedorTandaTransferencia.columnconfigure(0, weight=1)
    
    def terminarTanda(self):
        reemplazos=[]
        for i in range(1, len(self.seleccionadorReemplazo.valores)+1):
            reemplazos.append(self.seleccionadorReemplazo.getValue(f"Reemplazo {i}"))
        (existen)=Main.terminarTandaReemplazo(reemplazos)
        if existen:
            tanda=Main.getTandaReemplazo()
            if tanda is None:
                self.frame1.destroy()
                self.frame1 = tk.Frame(self.framePrincipal)
                self.frame1.grid(row=1, column=0, sticky="nswe")
                self.descripcionCambioSede = tk.Label(self.frame1, text=f"""Se ha completado el reemplazo de los empleados, tenga buen día.""", relief="ridge", font=("Arial", 10))
                self.descripcionCambioSede.grid(row=0, column=0 ,sticky="nswe")
                self.frame1.columnconfigure(0, weight=3)
                self.frame1.rowconfigure(0, weight=3)
            else:
                self.dibujarTandaDeReemplazo(Main.getTandaReemplazo())
        else:
            tk.messagebox.showwarning("Empleado no valido","Verifique que el empleado esta en la lista de candidatos.")

#--------------------------------------------------- Insumos -------------------------------------------------------------------

    def crearInsumos(self):
        self.insumos=tk.Frame(self)
        self.inicialInsumos()
        return self.insumos

    def inicialInsumos(self):
        from src.uiMain.main import Main
        self.framePrincipal =  tk.Frame(self.insumos)
        self.framePrincipal.pack(fill="both", expand=True, padx=7, pady=7)
        
        self.frame1 = tk.Frame(self.framePrincipal, height=150)
        self.frame1.pack(side="top", fill="x")

        self.tituloF2 = tk.Label(self.frame1, text="Surtir Insumos", bg="medium orchid", relief="ridge", font=("Arial",16, "bold"))
        self.tituloF2.place(relx=0.5, rely=0.6, relwidth=1, relheight=0.6, anchor="s") 

            ## relwidth y relheight reciben el porcentaje de tamaño respecto al contenedor
        self.descripcionF2 = tk.Label(self.frame1, text="Registra la llegada de nuevos insumos: Incluye una predicción de ventas del siguiente mes para hacer la compra de los insumos, actualiza la deuda con los proveedores y añade los nuevos insumos a la cantidad en Stock.", relief="ridge",wraplength=600)
        self.descripcionF2.place(relx=1, rely=0.8, relwidth=1, relheight=0.4, anchor="e")
        
        Main.planificarProduccion(self)

    # Interacción 1
    def pesimismo(self, c, v):
        from src.uiMain import fieldFrame
        criterios = c
        valores = v

        self.frame2 = tk.Frame(self.framePrincipal, bg="light gray")
        self.frame2.pack(anchor="s", fill="x")
            
        self.field = fieldFrame.FieldFrame(self.frame2, "\nPuede cambiar la prediccion de ventas para el siguiente mes...", criterios, "", valores, [True, True])
        self.field.pack(anchor="s",  expand=True, fill="both")

    def prediccion(self, texto):
        self.frame3 = tk.Frame(self.framePrincipal, bg="#f0f0f0")
        self.frame3.pack(anchor="s",  expand=True, fill="both",pady=5)
        prediccion = tk.Text(self.frame3, font=("Arial", 10), bg="#f0f0f0", relief="flat")
        mensaje = ""

        for caso in texto:
            mensaje += caso + "\n"
        prediccion.tag_add("center", "1.0", "end")
        prediccion.tag_config("center", justify="center")
        prediccion.insert("1.0", mensaje,"center")

        prediccion.place(relx=0.5, rely=0.5, relwidth=1, relheight=0.7,anchor="c")
        prediccion.config(state="disabled")

        label3 = tk.Label(self.frame3, text="Según dicha predicción se hará la compra de los insumos")
        label3.place(relx=0.4, rely=0.8, relwidth=1, relheight=0.1, anchor="c")    
        aceptar = tk.Button(self.frame3, text="Aceptar")
        aceptar.place(relx=0.8, rely=0.8, relwidth=0.1, relheight=0.1, anchor="c")    
            


    # Interacción 2
    


#----------------------------------------------- Sistema Financiero -------------------------------------------------------------------



#-------------------------------------------------- Facturación -------------------------------------------------------------------



    def Facturar(self):
        from src.gestorAplicacion.administracion.area import Area
        from src.gestorAplicacion.administracion.empleado import Empleado
        from src.gestorAplicacion.persona import Persona
        from src.gestorAplicacion.sede import Sede
        from src.uiMain.fieldFrame import FieldFrame
        from src.uiMain.main import Main
        
        def Interaccion1(self):
            framePrincipal =  tk.Frame(self)
            framePrincipal.pack(fill="both", expand=True, padx=7, pady=7)
            frame1 = tk.Frame(framePrincipal, height=150)
            frame1.pack(side="top", fill="x")
            tituloF4 = tk.Label(frame1, text="Facturación", bg="medium orchid", relief="ridge", font=("Arial",16, "bold"))
            tituloF4.place(relx=0.5, rely=0.6, relwidth=1, relheight=0.6, anchor="s") 
            ## relwidth y relheight reciben el porcentaje de tamaño respecto al contenedor
            descripcionF4 = tk.Label(frame1, text="Se encarga de registrar cada una de las ventas, generando la factura al cliente con los datos necesarios.", relief="ridge", font=("Arial",10), wraplength=800)
            descripcionF4.place(relx=1, rely=0.8, relwidth=1, relheight=0.4, anchor="e")
            frameGeneral= tk.Frame(framePrincipal)
            frameGeneral.pack(expand=True, fill="both")
            frame2 = tk.Frame(frameGeneral)
            frame2.place(relx=0, rely=0, relwidth=1, relheight=0.6)
            criterios = ["Cliente","Sede","Tipo de Prenda", "Cantidad Prenda"]
            valores = ["","Sede Principal","camisa/pantalon","0"]
            habilitado = [True, True,True,True]
            # Creamos el FieldFrame con los botones
            field_frame = FieldFrame(frame2, "Detalles Venta", criterios, "Campos", valores, habilitado, ancho_entry=20, crecer=False, tamañoFuente=12, aceptar=True,borrar=True, callbackAceptar=None)
            field_frame.place(relx=1, rely=0.1, relwidth=1, relheight=1, anchor="e")

            framec = tk.Frame(frameGeneral)
            framec.place(relx=0, rely=0.6, relwidth=1, relheight=0.4)
            labelCliente= tk.Frame(framec)
            labelCliente.place(relx=0, rely=0, relwidth=1, relheight=1)
            clientes=Main.imprimirNoEmpleados()
            
            tituloCliente=tk.Label(labelCliente, text="Clientes: ", font=("Arial", 12, "bold"), anchor="center")
            
            tituloCliente.grid(row=2, column=0, columnspan=3)
            contador=1
            rowbase=3
            for cliente in clientes:
                if contador<=(len(clientes)/3):
                    nombre1 = tk.Label(labelCliente, text=str(Persona.getNombre(cliente)), font=("Arial", 10))
                    nombre1.grid(row=rowbase, column=0)
                    if contador==(len(clientes)/3):
                        rowbase=3
                    else:
                        rowbase+=1
                    contador+=1
                
                elif contador<=((len(clientes)/3)*2) and contador>(len(clientes)/3):
                    nombre2 = tk.Label(labelCliente, text=str(Persona.getNombre(cliente)), font=("Arial", 10))
                    nombre2.grid(row=rowbase, column=1)
                    if contador==((len(clientes)/3)*2):
                        rowbase=3
                    else:
                        rowbase+=1
                    contador+=1
                else:
                    nombre2 = tk.Label(labelCliente, text=str(Persona.getNombre(cliente)), font=("Arial", 10))
                    nombre2.grid(row=rowbase, column=2)
                    rowbase+=1

            labelCliente.columnconfigure(0, weight=1)
            labelCliente.columnconfigure(1, weight=1)
            labelCliente.columnconfigure(2, weight=1)
            return framePrincipal

        def Siguiente(event):
            pass
        
        
        return Interaccion1(self)


#-------------------------------------------------- Producción -------------------------------------------------------------------


#----------------------------------------------Sistema Financiero------------------------------------------------------------------------

def SistemaFinanciero(self)->tk.Frame:
        from src.gestorAplicacion.administracion.banco import Banco
        from src.gestorAplicacion.administracion.deuda import Deuda
        from src.gestorAplicacion.administracion.empleado import Empleado
        from src.gestorAplicacion.administracion.evaluacionFinanciera import EvaluacionFinanciera
        from src.gestorAplicacion.venta import Venta
        from src.uiMain.fieldFrame import FieldFrame
        ventana=self      
                    
        def LeerF2(self, field_frame2, texto2):
            from src.uiMain.startFrame import startFrame
            from src.uiMain.main import Main
            Porcentaje = FieldFrame.getValue(field_frame2, "Descuento")
            
            if Porcentaje != "0% / 100%":
                Porcentaje = Porcentaje.strip("%")
                startFrame.diferencia_estimada = Main.calcularEstimado(float(Porcentaje) / 100)  # Use float to handle percentage
                texto2.config(state="normal")   # Habilitar edición
                texto2.delete("1.0", "end")     # Eliminar texto actual
                texto2.insert("1.0", "La diferencia entre ventas y deudas futuras, fue de: $"+str(startFrame.diferencia_estimada), "center")  # Insertar nuevo texto
                texto2.config(state="disabled") 
                
        def Interaccion2(self):
            frame2.destroy()
            frame3.destroy()
            
            frame4 = tk.Frame(framePrincipal)
            frame4.pack(anchor="s", expand=True, fill="both")
            
            criterios = ["Descuento"]
            valores = ["0% / 100%"]
            habilitado = [True]
            
            # Creamos el FieldFrame con los botones
            field_frame2 = FieldFrame(frame4, "Ingrese porcentaje a modificar para:", criterios, "fidelidad de los clientes sin membresía", valores, habilitado)
            field_frame2.place(relx=1, rely=0.7, relwidth=1, relheight=1, anchor="e")
            
            frame5 = tk.Frame(framePrincipal)
            frame5.pack(anchor="s", expand=True, fill="both")
            
            boton1 = tk.Button(frame5, text="Aceptar", command=lambda: LeerF2(self, field_frame2, texto2))
            boton1.place(relx=0.3, rely=0.5, relwidth=0.1, relheight=0.1, anchor="s")            
            borrar=tk.Button(frame5,text="Borrar", command = lambda: field_frame2.borrar())
            borrar.place(relx=0.5, rely=0.5, relwidth=0.1, relheight=0.1, anchor="s")
            boton2 = tk.Button(frame5, text="Siguiente", command=lambda: Interaccion3(self,frame4, frame5))
            boton2.place(relx=0.7, rely=0.5, relwidth=0.1, relheight=0.1, anchor="s")
            
            confirmacion2 = tk.Label(frame5, text="Calculando estimado entre Ventas y Deudas para ver el estado de endeudamiento de la empresa...", anchor="center")
            confirmacion2.place(relx=0, rely=0.7, relwidth=1, relheight=0.3)
            
            texto2 = tk.Text(confirmacion2, width=50, height=5, font=("Arial", 10))  # Usa valores válidos
            texto2.pack(fill="both", expand=True)
            texto2.tag_configure("center", justify="center",spacing1=10, spacing3=10)

            texto2.config(state="normal")   # Habilitar edición
            texto2.delete("1.0", "end")     # Eliminar texto actual
            texto2.insert("1.0", "Calculando estimado entre Ventas y Deudas para ver el estado de endeudamiento de la empresa...", "center")  # Insertar nuevo texto
            texto2.config(state="disabled") 

        def LeerF3(self,field_frame3, texto3):
            from src.uiMain.main import Main
            seleccion = FieldFrame.getValue(field_frame3, "Bancos")
            banco=None
            for banco_actual in Banco.getListaBancos():
                if Banco.getNombreEntidad(banco_actual) == seleccion:
                        banco = seleccion
                        break
            c = Main.planRecuperacion(startFrame.diferencia_estimada,banco)  # Use float to handle percentage  
            texto3.config(state="normal")   # Habilitar edición
            texto3.delete("1.0", "end")     # Eliminar texto actual
            texto3.insert("1.0", str(c), "center")  # Insertar nuevo texto
            texto3.config(state="disabled") 
                
            return c
            
        def listaBancos(self, frameb):
            
            bancos=Banco.getListaBancos()

            tituloNombre=tk.Label(frameb, text="Nombre", font=("Arial", 10))
            tituloDeuda=tk.Label(frameb, text="Deuda inicial", font=("Arial", 10))
            tituloAhorro=tk.Label(frameb, text="Ahorros", font=("Arial", 10))
            tituloInter=tk.Label(frameb, text="Interés", font=("Arial", 10))
            
            tituloNombre.grid(row=2, column=0)
            tituloDeuda.grid(row=2, column=1)
            tituloAhorro.grid(row=2, column=2)
            tituloInter.grid(row=2, column=3)

            for row, banco in enumerate(bancos):
                nombre = tk.Label(frameb, text=Banco.getNombreEntidad(banco), font=("Arial", 10))
                deudaInicial=0
                for deuda in Banco.getDeuda(banco):
                    deudaInicial+=Deuda.getValorInicialDeuda(deuda)
                deuda = tk.Label(frameb, text=deudaInicial, font=("Arial", 10))
                ahorro = tk.Label(frameb, text=Banco.getAhorroBanco(banco), font=("Arial", 10))
                Interes = tk.Label(frameb, text=Banco.getInteres(banco), font=("Arial", 10))
                nombre.grid(row=row+3, column=0)
                deuda.grid(row=row+3, column=1)
                ahorro.grid(row=row+3, column=2)
                Interes.grid(row=row+3, column=3)
            
            frameb.rowconfigure(0, weight=0)
            frameb.rowconfigure(1, weight=4)
            frameb.columnconfigure(0, weight=2)# Empleado insuficiente
            frameb.columnconfigure(1, weight=1)# area
            frameb.columnconfigure(2, weight=1)# rendimiento
            frameb.columnconfigure(3, weight=1)# rendimiento esperado
       
        def Interaccion3(self,frame4,frame5):
            from src.uiMain.main import Main
            frame4.destroy()
            frame5.destroy()
            frame6 = tk.Frame(framePrincipal, bg="light gray")
            frame6.pack(anchor="s",  expand=True, fill="both")
            criterios = ["Bancos"]
            valores = ["Ingrese nombre"]
            habilitado = [True]
            # Creamos el FieldFrame con los botones
            field_frame3 = FieldFrame(frame6, "Ingrese Banco para evaluar las deudas", criterios, "", valores, habilitado)
            field_frame3.place(relx=1, rely=0.5, relwidth=1, relheight=1, anchor="e")

            frameb = tk.Frame(framePrincipal)
            frameb.pack(anchor="s", expand=True, fill="both")
            labelBanco= tk.Frame(frameb)
            labelBanco.place(relx=0, rely=0, relwidth=1, relheight=1)
            listaBancos(self,labelBanco)
            
            frame7 = tk.Frame(framePrincipal)
            frame7.pack(anchor="s", expand=True, fill="both")
            boton1 = tk.Button(frame7, text="Aceptar", command=lambda: LeerF3(self, field_frame3,texto3))
            boton1.place(relx=0.3, rely=0.5, relwidth=0.1, relheight=0.2, anchor="s")            
            borrar=tk.Button(frame7,text="Borrar", command = lambda: field_frame3.borrar())
            borrar.place(relx=0.5, rely=0.5, relwidth=0.1, relheight=0.2, anchor="s")
            boton2 = tk.Button(frame7, text="Siguiente", command=lambda: Interaccion4(self, frame6, frameb, frame7))
            boton2.place(relx=0.7, rely=0.5, relwidth=0.1, relheight=0.2, anchor="s")
            
            confirmacion3 = tk.Label(frame7, text="", anchor="center")
            confirmacion3.place(relx=0, rely=0.6, relwidth=1, relheight=0.4)
            texto3 = tk.Text(confirmacion3, width=50, height=5, font=("Arial", 10))  # Usa valores válidos
            texto3.pack(fill="both", expand=True)
            texto3.tag_configure("center", justify="center",spacing1=10, spacing3=10)
            texto3.config(state="normal")   # Habilitar edición
            
            if startFrame.diferencia_estimada > 0:
                texto3.delete("1.0", "end")     # Eliminar texto actual
                texto3.insert("1.0", "El estimado es positivo, las ventas superan las deudas. Hay dinero suficiente para hacer el pago de algunas Deudas", "center")  # Insertar nuevo texto
                texto3.config(state="disabled") 
            else:
                texto3.delete("1.0", "end")     # Eliminar texto actual
                texto3.insert("1.0", "El estimado es negativo, la deuda supera las ventas. No hay Dinero suficiente para cubrir los gastos de la empresa, tendremos que pedir un préstamo", "center")  # Insertar nuevo texto
                texto3.config(state="disabled") 

        def LeerF4(self,field_frame4, texto4, descuento):
            from src.uiMain.startFrame import startFrame
            from src.uiMain.main import Main
            Porcentaje = FieldFrame.getValue(field_frame4, "Descuento entre 0% y 5%")
            
            if Porcentaje != str(descuento):
                Porcentaje = Porcentaje.strip("%")
                startFrame.analisis_futuro = Main.descuentosBlackFriday(descuento, float(Porcentaje) / 100)  # Use float to handle percentage

                texto4.config(state="normal")   # Habilitar edición
                texto4.delete("1.0", "end")     # Eliminar texto actual
                texto4.insert("1.0", "La diferencia entre ventas y deudas futuras, fue de: $"+str(startFrame.analisis_futuro), "center")  # Insertar nuevo texto
                texto4.config(state="disabled") 
        
        def Interaccion4(self,frame6,frameb, frame7):
            from src.uiMain.main import Main
            frame6.destroy()
            frameb.destroy()
            frame7.destroy()
            
            frame8 = tk.Frame(framePrincipal)
            frame8.pack(anchor="s", expand=True, fill="both")
            descuento = Venta.blackFriday(Main.fecha)
            resultado="si"
            if descuento <= 0.0:
                resultado="no"
                
            criterios = ["Descuento entre 0% y 5%"]
            valores = [str(descuento*100)]
            habilitado = [True]
            
            # Creamos el FieldFrame con los botones
            field_frame4 = FieldFrame(frame8, ("Según las Ventas anteriores, aplicar descuentos"+resultado+" funcionará"), criterios, "¿Desea Cambiar el siguiente descuento:?", valores, habilitado)
            field_frame4.place(relx=1, rely=0.7, relwidth=1, relheight=1, anchor="e")
            
            frame9 = tk.Frame(framePrincipal)
            frame9.pack(anchor="s", expand=True, fill="both")
            
            boton1 = tk.Button(frame9, text="Aceptar", command=lambda: LeerF4(self, field_frame4, texto4, descuento))
            boton1.place(relx=0.3, rely=0.5, relwidth=0.1, relheight=0.1, anchor="s")            
            borrar4=tk.Button(frame9,text="Borrar", command = lambda: field_frame4.borrar())
            borrar4.place(relx=0.5, rely=0.5, relwidth=0.1, relheight=0.1, anchor="s")
            boton2 = tk.Button(frame9, text="Siguiente", command=lambda: Interaccion5(self, frame8, frame9))
            boton2.place(relx=0.7, rely=0.5, relwidth=0.1, relheight=0.1, anchor="s")
            
            confirmacion4 = tk.Label(frame9, anchor="center")
            confirmacion4.place(relx=0, rely=0.7, relwidth=1, relheight=0.3)
            texto4 = tk.Text(confirmacion4, width=50, height=5, font=("Arial", 10))  # Usa valores válidos
            texto4.pack(fill="both", expand=True)
            texto4.tag_configure("center", justify="center",spacing1=10, spacing3=10)

            texto4.config(state="normal")   # Habilitar edición
            texto4.delete("1.0", "end")     # Eliminar texto actual
            texto4.insert("1.0", "Analizando posibilidad de hacer descuentos para subir las ventas...", "center")  # Insertar nuevo texto
            texto4.config(state="disabled") 
        
        def Interaccion5(self,frame8, frame9):
            from src.uiMain.startFrame import startFrame
            frame8.destroy()
            frame9.destroy()
            s1="Según la evaluación del estado Financiero actual: \n" +str(EvaluacionFinanciera.informe(startFrame.balance_anterior))
            s2="\n\nSe realizó un análisis sobre la posibilidad de aplicar descuentos: \n"+ str(startFrame.diferencia_estimada)
            s3="\n\nEste resultado se usó para estimar la diferencia entre ventas y deudas futuras, \nque fue de: $"+str(startFrame.analisis_futuro)
            s4= "\n y por tanto el nuevo porcentaje de pesimismo de la producción es:\n" + str(Venta.getPesimismo())+ "."        
            confirmacion5 = tk.Label(framePrincipal, anchor="center")
            confirmacion5.place(relx=0, rely=0.3, relwidth=1, relheight=0.4)
            texto5 = tk.Text(confirmacion5, width=50, height=5,bg="plum3", font=("Arial", 10))  # Usa valores válidos
            texto5.pack(fill="both", expand=True)
            texto5.tag_configure("center", justify="center",spacing1=10, spacing3=10)
            texto5.insert(1.0,s1+s2+s3+s4)
            
            boton2 = tk.Button(framePrincipal, text="Salir", bg="medium orchid",command=lambda: startFrame.abrirFrameInicial(self))
            boton2.place(relx=0.5, rely=0.9, relwidth=0.1, relheight=0.1, anchor="s")  
        
        
        def LeerF1(self):
            from src.uiMain.main import Main
            from src.uiMain.startFrame import startFrame
            eleccionDeuda=0
            resultadosP=FieldFrame.getValue(field_frame,"Proveedor")
            resultadosB=FieldFrame.getValue(field_frame,"Banco")
            if resultadosP.lower()!="si/no" and resultadosB.lower()!="si/no" and combo.get()!="":
                from src.uiMain.main import Main
                cosa=combo.get()
                if resultadosP.lower() == "si" and resultadosB.lower()=="no":
                    elecionDeuda = 1
                elif resultadosP.lower() == "no" and resultadosB.lower()=="si":
                    elecionDeuda = 2
                elif resultadosP.lower() == "si" and resultadosB.lower()=="si":
                    elecionDeuda = 3
                from src.gestorAplicacion.sede import Sede
                empleado=None
                for empleado_actual in Sede.getListaEmpleadosTotal():
                    seleccion=combo.get()
                    if Empleado.getNombre(empleado_actual) == seleccion:
                        empleado = empleado_actual
                startFrame.balance_anterior=Main.calcularBalanceAnterior(empleado,eleccionDeuda)
                
                texto.config(state="normal")   # Habilitar edición
                texto.delete("1.0", "end")     # Eliminar texto actual
                texto.insert("1.0", EvaluacionFinanciera.informe(startFrame.balance_anterior), "center")  # Insertar nuevo texto
                texto.config(state="disabled") 
            else: #Excepcion
                combo.delete(0,"end")

        def Directivos():
            from src.gestorAplicacion.administracion.area import Area
            from src.gestorAplicacion.sede import Sede
            
            elegible_empleados = []
            for empleado_actual in Sede.getListaEmpleadosTotal():
                if empleado_actual.getAreaActual() == Area.DIRECCION:
                    elegible_empleados.append(empleado_actual.getNombre())
            return elegible_empleados

        framePrincipal =  tk.Frame(ventana)
        framePrincipal.pack(fill="both", expand=True, padx=7, pady=7)
        frame1 = tk.Frame(framePrincipal, height=150)
        frame1.pack(side="top", fill="x")
        tituloF3 = tk.Label(frame1, text="Gestión Financiera", bg="medium orchid", relief="ridge", font=("Arial",16, "bold"))
        tituloF3.place(relx=0.5, rely=0.6, relwidth=1, relheight=0.6, anchor="s") 
        ## relwidth y relheight reciben el porcentaje de tamaño respecto al contenedor
        descripcionF3 = tk.Label(frame1, text="Se realiza una evaluación del estado financiero de la empresa haciendo el cálculo de los activos y los pasivos, para indicarle al usuario qué tan bien administrada está, mostrandole los resulatdos y su significado", relief="ridge", wraplength=600)
        descripcionF3.place(relx=1, rely=0.7, relwidth=1, relheight=0.4, anchor="e")
        frame2 = tk.Frame(framePrincipal)
        frame2.pack(anchor="s",  expand=True, fill="both")
        criterios = ["Proveedor", "Banco"]
        valores = ["Si/No", "Si/No"]
        habilitado = [True, True]
        # Creamos el FieldFrame con los botones
        field_frame = FieldFrame(frame2, "Desea calcular las ", criterios, "siguientes Deudas", valores, habilitado)
        field_frame.place(relx=1, rely=0.7, relwidth=1, relheight=1, anchor="e")
        frame3 = tk.Frame(framePrincipal)
        frame3.pack(anchor="s",  expand=True, fill="both")
        label7 = tk.Label(frame3, text="Directivos disponibles:",anchor="w", font=("Arial",12, "bold"))
        label7.place(relx=0.5, rely=0.6, relwidth=1, relheight=1, anchor="s")
        label7.config(padx=200)
        Lista=Directivos()
        placeholder = tk.StringVar(master=label7, value="Elije al directivo")
        combo = ttk.Combobox(master=label7,values=Lista, textvariable=placeholder,state="readonly")
        combo.place(relx=0.5, rely=0.6, relwidth=0.5, relheight=0.2, anchor="s")
        boton1 = tk.Button(frame3, text="Aceptar", command = lambda: LeerF1(self))
        boton1.place(relx=0.3, rely=0.6, relwidth=0.1, relheight=0.1, anchor="s")
        borrar=tk.Button(frame3,text="Borrar", command = lambda: field_frame.borrar())
        borrar.place(relx=0.5, rely=0.6, relwidth=0.1, relheight=0.1, anchor="s")
        boton2 = tk.Button(frame3, text="Siguiente", command = lambda: Interaccion2(self))
        boton2.place(relx=0.7, rely=0.6, relwidth=0.1, relheight=0.1, anchor="s")
        confirmacion = tk.Frame(frame3)
        confirmacion.place(relx=0, rely=0.7, relwidth=1, relheight=0.3)

        confirmacion.update_idletasks()  # Asegura que el tamaño se actualice correctamente

        texto = tk.Text(confirmacion, width=50, height=5, font=("Arial", 10))  # Usa valores válidos
        texto.pack(fill="both", expand=True)
        texto.tag_configure("center", justify="center",spacing1=10, spacing3=10)

        # Insertar el texto con el tag "center"
        texto.insert("1.0", "Calculando la diferencia entre ingresos por venta y costos de producción...", "center")

        # Deshabilitar edición si solo quieres mostrar el texto
        texto.config(state="disabled")
        return framePrincipal
    



def pasarAVentanaPrincipal():
    ventana = startFrame()
    ventana.mainloop()
    