# Dibuja la ventana y la parte externa, y la parte interna la saca de las clases F.
# O en el caso respectivo, no dibuja una funcionalidad, sino frameInicial.
#region imports
import os
import tkinter as tk
from tkinter import ttk
from tkinter.font import Font
import sys
from src.gestorAplicacion.administracion.empleado import Empleado
from src.gestorAplicacion.persona import Persona
from src.uiMain import fieldFrame
from src.uiMain.Excepciones.exceptionC1 import *
from src.uiMain.Excepciones.exceptionC2 import *
from src.uiMain.main import Main
from src.uiMain.F3Financiera import F3Financiera
from src.uiMain.F5Produccion import producir
from src.uiMain.fieldFrame import FieldFrame
from src.gestorAplicacion.fecha import Fecha
from src.gestorAplicacion.sede import Sede
from src.gestorAplicacion.administracion.rol import Rol
import math
#endregion

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
# Inicializar pygame para el audio
#pygame.mixer.init() Función para reproducir el audio #def reproducir_audio(): #ruta_audio = os.path.join("src", "uiMain", "imagenes", "EcomodaALaOrden.mp3") #pygame.mixer.music.load(ruta_audio)  # Cambia la ruta del archivo de audio #pygame.mixer.music.play()


class StartFrame(tk.Tk):
    balance_anterior=0
    diferencia_estimada=0
    analisis_futuro=0
    
    def __init__(self):
        self.bolsas=0
        self.insumo=None
        self.pagina="ninguna"
        Main.estadoGestionHumana="ninguno"
        self.framePrediccion=None # Contiene los texts bajo el pesimismo. Usado en Insumos
        super().__init__()
        self.title("Ecomoda")
        self.geometry("800x500")
        self.fechaValida = False
        self.listaPrendas=[]
        self.cantidadPrendas=[]
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

    #-------------------------------------------- Listeners para el menú superior ------------------------------------------------------------------
    
    def abrirGestionHumana(self):
        if not self.fechaValida:
            return
        self.areaPrincipal.destroy()
        self.pagina="gestionHumana"
        self.cambiarFrame(self.crearGestionHumana())

    def eliminarF2(self):
        if not self.fechaValida:
            return        
        self.pagina="insumos"
        self.areaPrincipal.destroy()
        self.cambiarFrame(self.crearInsumos())
        
    def eliminarF4(self):
        if not self.fechaValida:
            return
        self.pagina="facturacion"
        self.areaPrincipal.destroy()
        self.cambiarFrame(self.Facturar())
        
    def eliminarF3(self):
        if not self.fechaValida:
            return
        self.pagina="financiera"
        self.areaPrincipal.destroy()
        self.cambiarFrame(self.SistemaFinanciero())

    def iniciarProduccion(self):
        if not self.fechaValida:
            return
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
        Main.guardar()
        if self.pagina=="inicial":
            import src.uiMain.bienvenida.bienvenida as bienvenida
            self.destroy()
            bienvenida.pasarAVentanaBienvenida()
        else:
            self.abrirFrameInicial()
        

    
    def acercaDe(self):
        tk.messagebox.showinfo("Acerca de", "Andres David Calderón Jiménez \nGelsy Jackelin Lozano Blanquiceth \nAndrea Merino Mesa \nLuis Rincon \nJuanita Valentina Rosero")
# region frame Inicial
#---------------------------------------------------------Frame Inicial------------------------------------------------------------------------

    def crearFrameInicial(self)->tk.Frame:
        self.frameInicial=tk.Frame(self)
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

        if not FDia or FDia == -1 or FDia == " ":  
            camposVacios.append("Día")  
        if not FMes or FMes == -1 or FMes == " ":  
            camposVacios.append("Mes")  
        if not FAño or FAño == -1 or FAño == " ":  
            camposVacios.append("Año")         
        try:
            hayExcepcion = False
            if camposVacios: 
    
                hayExcepcion = True
            if hayExcepcion:
                raise ExcepcionContenidoVacio(camposVacios)
        except ExcepcionContenidoVacio as viejaMetida:
            messagebox.showwarning(title="Alerta",message=viejaMetida.mensaje_completo)
            self.borrar()
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
        partesDia = diaI.split()
        partesMes = mesI.split()
        partesAño = añoI.split()
        dia = -1
        mes = -1
        año = -1
            
        if partesDia[-1].isdigit():
            dia = int(partesDia[-1])
        if partesMes[-1].isdigit():
            mes = int(partesMes[-1])
        if partesAño[-1].isdigit():
            año = int(partesAño[-1])

        try:
            hayExcepcion1 = False
            if dia <= 0 or dia > 31:
                hayExcepcion1 = True
            if hayExcepcion1:
                raise ExcepcionValorNoValido(dia)
        except ExcepcionValorNoValido as moscaMuerta:
                messagebox.showwarning(title="Alerta", message=moscaMuerta.mensaje_completo)
                self.borrar()
                return hayExcepcion1
              
        try:
            hayExcepcion2 = False
            if mes <= 0 or mes > 12:
                hayExcepcion2 = True
            if hayExcepcion2:
                raise ExcepcionValorNoValido(mes)
        except ExcepcionValorNoValido as carrastrufia:
            messagebox.showwarning(title="Alerta", message=carrastrufia.mensaje_completo)
            self.borrar()
            return hayExcepcion2

        try:
            hayExcepcion3 = False
            if año <= 0:
                hayExcepcion3 = True
            if hayExcepcion3:
                raise ExcepcionValorNoValido(año)
        except ExcepcionValorNoValido as mojarra:
            messagebox.showwarning(title="Alerta", message=mojarra.mensaje_completo)
            self.borrar()
            return hayExcepcion3
            

        fecha = Fecha(dia, mes, año)
        Main.fecha=fecha
        self.fechaValida = True
        return fecha
#endregion

# region gestion hunana
#------------------------------------------------------------------------Gestión Humana---------------------------------------------------------------------------------------------
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
        
        self.frameCambianteGHumana = tk.Frame(self.framePrincipal)
        self.frameCambianteGHumana.grid(row=1, column=0, sticky="nswe")

        ## relwidth y relheight reciben el porcentaje de tamaño respecto al contenedor
        self.descripcionF1 = tk.Label(self.frameCambianteGHumana, wraplength=700 ,text="""Este área analiza la lista de todos los empleados y permite modificarla:
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
        self.rendimientoInsuficiencias = infoMalos[3]
        self.acciones=infoMalos[4]

        self.tituloNombre=tk.Label(self.frameCambianteGHumana, text="Nombre", font=("Arial", 10))
        self.tituloArea=tk.Label(self.frameCambianteGHumana, text="Area", font=("Arial", 10))
        self.tituloRendimiento=tk.Label(self.frameCambianteGHumana, text="Rendimiento", font=("Arial", 10))
        self.tituloRendimientoEsperado=tk.Label(self.frameCambianteGHumana, text="Rendimiento esperado", font=("Arial", 10))
        self.tituloAccion=tk.Label(self.frameCambianteGHumana, text="Acción", font=("Arial", 10))
        
        self.tituloNombre.grid(row=2, column=0)
        self.tituloArea.grid(row=2, column=1)
        self.tituloRendimiento.grid(row=2, column=2)
        self.tituloRendimientoEsperado.grid(row=2, column=3)
        self.tituloAccion.grid(row=2, column=4)
        self.widgetsTablaInsuficientes=[]
        row=3
        for i, empleado in enumerate(self.empleadosInsuficientes):
            nombre = tk.Label(self.frameCambianteGHumana, text=Empleado.getNombre(empleado), font=("Arial", 10))
            area = tk.Label(self.frameCambianteGHumana, text=Empleado.getNombre(Empleado.getAreaActual(empleado)), font=("Arial", 10))
            rendimiento = tk.Label(self.frameCambianteGHumana, text=f"{int(self.rendimientoInsuficiencias[i])}", font=("Arial", 10))
            rendimientoDeseado = tk.Label(self.frameCambianteGHumana, text=f"{int(Sede.getRendimientoDeseado(Empleado.getSede(empleado),Empleado.getAreaActual(empleado), Main.fecha))}", font=("Arial", 10))
            textoAccion = ""
            match self.acciones[i]:
                case "transferencia-sede":
                    textoAccion = "Transferido a otra sede"
                case "traslado-area":
                    textoAccion = "Trasladado a otra area"
                case "sugerencia-despido":
                    textoAccion = "¿Despedir?"

            accion = tk.Label(self.frameCambianteGHumana, text=textoAccion, font=("Arial", 10))
            
            nombre.grid(row=row, column=0)
            area.grid(row=row, column=1)
            rendimiento.grid(row=row, column=2)
            rendimientoDeseado.grid(row=row, column=3)
            accion.grid(row=row, column=4)
            
            self.widgetsTablaInsuficientes.append((nombre, area, rendimiento, rendimientoDeseado, accion))
            row += 1
        
        self.botonSeguirPreInteraccion=tk.Button(self.frameCambianteGHumana, text="Siguiente", font=("Arial", 12, "bold"), command=lambda : self.pantallaEleccionDespedir(True))
        self.botonSeguirPreInteraccion.grid(row=row, column=0, columnspan=5)

        self.frameCambianteGHumana.rowconfigure(0, weight=1)
        self.frameCambianteGHumana.rowconfigure(1, weight=10)
        self.frameCambianteGHumana.columnconfigure(0, weight=1)# Empleado insuficiente
        self.frameCambianteGHumana.columnconfigure(1, weight=1)# area
        self.frameCambianteGHumana.columnconfigure(2, weight=1)# rendimiento
        self.frameCambianteGHumana.columnconfigure(3, weight=1)# rendimiento esperado
        self.frameCambianteGHumana.columnconfigure(4, weight=1)# acción
        for i in range(0,row):
            self.frameCambianteGHumana.rowconfigure(i, weight=1)
        
        self.framePrincipal.columnconfigure(0, weight=1)
        self.framePrincipal.rowconfigure(0, weight=1)
        self.framePrincipal.rowconfigure(1, weight=10)

    def pantallaEleccionDespedir(self, limpiarFrame=False):
        if limpiarFrame:
            self.frameCambianteGHumana.destroy()
            self.frameCambianteGHumana = tk.Frame(self.framePrincipal)
            self.frameCambianteGHumana.grid(row=1, column=0, sticky="nswe",columnspan=4)

        empleadosMalosString=""
        
        empleadosMalosString += """Los empleados de la derecha no rinden correctamente y no pudieron ser cambiados ni de area ni de sede. .\n"""

        empleadosMalosString += """También puede añadir a otros empleados, para buscar mas empleados, haga click en "Añadir empleado a la lista guía" \n"""

        empleadosMalosString+=Main.mensajePromedioHumanas()

        self.labelPreConsulta=tk.Label(self.frameCambianteGHumana, text=empleadosMalosString, relief="ridge", font=("Arial", 10))
        self.labelPreConsulta.grid(row=1, column=0, sticky="nswe",columnspan=4)

        nombres=""
        for empleado in self.posiblesDespedidos:
            nombres+=Empleado.getNombre(empleado)+"\n"

        self.cantidadADespedir=len(self.posiblesDespedidos)

        self.seleccionadorDespedidos()

        self.malRendidos=tk.Label(self.frameCambianteGHumana, text=nombres, font=("Arial", 10))
        self.malRendidos.grid(row=2, column=1,sticky="nswe")

        self.opcionAñadir=tk.Button(self.frameCambianteGHumana, text="Añadir empleado a la lista guía", font=("Arial", 12, "bold"), command=self.pantallaAñadirDespedido)
        self.opcionAñadir.grid(row=3, column=0,columnspan=2)

        self.frameCambianteGHumana.rowconfigure(0, weight=1)
        self.frameCambianteGHumana.rowconfigure(1, weight=5)
        self.frameCambianteGHumana.rowconfigure(2, weight=10)
        self.frameCambianteGHumana.rowconfigure(3, weight=10)
        self.frameCambianteGHumana.columnconfigure(0, weight=10)
        self.frameCambianteGHumana.columnconfigure(1, weight=10)
        self.framePrincipal.columnconfigure(0, weight=1)
        self.framePrincipal.rowconfigure(0, weight=1)
        self.framePrincipal.rowconfigure(1, weight=10)
    
    def seleccionadorDespedidos(self):
        valores=[self.cantidadADespedir]
        criterios=["Cantidad de despedidos"]
        for i in range(self.cantidadADespedir):
            criterios.append(f"Nombre del despedido {i+1}")
            valores.append("")
        self.seleccionador=FieldFrame(self.frameCambianteGHumana, "Dato", 
                                      criterios, "valor",valores=valores, ancho_entry=20, 
                                      tamañoFuente=10,aceptar=True, borrar=True, callbackAceptar=self.despedir)
        self.seleccionador.configurarCallBack("Cantidad de despedidos", "<Return>", lambda e:self.actualizarCantidadDespedidos())
        self.seleccionador.grid(row=2, column=0,columnspan=1)
    
    def actualizarCantidadDespedidos(self):
        self.cantidadADespedir=int(self.seleccionador.getValue("Cantidad de despedidos"))
        self.seleccionador.destroy()
        self.seleccionadorDespedidos()
    
    def despedir(self):
        nombresADespedir=self.seleccionador.obtenerTodosLosValores()
        del nombresADespedir[0]
        (existen,self.empleadosADespedir)=Main.despedirEmpleados(nombresADespedir)
        try:
            empleadoExcepcion = False
            if existen:
                Main.estadoGestionHumana="cambio-sede"
                self.reemplazarPorCambioSede()
                empleadoExcepcion = False
            else:
                    empleadoExcepcion = True
            if empleadoExcepcion:
                raise ExcepcionEmpleadoNoEncontrado()
        except ExcepcionEmpleadoNoEncontrado as lol:
            messagebox.showwarning(title="Alerta", message=lol.mensaje_completo)
            return empleadoExcepcion
        

    # Parte de la interacción 1
    def pantallaAñadirDespedido(self):
        self.frameCambianteGHumana.destroy()

        self.frameCambianteGHumana = tk.Frame(self.framePrincipal, height=150)
        self.frameCambianteGHumana.grid(row=1, column=0, sticky="nswe")

        self.descripcionAñadirDespedido = tk.Label(self.frameCambianteGHumana, text="""Inserte los datos de el empleado a añadir a la lista, el panel de la derecha le ayudará, presione Enter al terminar de escribir un valor""", relief="ridge", font=("Arial", 10))
        self.descripcionAñadirDespedido.grid(row=0, column=0, sticky="nswe", columnspan=4)

        self.datosDespedido=FieldFrame(self.frameCambianteGHumana, "Dato del empleado" ,["sede","nombre"],"valor", ["",""],[True,False],ancho_entry=25, tamañoFuente=10)
        self.datosDespedido.configurarCallBack("sede", "<Return>", self.actualizarDatosAñadirSede)
        self.datosDespedido.grid(row=1, column=0, columnspan=2)

        self.pistas=tk.Label(self.frameCambianteGHumana, text=Main.posiblesSedes(), font=("Arial", 10))
        self.pistas.grid(row=1, column=3)
        self.aceptar=tk.Button(self.frameCambianteGHumana, text="Aceptar", font=("Arial", 12, "bold"), command=self.enviarEmpleadoNuevo)
        self.botonBorrarSeleccion=tk.Button(self.frameCambianteGHumana, text="Borrar", font=("Arial", 12, "bold"), command=self.datosDespedido.borrar)

        self.aceptar.grid(row=2, column=0)
        self.botonBorrarSeleccion.grid(row=2, column=1)
        
        self.frameCambianteGHumana.rowconfigure(0, weight=1)
        self.frameCambianteGHumana.rowconfigure(1, weight=10)
        self.frameCambianteGHumana.columnconfigure(0, weight=2)
        self.frameCambianteGHumana.columnconfigure(1, weight=2)
        self.frameCambianteGHumana.columnconfigure(3, weight=4)
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
        self.frameCambianteGHumana.destroy()
        self.frameCambianteGHumana = tk.Frame(self.framePrincipal)
        self.frameCambianteGHumana.grid(row=1, column=0, sticky="nswe")
        self.descripcionCambioSede = tk.Label(self.frameCambianteGHumana, text=f"""Se han despedido {len(self.empleadosADespedir)} empleados, verificamos si se pueden reemplazar
        con gente de otras sedes""", relief="ridge", font=("Arial", 10))
        self.descripcionCambioSede.grid(row=0, column=0 ,sticky="nswe")
        Main.prepararCambioSede()
        tanda = Main.getTandaReemplazo()
        if tanda is not None:
            self.dibujarTandaDeReemplazo(tanda)

        self.frameCambianteGHumana.columnconfigure(0, weight=3)
    
    def dibujarTandaDeReemplazo(self, tanda):
        candidatos,sedeDonadora,rol,cantidad = tanda

        if self.contenedorTandaTransferencia is not None:
            self.contenedorTandaTransferencia.destroy()

        self.contenedorTandaTransferencia=tk.Frame(self.frameCambianteGHumana)
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
                self.frameCambianteGHumana.destroy()
                self.frameCambianteGHumana = tk.Frame(self.framePrincipal)
                self.frameCambianteGHumana.grid(row=1, column=0, sticky="nswe")
                self.descripcionCambioSede = tk.Label(self.frameCambianteGHumana, text=f"""Se ha completado el reemplazo de los empleados, tenga buen día.""", relief="ridge", font=("Arial", 10))
                self.descripcionCambioSede.grid(row=0, column=0 ,sticky="nswe")
                self.frameCambianteGHumana.columnconfigure(0, weight=3)
                self.frameCambianteGHumana.rowconfigure(0, weight=3)
            else:
                self.dibujarTandaDeReemplazo(Main.getTandaReemplazo())
        else:
            tk.messagebox.showwarning("Empleado no valido","Verifique que el empleado esta en la lista de candidatos.")
#endregion

# region insumos
#---------------------------------------------------------------- Insumos ------------------------------------------------------------------------------------------------------------------


    def crearInsumos(self):
        self.insumos=tk.Frame(self)
        self.inicialInsumos()
        return self.insumos

    def inicialInsumos(self):
        from src.uiMain.main import Main
        self.framePrincipal =  tk.Frame(self.insumos)
        self.framePrincipal.pack(fill="both", expand=True, padx=7, pady=7)

        self.tituloF2 = tk.Label(self.framePrincipal, text="Surtir Insumos", bg="medium orchid", relief="ridge", font=("Arial",16, "bold"))
        self.tituloF2.grid(row=0, column=0, sticky="nswe")

            ## relwidth y relheight reciben el porcentaje de tamaño respecto al contenedor
        self.descripcionF2 = tk.Label(self.framePrincipal, 
                            text="Registra la llegada de nuevos insumos: Incluye una predicción de ventas del siguiente mes para hacer la compra de los insumos, actualiza la deuda con los proveedores y añade los nuevos insumos a la cantidad en Stock.", 
                            relief="ridge", wraplength=600)
        self.descripcionF2.grid(row=1, column=0, sticky="nswe")

        self.pesimismo(Main.datosParaFieldPesimismo())

        self.framePrincipal.rowconfigure(0, weight=1)
        self.framePrincipal.rowconfigure(1, weight=3)
        self.framePrincipal.rowconfigure(2, weight=10)
        self.framePrincipal.columnconfigure(0, weight=1)

    # Interacción 1
    def pesimismo(self, paraField):
        from src.uiMain import fieldFrame
        (criterios, valores) = paraField
        self.frameCambianteInsumos = tk.Frame(self.framePrincipal, bg="light gray")
        self.frameCambianteInsumos.grid(row=2, column=0, sticky="nswe")
            
        self.fieldPesimismo = fieldFrame.FieldFrame(self.frameCambianteInsumos, "\nPuede cambiar la prediccion de ventas para el siguiente mes", 
                                           criterios,"El porcentaje de pesimismo es de", valores, habilitado=[True, True], ancho_entry= 10, aceptar=True, borrar=True,callbackAceptar= lambda : self.dibujarPrediccion())
        self.fieldPesimismo.grid(column=0, row=0, sticky="nswe")
        self.frameCambianteInsumos.columnconfigure(0, weight=1)
        self.frameCambianteInsumos.rowconfigure(0, weight=1)


    def dibujarPrediccion(self):
        
        pesimismos=self.fieldPesimismo.obtenerTodosLosValores()
        self.retorno = Main.planificarProduccion(pesimismos)
        self.textoPrediccion = Main.texto
        self.framePrediccion = tk.Frame(self.frameCambianteInsumos, bg="#f0f0f0")
        self.framePrediccion.grid(row=1, column=0, sticky="nswe")
        prediccion = tk.Text(self.framePrediccion, font=("Arial", 10), bg="#f0f0f0", relief="flat",height=7)
        mensaje = ""

        for caso in self.textoPrediccion:
            mensaje += caso + "\n"

        prediccion.tag_add("center", "1.0", "end")
        prediccion.tag_config("center", justify="center")
        prediccion.insert("1.0", mensaje,"center")
        prediccion.grid(row=0, column=0, sticky="nswe",columnspan=2)
        prediccion.config(state="disabled")

        label3 = tk.Label(self.framePrediccion, text="Según dicha predicción se hará la compra de los insumos")
        label3.grid(row=1, column=0, sticky="nswe")    
        aceptar = tk.Button(self.framePrediccion, text="Siguiente", command=lambda: self.pasarAInteraccion2())
        aceptar.grid(row=1, column=1, sticky="nswe")
        self.framePrediccion.rowconfigure(0, weight=1)
        self.framePrediccion.columnconfigure(0, weight=1)
        self.frameCambianteInsumos.rowconfigure(0, weight=1)
        self.frameCambianteInsumos.rowconfigure(1, weight=1)

    def pasarAInteraccion2(self):
        self.contenedorFieldTransferencia=None
        Main.prepararCoordinacionBodegas(self)
        Main.coordinarBodega()
        self.tablaInsumos(Main.infoTablaInsumos)

    def tablaInsumos(self,infoTabla):
        if self.frameCambianteInsumos is not None:
            self.frameCambianteInsumos.destroy()
        self.descripcionF2.config(text=Main.infoPostCoordinacion+"\nEsta tabla le muestra los insumos necesarios para producir, y de donde se pueden sacar.")
        
        self.frameCambianteInsumos = tk.Frame(self.framePrincipal)
        self.frameCambianteInsumos.grid(row=2, column=0, sticky="nswe")
        self.elementosTabla = []
        idxFila = 1
        encabezados=["Insumo", "Cantidad en bodega", "Cantidad necesaria", "Cantidad a conseguir", "Modo para conseguir"]
        self.encabezadosTabla = []
        for i in range(len(encabezados)):
            encabezado = tk.Label(self.frameCambianteInsumos, text=encabezados[i], font=("Arial", 10))
            self.encabezadosTabla.append(encabezado)
            encabezado.grid(row=0, column=i)
        
        for fila in infoTabla:
            for i in range(len(fila)):
                elemento=tk.Label(self.frameCambianteInsumos, text=fila[i], font=("Arial", 10))
                self.elementosTabla.append(elemento)
                elemento.grid(row=idxFila, column=i)
            self.frameCambianteInsumos.rowconfigure(idxFila, weight=1)
            idxFila += 1
        
        self.seguirDeTabla=tk.Button(self.frameCambianteInsumos, text="Elegir sobre transferencias", command=lambda: self.transferir(Main.getCriteriosCoordinarBodegas(), Main.getNombreSedeActualCoordinacion()))
        self.seguirDeTabla.grid(row=idxFila+1, column=0)
        self.frameCambianteInsumos.rowconfigure(idxFila+1, weight=1)
        self.frameCambianteInsumos.columnconfigure(0, weight=1) #insumo
        self.frameCambianteInsumos.columnconfigure(1, weight=1) # cantidad en bodega
        self.frameCambianteInsumos.columnconfigure(2, weight=1) # cantidad necesaria
        self.frameCambianteInsumos.columnconfigure(3, weight=1) # cantidad a conseguir
        self.frameCambianteInsumos.columnconfigure(4, weight=1) # modo para conseguir

    # Interacción 2
    def transferir(self, criterios, sede):
        if self.frameCambianteInsumos is not None:
            self.frameCambianteInsumos.destroy()
        self.frameCambianteInsumos = tk.Frame(self.framePrincipal)
        self.frameCambianteInsumos.grid(row=2, column=0, sticky="nswe")
        self.descripcionF2.config(text="Estos insumos no estan en esta sede, pero pueden traerse de otra o comprarse.")
        if len(criterios)>0:
            self.contenedorFieldTransferencia = tk.Frame(self.frameCambianteInsumos)
            self.contenedorFieldTransferencia.pack(anchor="s", expand=True, fill="both")

            self.fieldTransferencia = fieldFrame.FieldFrame(self.contenedorFieldTransferencia, f"\nPara la {sede} tenemos", criterios, "Desea transferir el insumo o comprarlo", ["T/C" for i in range(len(criterios))], [True for i in range(len(criterios))], 20, True, 10, callbackAceptar=lambda : self.otraSede(),aceptar=True, borrar=True)
            self.fieldTransferencia.pack(anchor="s",  expand=True, fill="both")
        else:
            self.descripcionF2.config(text="No hay insumos que se deban y puedan transferir, puedes seguir al siguiente paso.")
            self.siguiente=tk.Button(self.frameCambianteInsumos, text="Siguiente", command=self.otraSede)
            self.siguiente.pack(anchor="s", expand=True, fill="both")
            self.fieldTransferencia=None

    def otraSede(self):
        existeOtraSede=Main.siguienteSedeCoordinarBodegas(self.fieldTransferencia.obtenerTodosLosValores() if self.fieldTransferencia is not None else [])
        if existeOtraSede:
            self.criterios = Main.coordinarBodega()
            self.tablaInsumos(Main.infoTablaInsumos)
        else:
            self.frameCambianteInsumos.destroy()
            self.dibujarTablaCompraExtra(Main.comprarInsumos())
    
    def dibujarTablaCompraExtra(self, criterios)->None:
        self.frameCambianteInsumos=tk.Frame(self.framePrincipal)
        self.frameCambianteInsumos.grid(row=2, column=0, sticky="nswe")
        if len(criterios)>0:
            self.descripcionF2.config(text="Algunos proveedores a veces bajan sus precios, en tal caso, puede que quiera comprar insumos adicionales. Si es así, inserte la cantidad adicional a comprar, y aceptar para proceder con la compra.")
            self.fieldCompraExtra=fieldFrame.FieldFrame(self.frameCambianteInsumos, "Insumo", criterios=criterios, tituloValores= "Cantidad extra", valores=["0" for i in range(len(criterios))],aceptar=True, borrar=True, callbackAceptar=self.comprarExtra)
            self.fieldCompraExtra.grid(row=0, column=0, sticky="nswe")
            self.frameCambianteInsumos.rowconfigure(0, weight=1)
            self.frameCambianteInsumos.columnconfigure(0, weight=1)
        else:
            self.explicacion=tk.Label(self.frameCambianteInsumos, text="No se deben comprar insumos adicionales, los precios están estables o subiendo, ya compramos todo.", font=("Arial", 10))
            self.explicacion.grid(row=0, column=0)
            self.seguirADeudas=tk.Button(self.frameCambianteInsumos, text="Ver deudas", command=self.dibujarDeudas)
            self.seguirADeudas.grid(row=1, column=0)
            self.frameCambianteInsumos.rowconfigure(0, weight=1)
            self.frameCambianteInsumos.columnconfigure(0, weight=1)
    
    def comprarExtra(self):
        Main.terminarCompraDeInsumos(self.fieldCompraExtra.obtenerTodosLosValores())
        self.dibujarDeudas()
    
    def dibujarDeudas(self):
        self.descripcionF2.config(text="""A continuación se muestra la deuda con los proveedores, y el estado de la misma, comprar insumos aumenta la deuda.
Ya terminamos, tenga buen día.""")
        self.frameCambianteInsumos.destroy()
        self.frameCambianteInsumos = tk.Frame(self.framePrincipal)
        self.frameCambianteInsumos.grid(row=2, column=0, sticky="nswe")
        infoTablaDeudas = Main.infoTablaDeudas()
        encabezados = ["Proveedor", "Capital inicial", "Capital pagado", "Interes","Cuotas meta","¿Pagado?"]
        for i in encabezados:
            encabezado = tk.Label(self.frameCambianteInsumos, text=i, font=("Arial", 10))
            encabezado.grid(row=0, column=encabezados.index(i))
        self.frameCambianteInsumos.rowconfigure(0, weight=1)
        for fila , columnas in enumerate(infoTablaDeudas,start=1):
            for i in columnas:
                elemento = tk.Label(self.frameCambianteInsumos, text=i, font=("Arial", 10))
                elemento.grid(row=fila, column=columnas.index(i))
                self.frameCambianteInsumos.rowconfigure(fila, weight=1)
        self.frameCambianteInsumos.columnconfigure(0, weight=1)
        self.frameCambianteInsumos.columnconfigure(1, weight=1)
        self.frameCambianteInsumos.columnconfigure(2, weight=1)
        self.frameCambianteInsumos.columnconfigure(3, weight=1)
        self.frameCambianteInsumos.columnconfigure(4, weight=1)        

#endregion


#---------------------------------------------------------------------- Producción ----------------------------------------------------------------------------------------------------


#region sistema financiero
#-------------------------------------------------------------------Sistema Financiero--------------------------------------------------------------------------------------------------------

    def SistemaFinanciero(self)->tk.Frame:
            from src.gestorAplicacion.administracion.banco import Banco
            from src.gestorAplicacion.administracion.deuda import Deuda
            from src.gestorAplicacion.administracion.empleado import Empleado
            from src.gestorAplicacion.administracion.evaluacionFinanciera import EvaluacionFinanciera
            from src.gestorAplicacion.venta import Venta
            from src.uiMain.fieldFrame import FieldFrame
            ventana=self      
                        
            def LeerF2(self, field_frame2, texto2):
                from src.uiMain.startFrame import StartFrame
                from src.uiMain.main import Main
                Porcentaje = FieldFrame.getValue(field_frame2, "Fidelidad")
                
                
                try:
                    if isinstance(Porcentaje, str) and not str(Porcentaje).replace(".", "", 1).isdigit():
                      raise ExcepcionNumeroNoString(Porcentaje)
                except ExcepcionNumeroNoString as uwu:
                    messagebox.showwarning(title="Alerta", message=uwu.mensaje_completo)
                    return True 
                
                if Porcentaje != "0% / 100%":
                    Porcentaje = Porcentaje.strip("%")
                    StartFrame.diferencia_estimada = Main.calcularEstimado(float(Porcentaje) / 100)  # Use float to handle percentage
                    texto2.config(state="normal")   # Habilitar edición
                    texto2.delete("1.0", "end")     # Eliminar texto actual
                    texto2.insert("1.0", "La diferencia entre ventas y deudas futuras, fue de: $"+str(StartFrame.diferencia_estimada), "center")  # Insertar nuevo texto
                    texto2.config(state="disabled") 
                    boton2 = tk.Button(self.estimadoVentasDeudas, text="Siguiente", command=lambda: Interaccion3(self))
                    boton2.place(relx=0.7, rely=0.5, relwidth=0.1, relheight=0.1, anchor="s")

                Porcentaje = float(Porcentaje)
                try:
                    if Porcentaje < 0 or Porcentaje > 100:
                        raise ExcepcionValorNoValido(Porcentaje)
                except ExcepcionValorNoValido as pochoclo:
                    messagebox.showwarning(title="Alerta", message=pochoclo.mensaje_completo)
                    return True
                
            def Interaccion2(self):
                frame2.destroy()
                frame3.destroy()
                
                self.fidelidadclientes = tk.Frame(framePrincipal)
                self.fidelidadclientes.pack(anchor="s", expand=True, fill="both")
                
                criterios = ["Fidelidad"]
                valores = ["0% / 100%"]
                habilitado = [True]
                
                # Creamos el FieldFrame con los botones
                field_frame2 = FieldFrame(self.fidelidadclientes, "Ingrese porcentaje a modificar para", criterios, "los clientes sin membresía", valores, habilitado)
                field_frame2.place(relx=1, rely=0.7, relwidth=1, relheight=1, anchor="e")
                
                self.estimadoVentasDeudas = tk.Frame(framePrincipal)
                self.estimadoVentasDeudas.pack(anchor="s", expand=True, fill="both")
                
                boton1 = tk.Button(self.estimadoVentasDeudas, text="Aceptar", command=lambda: LeerF2(self, field_frame2, texto2))
                boton1.place(relx=0.3, rely=0.5, relwidth=0.1, relheight=0.1, anchor="s")            
                borrar=tk.Button(self.estimadoVentasDeudas,text="Borrar", command = lambda: field_frame2.borrar())
                borrar.place(relx=0.5, rely=0.5, relwidth=0.1, relheight=0.1, anchor="s")
                
                confirmacion2 = tk.Label(self.estimadoVentasDeudas, text="Calculando estimado entre Ventas y Deudas para ver el estado de endeudamiento de la empresa...", anchor="center", wraplength=600)
                confirmacion2.place(relx=0, rely=0.7, relwidth=1, relheight=0.3)
                
                texto2 = tk.Text(confirmacion2, width=50, height=5, font=("Arial", 10), bg="#f0f0f0")  # Usa valores válidos
                texto2.pack(fill="both", expand=True)
                texto2.tag_configure("center", justify="center",spacing1=10, spacing3=10)

                texto2.config(state="normal")   # Habilitar edición
                texto2.delete("1.0", "end")     # Eliminar texto actual
                texto2.insert("1.0", "Calculando estimado entre Ventas y Deudas para ver el estado de endeudamiento de la empresa...", "center")  # Insertar nuevo texto
                texto2.config(state="disabled") 

            def LeerF3(self,field_frame3, frameb):
                from src.uiMain.main import Main
                seleccion = FieldFrame.getValue(field_frame3, "Bancos")
                banco=None
                for banco_actual in Banco.getListaBancos():
                    if Banco.getNombreEntidad(banco_actual) == seleccion:
                            banco = seleccion
                            break
                if banco == None:
                    try:
                         if not isinstance(seleccion, str):
                            raise ExcepcionStringNoNumero(seleccion)
                    except ExcepcionStringNoNumero as p:
                        messagebox.showwarning(title="Alerta", message=p.mensaje_completo)
                        return True
                    else:
                        try:
                            bancos_disponibles = [Banco.getNombreEntidad(banco) for banco in Banco.getListaBancos()]
                            if seleccion not in bancos_disponibles:
                                 raise ExcepcionValorNoValido(seleccion)
                        except ExcepcionValorNoValido as ch:
                            messagebox.showwarning(title="Alerta", message = ch.mensaje_completo)
                            return True
                        
                c = Main.planRecuperacion(StartFrame.diferencia_estimada,banco)  # Use float to handle percentage  
                self.texto3.config(state="normal")   # Habilitar edición
                self.texto3.delete("1.0", "end")     # Eliminar texto actual
                self.texto3.insert("1.0", str(c), "center")  # Insertar nuevo texto
                self.texto3.config(state="disabled") 
                boton2 = tk.Button(self.botonesI3, text="Siguiente", command=lambda: Interaccion4(self, frameb))
                boton2.place(relx=0.7, rely=0.5, relwidth=0.1, relheight=0.2, anchor="s")
                    
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
        
            def Interaccion3(self):
                from src.uiMain.main import Main
                self.fidelidadclientes.destroy()
                self.estimadoVentasDeudas.destroy()
                self.bancoParaDeudas = tk.Frame(framePrincipal, bg="light gray")
                self.bancoParaDeudas.pack(anchor="s",  expand=True, fill="both")
                criterios = ["Bancos"]
                valores = ["Ingrese nombre"]
                habilitado = [True]
                # Creamos el FieldFrame con los botones
                field_frame3 = FieldFrame(self.bancoParaDeudas, "Ingrese Banco para evaluar las deudas", criterios, "", valores, habilitado)
                field_frame3.place(relx=1, rely=0.5, relwidth=1, relheight=1, anchor="e")

                frameb = tk.Frame(framePrincipal)
                frameb.pack(anchor="s", expand=True, fill="both")
                labelBanco= tk.Frame(frameb)
                labelBanco.place(relx=0, rely=0, relwidth=1, relheight=1)
                listaBancos(self,labelBanco)
                
                self.botonesI3 = tk.Frame(framePrincipal)
                self.botonesI3.pack(anchor="s", expand=True, fill="both")
                boton1 = tk.Button(self.botonesI3, text="Aceptar", command=lambda: LeerF3(self, field_frame3,frameb))
                boton1.place(relx=0.3, rely=0.5, relwidth=0.1, relheight=0.2, anchor="s")            
                borrar=tk.Button(self.botonesI3,text="Borrar", command = lambda: field_frame3.borrar())
                borrar.place(relx=0.5, rely=0.5, relwidth=0.1, relheight=0.2, anchor="s")
                
                confirmacion3 = tk.Label(self.botonesI3, text="", anchor="center",wraplength=600)
                confirmacion3.place(relx=0, rely=0.6, relwidth=1, relheight=0.4)
                self.texto3 = tk.Text(confirmacion3, width=50, height=5, font=("Arial", 10), bg="#f0f0f0")  # Usa valores válidos
                self.texto3.pack(fill="both", expand=True)
                self.texto3.tag_configure("center", justify="center",spacing1=10, spacing3=10)
                self.texto3.config(state="normal")   # Habilitar edición
                
                if StartFrame.diferencia_estimada > 0:
                    self.texto3.delete("1.0", "end")     # Eliminar texto actual
                    self.texto3.insert("1.0", "El estimado es positivo, las ventas superan las deudas. Hay dinero suficiente para hacer el pago de algunas Deudas", "center")  # Insertar nuevo texto
                    self.texto3.config(state="disabled") 
                else:
                    self.texto3.delete("1.0", "end")     # Eliminar texto actual
                    self.texto3.insert("1.0", "El estimado es negativo, la deuda supera las ventas. No hay Dinero suficiente para cubrir los gastos de la empresa, tendremos que pedir un préstamo", "center")  # Insertar nuevo texto
                    self.texto3.config(state="disabled") 

            def LeerF4(self,field_frame4, texto4, descuento):
                from src.uiMain.startFrame import StartFrame
                from src.uiMain.main import Main
                Porcentaje = FieldFrame.getValue(field_frame4, "Descuento a futuro")

                if isinstance(Porcentaje, str) and not str(Porcentaje).replace(".", "", 1).isdigit():
                    try:
                        raise ExcepcionNumeroNoString(Porcentaje)
                    except ExcepcionNumeroNoString as ask:
                        messagebox.showwarning(title="Alerta", message=ask.mensaje_completo)
                        Porcentaje.delete(0, "end")
                        return True
                                   
                if Porcentaje != str(descuento):
                    Porcentaje = Porcentaje.strip("%")
                    StartFrame.analisis_futuro = Main.descuentosBlackFriday(descuento, float(Porcentaje) / 100)  # Use float to handle percentage

                    texto4.config(state="normal")   # Habilitar edición
                    texto4.delete("1.0", "end")     # Eliminar texto actual
                    texto4.insert("1.0", "La diferencia entre ventas y deudas futuras, fue de: $"+str(StartFrame.analisis_futuro), "center")  # Insertar nuevo texto
                    texto4.config(state="disabled")
                    boton2 = tk.Button(self.botonesF4, text="Siguiente", command=lambda: Interaccion5(self))
                    boton2.place(relx=0.7, rely=0.5, relwidth=0.1, relheight=0.1, anchor="s")
            
            def Interaccion4(self,frameb):
                from src.uiMain.main import Main
                self.bancoParaDeudas.destroy()
                frameb.destroy()
                self.botonesI3.destroy()
                
                self.evBlackFriday = tk.Frame(framePrincipal)
                self.evBlackFriday.pack(anchor="s", expand=True, fill="both")
                descuento = Venta.blackFriday(Main.fecha)
                resultado="si"
                if descuento <= 0.0:
                    resultado="no"
                    
                criterios = ["Descuento a futuro"]
                valores = [str(descuento*100)]
                habilitado = [True]
                
                # Creamos el FieldFrame con los botones
                field_frame4 = FieldFrame(self.evBlackFriday, ("Según las Ventas anteriores, aplicar descuentos"+resultado+" funcionará"), criterios, "¿Desea Cambiar el siguiente descuento:?", valores, habilitado)
                field_frame4.place(relx=1, rely=0.7, relwidth=1, relheight=1, anchor="e")
                
                self.botonesF4 = tk.Frame(framePrincipal)
                self.botonesF4.pack(anchor="s", expand=True, fill="both")
                
                boton1 = tk.Button(self.botonesF4, text="Aceptar", command=lambda: LeerF4(self, field_frame4, texto4, descuento))
                boton1.place(relx=0.3, rely=0.5, relwidth=0.1, relheight=0.1, anchor="s")            
                borrar4=tk.Button(self.botonesF4,text="Borrar", command = lambda: field_frame4.borrar())
                borrar4.place(relx=0.5, rely=0.5, relwidth=0.1, relheight=0.1, anchor="s")
                
                confirmacion4 = tk.Label(self.botonesF4, anchor="center", wraplength=600)
                confirmacion4.place(relx=0, rely=0.7, relwidth=1, relheight=0.3)
                texto4 = tk.Text(confirmacion4, width=50, height=5, font=("Arial", 10), bg="#f0f0f0")  # Usa valores válidos
                texto4.pack(fill="both", expand=True)
                texto4.tag_configure("center", justify="center",spacing1=10, spacing3=10)

                texto4.config(state="normal")   # Habilitar edición
                texto4.delete("1.0", "end")     # Eliminar texto actual
                texto4.insert("1.0", "Analizando posibilidad de hacer descuentos para subir las ventas...", "center")  # Insertar nuevo texto
                texto4.config(state="disabled") 
            
            def Interaccion5(self):
                from src.uiMain.startFrame import StartFrame
                self.evBlackFriday.destroy()
                self.botonesF4.destroy()
                s1="Según la evaluación del estado Financiero actual: \n" +str(EvaluacionFinanciera.informe(StartFrame.balance_anterior))
                s2="\n\nSe realizó un análisis sobre la posibilidad de aplicar descuentos: \n"+ str(StartFrame.diferencia_estimada)
                s3="\n\nEste resultado se usó para estimar la diferencia entre ventas y deudas futuras, \nque fue de: $"+str(self.diferencia_estimada)+"\n"+str(StartFrame.analisis_futuro)
                s4= "\n y por tanto el nuevo porcentaje de pesimismo de la producción es:\n" + str(Venta.getPesimismo())+ "."        
                confirmacion5 = tk.Label(framePrincipal, anchor="center", wraplength=600)
                confirmacion5.place(relx=0, rely=0.3, relwidth=1, relheight=0.4)
                texto5 = tk.Text(confirmacion5, width=50, height=5,bg="plum3", font=("Arial", 10))  # Usa valores válidos
                texto5.pack(fill="both", expand=True)
                texto5.tag_configure("center", justify="center",spacing1=10, spacing3=10)
                texto5.insert(1.0,s1+s2+s3+s4)
                
                boton2 = tk.Button(framePrincipal, text="Salir", bg="medium orchid",command=lambda: StartFrame.abrirFrameInicial(self))
                boton2.place(relx=0.5, rely=0.9, relwidth=0.1, relheight=0.1, anchor="s")  
            
            
            def LeerF1(self):
                from src.uiMain.main import Main
                from src.uiMain.startFrame import StartFrame
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
                    StartFrame.balance_anterior=Main.calcularBalanceAnterior(empleado,eleccionDeuda)
                   
                    texto.config(state="normal")   # Habilitar edición
                    texto.delete("1.0", "end")     # Eliminar texto actual
                    texto.insert("1.0", EvaluacionFinanciera.informe(StartFrame.balance_anterior), "center")  # Insertar nuevo texto
                    texto.config(state="disabled") 
                    boton2 = tk.Button(frame3, text="Siguiente", command = lambda: Interaccion2(self))
                    boton2.place(relx=0.7, rely=0.6, relwidth=0.1, relheight=0.1, anchor="s")
                else: #Excepcion
                    combo.delete(0,"end")
                try:
                    error = []
                    if not isinstance(resultadosP, str):
                        error.append(resultadosP)
                    if not isinstance(resultadosB, str):
                        error.append(resultadosB)
                    if error != []:
                        raise ExcepcionStringNoNumero(error)
                except ExcepcionStringNoNumero as obleas:
                    messagebox.showwarning(title="Alerta", message=obleas.mensaje_completo)
                try:
                    if resultadosP.lower() not in ["si", "no"] or resultadosB.lower() not in ["si", "no"]:
                        raise ExcepcionValorNoValido(resultadosP.lower())
                except ExcepcionValorNoValido as cornal:
                    messagebox.showwarning(title="Alerta", message=cornal.mensaje_completo)
                    return True

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
            Lista=Main.Directivos()
            placeholder = tk.StringVar(master=label7, value="Elije al directivo")
            combo = ttk.Combobox(master=label7,values=Lista, textvariable=placeholder,state="readonly")
            combo.place(relx=0.5, rely=0.6, relwidth=0.5, relheight=0.2, anchor="s")
            boton1 = tk.Button(frame3, text="Aceptar", command = lambda: LeerF1(self))
            boton1.place(relx=0.3, rely=0.6, relwidth=0.1, relheight=0.1, anchor="s")
            borrar=tk.Button(frame3,text="Borrar", command = lambda: field_frame.borrar())
            borrar.place(relx=0.5, rely=0.6, relwidth=0.1, relheight=0.1, anchor="s")
            confirmacion = tk.Frame(frame3)
            confirmacion.place(relx=0, rely=0.7, relwidth=1, relheight=0.3)
            espacio=tk.Label(confirmacion, text="", font=("Arial", 10), wraplength=600)
            espacio.place(relx=0, rely=0, relwidth=1, relheight=1, anchor="c")
            confirmacion.update_idletasks()  # Asegura que el tamaño se actualice correctamente

            texto = tk.Text(confirmacion, width=50, height=5, font=("Arial", 10), bg="#f0f0f0")  # Usa valores válidos
            texto.pack(fill="both", expand=True)
            texto.tag_configure("center", justify="center",spacing1=10, spacing3=10)

            # Insertar el texto con el tag "center"
            texto.insert("1.0", "Calculando la diferencia entre ingresos por venta y costos de producción...", "center")

            # Deshabilitar edición si solo quieres mostrar el texto
            texto.config(state="disabled")
            return framePrincipal
    #endregion
    #region facturacion
#--------------------------------------------------------- Facturación ----------------------------------------------------------------------------------------------------------------------------------
    
    def Facturar(self):
        self.Facturacion=tk.Frame(self)
        self.sede=None
        self.inicialFacturacion()
        self.cantidadADespedir=0
        return self.Facturacion
        
    def inicialFacturacion(self):
        self.dineroTransferido=False
        self.framePrincipal =  tk.Frame(self.Facturacion)
        self.framePrincipal.pack(fill="both", expand=True, padx=7, pady=7)

        self.tituloF1 = tk.Label(self.framePrincipal, text="Facturacion", bg="medium orchid", relief="ridge", font=("Arial",16, "bold"))
        self.tituloF1.grid(row=0, column=0, sticky="nswe")
        
        ## relwidth y relheight reciben el porcentaje de tamaño respecto al contenedor
        self.descripcionF1 = tk.Label(self.framePrincipal, wraplength=700 ,text="Se encarga de registrar cada una de las ventas, generando la factura al cliente con los datos necesarios.", relief="ridge", font=("Arial", 10))
        self.descripcionF1.grid(row=1, column=0, sticky="nswe")        
        
        self.freameCambianteFacturacion = tk.Frame(self.framePrincipal)
        self.freameCambianteFacturacion.grid(row=2, column=0, sticky="nswe")

        self.outputFacturacion=tk.Text(master=self.framePrincipal,state="disabled", font=("Arial", 10),height=2, bg="#f0f0f0")
        self.outputFacturacion.grid(row=3, column=0, sticky="nswe")
        
        self.framePrincipal.columnconfigure(0, weight=1)
        self.framePrincipal.rowconfigure(0, weight=1)
        self.framePrincipal.rowconfigure(1, weight=1)
        self.framePrincipal.rowconfigure(2, weight=10)
        self.framePrincipal.rowconfigure(3, weight=2)
        self.interaccion1Facturacion()

    #Este si
    # Parte de la interacción 1
    def interaccion1Facturacion(self):
        self.descripcionF1.config(text="""Se encarga de registrar cada una de las ventas, generando la factura al cliente con los datos necesarios.\nInserte los datos de la sede y presione Enter para ver los empleados""")
        self.freameCambianteFacturacion.destroy()

        self.freameCambianteFacturacion = tk.Frame(self.framePrincipal, height=150)
        self.freameCambianteFacturacion.grid(row=2, column=0, sticky="nswe")

        self.datosEntradasFacturacion=FieldFrame(self.freameCambianteFacturacion, "Detalles Venta" ,
        ["Cliente","sede", "Vendedor","Empleado caja","Prenda", "Cantidad"],"valor", ["","Sede Principal", "",
        "","Camisa/Pantalon","0"],[True,True,False,False,True,True],ancho_entry=25, tamañoFuente=10)
        self.datosEntradasFacturacion.configurarCallBack("sede", "<Return>", self.actualizarDatosEmpleadosFacturacion)
        self.datosEntradasFacturacion.grid(row=1, column=0, columnspan=2)
        clientesPosibles="Clientes"
        self.Clientes=tk.Label(self.freameCambianteFacturacion, text=clientesPosibles, font=("Arial", 10))
        self.Clientes.grid(row=1, column=3)
        clientes= Main.imprimirNoEmpleados()
        for cliente in clientes:
            if isinstance(cliente,Persona):
                clientesPosibles+="\n"+cliente.getNombre()        
        self.Clientes.config(text=clientesPosibles)
        self.pistas=tk.Label(self.freameCambianteFacturacion, text=Main.posiblesSedes(), font=("Arial", 10))
        self.pistas.grid(row=1, column=4)
        self.aceptar=tk.Button(self.freameCambianteFacturacion, text="Aceptar", font=("Arial", 10, "bold"), command=self.leer1Facturacion)
        self.botonBorrarSeleccion=tk.Button(self.freameCambianteFacturacion, text="Borrar", font=("Arial", 10, "bold"), command=self.datosEntradasFacturacion.borrar)

        self.aceptar.grid(row=2, column=0)
        self.botonBorrarSeleccion.grid(row=2, column=1)
        
        self.freameCambianteFacturacion.rowconfigure(0, weight=1)
        self.freameCambianteFacturacion.rowconfigure(1, weight=10)
        self.freameCambianteFacturacion.columnconfigure(0, weight=2)
        self.freameCambianteFacturacion.columnconfigure(1, weight=2)
        self.freameCambianteFacturacion.columnconfigure(3, weight=3)
        self.freameCambianteFacturacion.columnconfigure(4, weight=3)
        self.framePrincipal.rowconfigure(0, weight=1)
        self.framePrincipal.rowconfigure(1, weight=10)
        
    def interaccion6Facturacion(self, mensaje):
        self.cantidadBolsaGrande=0
        self.cantidadBolsaMediana=0
        self.cantidadBolsaPequeña=0
        self.descripcionF1.config(text="""Factura de la compra realizada.""")
        self.freameCambianteFacturacion.destroy()
        self.outputFacturacion.destroy()
        self.freameCambianteFacturacion = tk.Frame(self.framePrincipal, height=150)
        self.freameCambianteFacturacion.grid(row=2, column=0, sticky="nswe")

        confirmacion=tk.Label(self.freameCambianteFacturacion, anchor="center")
        confirmacion.grid(row=0, column=0, sticky="nswe")
        self.impresionFinal= tk.Text(confirmacion, font=("Arial", 10), height=10,bg="plum3")
        self.impresionFinal.pack(fill="both", expand=True)
        self.impresionFinal.tag_configure("center", justify="center",spacing1=10, spacing3=10)
        self.impresionFinal.insert(1.0,mensaje)
        
        self.siguiente=tk.Button(self.frameCambianteGHumana, text="Salir", bg="medium orchid",command=lambda: StartFrame.abrirFrameInicial(self))
        self.siguiente.grid(row=1, column=0)       
          
        self.freameCambianteFacturacion.rowconfigure(0, weight=10)
        self.freameCambianteFacturacion.rowconfigure(1, weight=2)       
        self.freameCambianteFacturacion.columnconfigure(0, weight=10)      
        self.framePrincipal.rowconfigure(0, weight=1)
        self.framePrincipal.rowconfigure(1, weight=1)
        self.framePrincipal.rowconfigure(2, weight=10)


    def interaccion5Facturacion(self):
        self.cantidadBolsaGrande=0
        self.cantidadBolsaMediana=0
        self.cantidadBolsaPequeña=0
        self.descripcionF1.config(text="""Se encarga de tranferir los fondos a la cuenta principal.""")
        self.freameCambianteFacturacion.destroy()
        self.outputFacturacion.config(state="normal")
        self.outputFacturacion.delete("1.0", "end")
        self.outputFacturacion.config(state="disabled")

        self.freameCambianteFacturacion = tk.Frame(self.framePrincipal, height=150)
        self.freameCambianteFacturacion.grid(row=2, column=0, sticky="nswe")
        
        self.datosEntradasFacturacion=FieldFrame(self.freameCambianteFacturacion, "Fondos" ,["Transferir fondos a la cuenta principal","¿Qué porcentaje desea transferir?"],"", ["Si/No","20% o 60%"],[True,False],ancho_entry=25, tamañoFuente=10)
        self.datosEntradasFacturacion.configurarCallBack("Transferir fondos a la cuenta principal", "<Return>", self.transferirDinero)
        self.datosEntradasFacturacion.grid(row=1, column=0, columnspan=2)
        
        self.aceptar=tk.Button(self.freameCambianteFacturacion, text="Aceptar", font=("Arial", 10,  "bold"), command=self.leer5Facturacion)
        self.botonBorrarSeleccion=tk.Button(self.freameCambianteFacturacion, text="Borrar", font=("Arial", 10,  "bold"), command=self.datosEntradasFacturacion.borrar)

        self.aceptar.grid(row=2, column=0)
        self.botonBorrarSeleccion.grid(row=2, column=1)        
        
        self.freameCambianteFacturacion.rowconfigure(0, weight=1)
        self.freameCambianteFacturacion.rowconfigure(1, weight=10)
        self.freameCambianteFacturacion.columnconfigure(0, weight=2)
        self.freameCambianteFacturacion.columnconfigure(1, weight=2)
        self.freameCambianteFacturacion.columnconfigure(3, weight=2)
        self.framePrincipal.rowconfigure(0, weight=1)
        self.framePrincipal.rowconfigure(1, weight=1)

    def transferirDinero(self, evento):
        self.dineroTransferido=True
        if (self.datosEntradasFacturacion.getValue("Transferir fondos a la cuenta principal").lower())=="si":
            self.datosEntradasFacturacion.habilitarEntry("¿Qué porcentaje desea transferir?", True)
        else:
            valor = (self.datosEntradasFacturacion.getValue("Transferir fondos a la cuenta principal").lower())
            try: 
                if not isinstance(valor, str):
                    raise ExcepcionStringNoNumero((self.datosEntradasFacturacion.getValue("Transferir fondos a la cuenta principal")))
            except ExcepcionPrendaNoExistente as guegue:
                messagebox.showwarning(title="Alerta", message=guegue.mensaje_completo)
                return True
            else:
                try:
                    if valor not in ["si", "no"]:
                        raise ExcepcionValorNoValido((self.datosEntradasFacturacion.getValue("Transferir fondos a la cuenta principal").lower()))
                except ExcepcionValorNoValido as cacahuate:
                    messagebox.showwarning(title="Alerta", message=cacahuate.mensaje_completo)
                    return True

    def leer5Facturacion(self):
        porcentaje=0
        mensaje=""
        if isinstance(self.datosEntradasFacturacion.getValue("¿Qué porcentaje desea transferir?"),str):
            try:
                raise ExcepcionNumeroNoString(self.datosEntradasFacturacion.getValue("¿Qué porcentaje desea transferir?"))
            except ExcepcionNumeroNoString as b:
                messagebox.showwarning(title="Alerta", message=b.mensaje_completo)
                return True
        elif self.datosEntradasFacturacion.getValue("¿Qué porcentaje desea transferir?") != "":
            if  self.datosEntradasFacturacion.getValue("¿Qué porcentaje desea transferir?").strip("%") < 0:
                try:
                    raise ExcepcionValorNoValido(self.datosEntradasFacturacion.getValue("¿Qué porcentaje desea transferir?"))  
                except ExcepcionValorNoValido as mon:
                    messagebox.showwarning(title="Alerta", message=mon.mensaje_completo)
                    return True

        else:
            if self.datosEntradasFacturacion.getValue("¿Qué porcentaje desea transferir?")!=None and self.datosEntradasFacturacion.getValue("Transferir fondos a la cuenta principal")!=None:
                string=self.datosEntradasFacturacion.getValue("¿Qué porcentaje desea transferir?").strip("%")
                if string.isnumeric():
                    porcentaje=int(string)
                if self.datosEntradasFacturacion.getValue("Transferir fondos a la cuenta principal").lower()=="si" or self.datosEntradasFacturacion.getValue("Transferir fondos a la cuenta principal").lower()=="no":
                    if self.datosEntradasFacturacion.getValue("Transferir fondos a la cuenta principal").lower()=="si" and porcentaje>=20 and porcentaje <=60:
                        mensajeFinal,mensaje=Main.ingresoEmpresa(self.venta, self.datosEntradasFacturacion.getValue("Transferir fondos a la cuenta principal").lower(), porcentaje)
                    else:
                        mensajeFinal=Main.ingresoEmpresa(self.venta, self.datosEntradasFacturacion.getValue("Transferir fondos a la cuenta principal").lower(), 0)
                        mensaje="No se transfirió el dinero a la cuenta principal."
                    self.siguiente=tk.Button(self.freameCambianteFacturacion, text="Siguiente", font=("Arial", 10, "bold"), command=lambda:self.interaccion6Facturacion(mensajeFinal))
                    self.siguiente.grid(row=2, column=3)   
                self.outputFacturacion.config(state="normal")
                self.outputFacturacion.delete("1.0", "end")
                self.outputFacturacion.insert("1.0",mensaje)
                self.outputFacturacion.config(state="disabled")    

    def interaccion4Facturacion(self):
        self.cantidadBolsaGrande=0
        self.cantidadBolsaMediana=0
        self.cantidadBolsaPequeña=0
        self.descripcionF1.config(text="""Se esncarga de Redimir y/o comprar tarjetas de regalo. \nIngrese -1 si no desea redimir ninguna tarjeta y No si no desea cmprar.""")
        self.freameCambianteFacturacion.destroy()
        self.outputFacturacion.config(state="normal")
        self.outputFacturacion.delete("1.0", "end")
        self.outputFacturacion.config(state="disabled")

        self.freameCambianteFacturacion = tk.Frame(self.framePrincipal, height=150)
        self.freameCambianteFacturacion.grid(row=2, column=0, sticky="nswe")
        
        self.datosEntradasFacturacion=FieldFrame(self.freameCambianteFacturacion, "Targeta de regalo" ,["Código","Nueva tarjeta","Monto nueva Tarjeta"],"", ["-1","Si/No","100000"],[True, True,True],ancho_entry=25, tamañoFuente=10, aceptar=True,borrar=True,callbackAceptar= self.leer4Facturacion)
        self.datosEntradasFacturacion.grid(row=1, column=0, columnspan=2)     
        
        self.freameCambianteFacturacion.rowconfigure(0, weight=1)
        self.freameCambianteFacturacion.rowconfigure(1, weight=10)
        self.freameCambianteFacturacion.columnconfigure(0, weight=2)
        self.freameCambianteFacturacion.columnconfigure(1, weight=2)
        self.framePrincipal.rowconfigure(0, weight=1)
        self.framePrincipal.rowconfigure(1, weight=1)

    def leer4Facturacion(self):
        if self.datosEntradasFacturacion.getValue("Código")!=None and (self.datosEntradasFacturacion.getValue("Nueva tarjeta").lower()=="si" or  self.datosEntradasFacturacion.getValue("Nueva tarjeta").lower()=="no")and self.datosEntradasFacturacion.getValue("Monto nueva Tarjeta")!=None:
            respuesta="Si"
            if self.datosEntradasFacturacion.getValue("Código")=="-1":
                respuesta="No"
            codigo=self.datosEntradasFacturacion.getValue("Código")
            compraTarjeta=self.datosEntradasFacturacion.getValue("Nueva tarjeta")
            valorNuevaTarjeta=int(self.datosEntradasFacturacion.getValue("Monto nueva Tarjeta"))
            resultado=Main.tarjetaRegalo(self.venta,codigo,respuesta,compraTarjeta, valorNuevaTarjeta)
            self.outputFacturacion.config(state="normal")
            self.outputFacturacion.delete("1.0", "end")
            self.outputFacturacion.insert("1.0",resultado)
            self.outputFacturacion.config(state="disabled")
            self.siguiente=tk.Button(self.datosEntradasFacturacion, text="Siguiente", font=("Arial", 10, "bold"), command=self.interaccion5Facturacion)
            self.siguiente.grid(row=4, column=3)
        else:
            tk.messagebox.showwarning("Faltan datos","Por favor llene todos los campos")
   
    def interaccion3Facturacion(self):
        self.cantidadBolsaGrande=0
        self.cantidadBolsaMediana=0
        self.cantidadBolsaPequeña=0
        self.descripcionF1.config(text="""Se encarga de surtir bolsas de ser necesario.""")
        self.freameCambianteFacturacion.destroy()

        self.freameCambianteFacturacion = tk.Frame(self.framePrincipal, height=150)
        self.freameCambianteFacturacion.grid(row=2, column=0, sticky="nswe")
        
        self.datosEntradasFacturacion=FieldFrame(self.freameCambianteFacturacion, "Cantidad Bolsas" ,["Cantidad a comprar"],"Cantidad que desea Comprar", ["0"],[False],ancho_entry=25, tamañoFuente=10, aceptar=True,borrar=True,callbackAceptar= self.leer3Facturacion)
        self.datosEntradasFacturacion.grid(row=1, column=0, columnspan=2)      
        self.outputFacturacion.config(state="normal")
        self.outputFacturacion.delete("1.0", "end")
        self.outputFacturacion.insert("1.0","verificando...")
        self.outputFacturacion.config(state="disabled")
        self.freameCambianteFacturacion.rowconfigure(0, weight=1)
        self.freameCambianteFacturacion.rowconfigure(1, weight=10)
        self.freameCambianteFacturacion.columnconfigure(0, weight=2)
        self.freameCambianteFacturacion.columnconfigure(1, weight=2)
        self.framePrincipal.rowconfigure(0, weight=1)
        self.framePrincipal.rowconfigure(1, weight=1)
        Main.surtirBolsas(self, self.venta, 0)
   
    def modifInteraccion3Facturacion(self,insumo, mensaje):
        self.insumo=insumo
        self.outputFacturacion.config(state="normal")
        self.outputFacturacion.delete("1.0", "end")
        self.outputFacturacion.insert("1.0",mensaje)
        self.outputFacturacion.config(state="disabled")
        self.datosEntradasFacturacion.habilitarEntry("Cantidad a comprar", True)
   
    def leer3Facturacion(self):
        if isinstance(self.datosEntradasFacturacion.getValue("Cantidad a comprar"),str):
            try:
                raise ExcepcionNumeroNoString(self.datosEntradasFacturacion.getValue("Cantidad a comprar"))
            except ExcepcionNumeroNoString as b:
                messagebox.showwarning(title="Alerta", message=b.mensaje_completo)
                return True
        elif self.datosEntradasFacturacion.getValue("Cantidad a comprar") != "":
            if  self.datosEntradasFacturacion.getValue("Cantidad a comprar") < 0:
                try:
                    raise ExcepcionValorNoValido(self.datosEntradasFacturacion.getValue("Cantidad a comprar"))  
                except ExcepcionValorNoValido as mon:
                    messagebox.showwarning(title="Alerta", message=mon.mensaje_completo)
                    return True
        if self.datosEntradasFacturacion.getValue("Cantidad a comprar")!=None:
            cantidad=int(self.datosEntradasFacturacion.getValue("Cantidad a comprar"))
            contador=0
            mensaje= Main.comprarBolsas(self, self.venta, self.insumo, cantidad)
            self.outputFacturacion.config(state="normal")
            self.outputFacturacion.delete("1.0", "end")
            self.outputFacturacion.insert("1.0",mensaje)
            self.outputFacturacion.config(state="disabled")
            self.siguiente=tk.Button(self.datosEntradasFacturacion, text="Siguiente", font=("Arial", 10, "bold"), command=self.interaccion4Facturacion)
            self.siguiente.grid(row=2, column=3)
    
    
    def interaccion2Facturacion(self):
        self.cantidadBolsaGrande=0
        self.cantidadBolsaMediana=0
        self.cantidadBolsaPequeña=0
        self.descripcionF1.config(text="""Se encarga de seleccionar bolsas para la compra.""")
        self.freameCambianteFacturacion.destroy()

        self.freameCambianteFacturacion = tk.Frame(self.framePrincipal, height=150)
        self.freameCambianteFacturacion.grid(row=2, column=0, sticky="nswe")

        self.datosEntradasFacturacion=FieldFrame(self.freameCambianteFacturacion, "Tamaño bolsa" ,["Grande","Mediana", "Pequeña"],"Bolsas Necesarias", ["0","0", "0"],[True,True,True],ancho_entry=25, tamañoFuente=10, aceptar=True,borrar=True,callbackAceptar= self.leer2Facturacion)
        self.datosEntradasFacturacion.grid(row=1, column=0, columnspan=2)
        
        self.freameCambianteFacturacion.rowconfigure(0, weight=1)
        self.freameCambianteFacturacion.rowconfigure(1, weight=10)
        self.freameCambianteFacturacion.columnconfigure(0, weight=2)
        self.freameCambianteFacturacion.columnconfigure(1, weight=2)
        self.framePrincipal.rowconfigure(0, weight=1)
        self.framePrincipal.rowconfigure(1, weight=1)
        self.revisarBolsasDisponibles()
        
    def anadirPrenda(self):
        self.freameCambianteFacturacion.destroy()

        self.freameCambianteFacturacion = tk.Frame(self.framePrincipal, height=150)
        self.freameCambianteFacturacion.grid(row=1, column=0, sticky="nswe")

        self.descripcionAñadirDespedido = tk.Label(self.freameCambianteFacturacion, text="""La prenda que desea añadir y la cantidad a comprar""", relief="ridge", font=("Arial", 10))
        self.descripcionAñadirDespedido.grid(row=0, column=0, sticky="nswe", columnspan=4)

        self.datosEntradasFacturacion=FieldFrame(self.freameCambianteFacturacion, "Añadir Prenda" ,["Prenda","Cantidad"],"valor", ["Camisa/Pantalon","0"],[True,False],ancho_entry=25, tamañoFuente=10, callbackAceptar= self.actualizarDatosAñadirSede())
        self.datosEntradasFacturacion.grid(row=1, column=0, columnspan=2)

        self.pistas=tk.Label(self.freameCambianteFacturacion, text=Main.posiblesSedes(), font=("Arial", 10))
        self.pistas.grid(row=1, column=3)
        self.aceptar=tk.Button(self.freameCambianteFacturacion, text="Aceptar", font=("Arial", 10, "bold"), command=self.anadirOtraPrenda)
        self.botonBorrarSeleccion=tk.Button(self.freameCambianteFacturacion, text="Borrar", font=("Arial", 10, "bold"), command=self.datosEntradasFacturacion.borrar)

        self.aceptar.grid(row=2, column=0)
        self.botonBorrarSeleccion.grid(row=2, column=1)
        
        self.freameCambianteFacturacion.rowconfigure(0, weight=1)
        self.freameCambianteFacturacion.rowconfigure(1, weight=10)
        self.freameCambianteFacturacion.columnconfigure(0, weight=2)
        self.freameCambianteFacturacion.columnconfigure(1, weight=2)
        self.freameCambianteFacturacion.columnconfigure(3, weight=4)
        self.framePrincipal.rowconfigure(0, weight=1)
        self.framePrincipal.rowconfigure(1, weight=10)

#Este si
    def actualizarDatosEmpleadosFacturacion(self, evento):
        if Main.verificarSedeExiste(self.datosEntradasFacturacion.getValue("sede")):
            self.datosEntradasFacturacion.habilitarEntry("Vendedor", True)
            self.datosEntradasFacturacion.configurarCallBack("Vendedor", "<Return>", lambda e: self.actualizarDatosAñadirVendedor())
            empleadosPosibles="Vendedores posibles"
            self.datosEntradasFacturacion.habilitarEntry("Empleado caja", True)
            self.datosEntradasFacturacion.configurarCallBack("Empleado caja", "<Return>", lambda e: self.actualizarDatosAñadirCaja())
            asesoresPosibles="\n\nEmpleados de caja posibles"
            
            self.sede = Main.sedePorNombre(self.datosEntradasFacturacion.getValue("sede"))
            empleados= Main.listaVendedores(self.sede)
            empleados2= Main.listaEncargados(self.sede)
            for empleado in empleados:
                if isinstance(empleado,Persona):
                    empleadosPosibles+="\n"+empleado.getNombre()
                       
            for empleado2 in empleados2:                
                if isinstance(empleado2,Persona):
                    asesoresPosibles+="\n"+empleado2.getNombre()
            self.pistas.config(text=empleadosPosibles+asesoresPosibles)

        else:
            self.datosEntradasFacturacion.habilitarEntry("sede", True)
            self.datosEntradasFacturacion.habilitarEntry("Vendedor", False)
            self.datosEntradasFacturacion.habilitarEntry("Empleado caja", False)            
            tk.messagebox.showwarning("La sede no existe", "Intente otra vez, luego de verificar el nombre de la sede")
    #Este si
    def actualizarDatosAñadirVendedor(self):
        try:
            excepcion = False
            if self.sede.getEmpleado(self.datosEntradasFacturacion.getValue("Vendedor")) is None:
                excepcion = True
            if excepcion:
                raise ExcepcionEmpleadoNoEncontrado()
        except ExcepcionEmpleadoNoEncontrado as patoLucas:
            messagebox.showwarning(title = "Alerta", message = patoLucas.mensaje_completo)
            return excepcion

  #Este si
    def actualizarDatosAñadirCaja(self):
        try:
            excepcion = False
            if self.sede.getEmpleado(self.datosEntradasFacturacion.getValue("Empleado Caja")) is None:
                excepcion = True
            if excepcion:
                raise ExcepcionEmpleadoNoEncontrado()
        except ExcepcionEmpleadoNoEncontrado as sabandija:
            messagebox.showwarning(title = "Alerta", message = sabandija.mensaje_completo)
            return excepcion

    #Este si
    def leer1Facturacion(self):
        excepcion=True
        try:
          if excepcion:
               raise ExcepcionAgregarOtraPrenda()
        except ExcepcionAgregarOtraPrenda as e:
            excepcion = messagebox.askyesno(title = "Confirmación", message= e.mensaje_completo)           
        cliente=None
        for persona in Persona.getListaPersonas():
            if persona.getNombre() == self.datosEntradasFacturacion.getValue("Cliente"):
                cliente=persona
        if (cliente is not None) and (self.sede is not None) and (self.sede.getEmpleado(self.datosEntradasFacturacion.getValue("Vendedor")) is not None) and (self.sede.getEmpleado(self.datosEntradasFacturacion.getValue("Empleado caja")) is not None) :
            self.cliente=cliente
            self.vendedor=self.sede.getEmpleado(self.datosEntradasFacturacion.getValue("Vendedor"))
            self.caja=self.sede.getEmpleado(self.datosEntradasFacturacion.getValue("Empleado caja"))
            prenda=None
            
            try: 
                if not (self.datosEntradasFacturacion.getValue("Prenda").lower() == "camisa" or self.datosEntradasFacturacion.getValue("Prenda").lower() == "pantalon"):
                    raise ExcepcionPrendaNoExistente(self.datosEntradasFacturacion.getValue("Prenda"))
            except ExcepcionPrendaNoExistente as b:
                    messagebox.showwarning(title="Alerta", message=b.mensaje_completo)
            else:
                for prendai in Sede.getPrendasInventadasTotal():
                    if (prendai.getNombre().lower()==self.datosEntradasFacturacion.getValue("Prenda").lower()):
                        prenda = prendai
                        break
                    elif (prenda == None):
                        continue
                    
                if prenda not in self.listaPrendas:
                    self.listaPrendas.append(prenda)
                    self.cantidadPrendas.append(int(self.datosEntradasFacturacion.getValue("Cantidad")))
                else:
                    self.cantidadPrendas[self.listaPrendas.index(prenda)]+=int(self.datosEntradasFacturacion.getValue("Cantidad"))
                if excepcion:
                    #self.pantallaBaseFacturacion(True)
                    self.datosEntradasFacturacion.habilitarEntry("Cliente", False)
                    self.datosEntradasFacturacion.habilitarEntry("sede", False)
                    self.datosEntradasFacturacion.habilitarEntry("Vendedor", False)
                    self.datosEntradasFacturacion.habilitarEntry("Empleado caja", False)
                else: 
                    self.venta=Main.vender(self.cliente,self.sede,self.vendedor,self.caja,self.listaPrendas,self.cantidadPrendas)
                    self.outputFacturacion.config(state="normal")
                    self.outputFacturacion.delete("1.0", "end")
                    self.outputFacturacion.insert("1.0", f"Se ha añadido la venta con éxito, subtotal: {self.venta.getSubtotal()}", "center")
                    self.outputFacturacion.config(state="disabled")
                    self.siguiente=tk.Button(self.freameCambianteFacturacion, text="Siguiente", font=("Arial", 10, "bold"), command=self.interaccion2Facturacion)
                    self.siguiente.grid(row=2, column=2)
        else:
            self.outputFacturacion.config(state="normal")
            self.outputFacturacion.delete("1.0", "end")
            self.outputFacturacion.insert("1.0", "Datos inválidos", "center")
            self.outputFacturacion.config(state="disabled")

    def leer2Facturacion(self):
        self.cantidadBolsaGrande=int(self.datosEntradasFacturacion.getValue("Grande"))
        self.cantidadBolsaMediana=int(self.datosEntradasFacturacion.getValue("Mediana"))
        self.cantidadBolsaPequeña=int(self.datosEntradasFacturacion.getValue("Pequeña"))
        revisionBolsa= self.verificarCantidadBolsa()
        self.outputFacturacion.config(state="normal")
        self.outputFacturacion.delete("1.0", "end")
        self.outputFacturacion.insert("1.0", revisionBolsa, "center")
        self.outputFacturacion.config(state="disabled")
        if revisionBolsa=="Se tienen suficientes bolsas para empacar todos los artículos":
            self.siguiente=tk.Button(self.datosEntradasFacturacion, text="Siguiente", font=("Arial", 10, "bold"), command=lambda: self.interaccion3Facturacion())
            self.siguiente.grid(row=4, column=3)

            

    def revisarBolsasDisponibles(self):
        self.bp, self.bm, self.bg = Main.verificarBolsas(self.venta)
        if self.bg>0:
            self.datosEntradasFacturacion.habilitarEntry("Grande", True)
        if self.bm>0:
            self.datosEntradasFacturacion.habilitarEntry("Mediana", True)
        if self.bp>0:
            self.datosEntradasFacturacion.habilitarEntry("Pequeña", True)
        self.outputFacturacion.config(state="normal")
        self.outputFacturacion.delete("1.0", "end")
        self.outputFacturacion.insert("1.0", f"Hay máximo {self.bg} bolsas grandes, {self.bm} bolsas medianas y {self.bp} bolsas pequeñas,", "center")     
        self.outputFacturacion.config(state="disabled")

    def verificarCantidadBolsa(self):
        
        if self.cantidadBolsaGrande<=self.bg or self.cantidadBolsaMediana<=self.bm or self.cantidadBolsaPequeña<=self.bp:
            BolsasFaltantes=Main.cantidadActualBolsas(self.venta, self.cantidadBolsaGrande, self.cantidadBolsaMediana, self.cantidadBolsaPequeña)
            self.outputFacturacion.config(state="normal")
            self.outputFacturacion.delete("1.0", "end")
            self.bolsas+=self.cantidadBolsaGrande+ self.cantidadBolsaMediana+ self.cantidadBolsaPequeña
            if BolsasFaltantes>0:
                bolasNecesarias=f"Se necesitan {BolsasFaltantes} bolsas más para empacar todos los artículos"
                self.datosEntradasFacturacion.habilitarEntry("Grande", True)
                self.datosEntradasFacturacion.habilitarEntry("Mediana", True)
                self.datosEntradasFacturacion.habilitarEntry("Pequeña", True)                
            else:
                bolasNecesarias="Se tienen suficientes bolsas para empacar todos los artículos"
                self.datosEntradasFacturacion.habilitarEntry("Grande", False)
                self.datosEntradasFacturacion.habilitarEntry("Mediana", False)
                self.datosEntradasFacturacion.habilitarEntry("Pequeña", False)
            self.outputFacturacion.config(state="disabled")   
            return bolasNecesarias
        else:
            self.datosEntradasFacturacion.borrar()
#endregion

def pasarAVentanaPrincipal():
    ventana = StartFrame()
    ventana.mainloop()
    