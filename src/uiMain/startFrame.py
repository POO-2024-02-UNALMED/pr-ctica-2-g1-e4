# Dibuja la ventana y la parte externa, y la parte interna la saca de las clases F.
# O en el caso respectivo, no dibuja una funcionalidad, sino frameInicial.
#region imports
import os
import tkinter as tk
from tkinter import ttk
from tkinter.font import Font
from tkinter import messagebox
import sys
import unicodedata
from src.gestorAplicacion.administracion.empleado import Empleado
from src.gestorAplicacion.persona import Persona
from src.uiMain import fieldFrame
from src.gestorAplicacion.venta import Venta
from src.uiMain.Excepciones.exceptionC1 import ExceptionC1
from src.uiMain.Excepciones.exceptionC1 import ExcepcionContenidoVacio
from src.uiMain.Excepciones.exceptionC1 import ExcepcionNumeroNoString
from src.uiMain.Excepciones.exceptionC1 import ExcepcionStringNoNumero
from src.uiMain.Excepciones.exceptionC1 import ExcepcionValorNoValido
from src.uiMain.Excepciones.exceptionC2 import ExceptionC2
from src.uiMain.Excepciones.exceptionC2 import ExcepcionAgregarOtraPrenda
from src.uiMain.Excepciones.exceptionC2 import ExcepcionCodigoTarjetaregalo
from src.uiMain.Excepciones.exceptionC2 import ExcepcionEmpleadoNoEncontrado
from src.uiMain.Excepciones.exceptionC2 import ExcepcionPrendaNoExistente
from src.uiMain.main import Main
from src.uiMain.fieldFrame import FieldFrame
from src.gestorAplicacion.fecha import Fecha
from src.gestorAplicacion.sede import Sede
from src.gestorAplicacion.administracion.rol import Rol
import math
import threading
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
        self.archivoMenu.add_command(label="Aplicacion", command = lambda : tk.messagebox.showinfo("Informacion", "La aplicación se enfoca principalmente en la creación de un sistema integral que aborda los retos operativos más relevantes de una industria textil, como lo es la empresa de Ecomoda, donde se maneja aspectos de gestión humana, manejo de insumos, planificación financiera, procesos de facturación y producción de prendas."))
        self.archivoMenu.add_command(label="Salir", command = lambda : self.pasarABienvenida())
        self.procesosMenu= tk.Menu(self.barraMenus, tearoff=0)
        self.barraMenus.add_cascade(label="Procesos y Consultas", menu=self.procesosMenu)
        self.procesosMenu.add_command(label="Despedir y reemplazar empleados", command = lambda :self.abrirGestionHumana())
        self.procesosMenu.add_separator()
        self.procesosMenu.add_command(label="Pedir insumos", command = lambda : self.eliminarF2())
        self.procesosMenu.add_separator()
        self.procesosMenu.add_command(label="Ver el desglose económico de la empresa", command = lambda : self.eliminarF3())
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
    def normalizar_texto(self,texto):
        return unicodedata.normalize("NFKD", texto).encode("ASCII", "ignore").decode("utf-8").strip().lower()
   
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
        self.cambiarFrame(self.producir(self))
        
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
            
    def ajustar_wraplengthhola(self,label):        
        nuevo_wraplength = label.winfo_width()
        if label.cget("wraplength") != nuevo_wraplength:
            label.config(wraplength=nuevo_wraplength)
    
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
        self.descripcionFrameInicial.bind('<Configure>', lambda e: self.descripcionFrameInicial.config(wraplength=self.descripcionFrameInicial.winfo_width()))
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

        self.descripcionFrameInicial.bind('<Configure>', lambda e: self.ajustar_wraplengthhola(self.descripcionFrameInicial))
    
    def actualizarWrapLengths(self,_event):
        if self.pagina=="inicial":
            self.descripcionFrameInicial.config(wraplength=self.frameInicial.winfo_width()*0.9)
            self.instruccionesFrameInicial.config(wraplength=self.contenedorFecha.winfo_width()*0.9)
            if self.winfo_width()<400:
                self.labelFotoEcomoda.place(relx=0.5, rely=0.2, relwidth=1, relheight=0.3, anchor="n")



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
               
        fecha_ingresada=self.ingresarFecha(FDia,FMes,FAño)
        if isinstance(fecha_ingresada,Fecha):
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
        
        excepcion = []
        try:
            if not partesDia[-1].isdigit():
                excepcion.append(partesDia)
            if not partesMes[-1].isdigit():
                excepcion.append(partesMes)
            if  not partesAño[-1].isdigit():
                excepcion.append(partesAño)
            if excepcion != []:
                raise ExcepcionNumeroNoString(excepcion)
        except ExcepcionNumeroNoString as t:
            messagebox.showwarning(title="Alerta", message=t.mensaje_completo)
            return True

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
        self.paginaGHumana="Tabla"
        self.inicialGestionHumana()
        self.empleadosADespedir=[] # Se llena al dar aceptar en la pantalla de seleccion.
        Main.estadoGestionHumana="despedir"
        self.bind("<Configure>", self.actualizarWrapLengthsGHumana)
        self.cantidadADespedir=0
        return self.gestionHumana

    def actualizarWrapLengthsGHumana(self,_event):
        if not self.pagina=="gestionHumana":
            return

        match self.paginaGHumana:
            case "Tabla":
                self.descripcionF1.config(wraplength=self.frameCambianteGHumana.winfo_width()*0.9)
            case "EleccionDespidos":
                self.labelPreConsulta.config(wraplength=self.frameCambianteGHumana.winfo_width()*0.9)
            case "Reemplazo":
                self.tituloTanda.config(wraplength=self.frameCambianteGHumana.winfo_width()*0.9)
                self.descripcionCambioSede.config(wraplength=self.frameCambianteGHumana.winfo_width()*0.9)
            case "Despedida":
                self.descripcionCambioSede.config(wraplength=self.frameCambianteGHumana.winfo_width()*0.9)

        
    def inicialGestionHumana(self):
        self.framePrincipal =  tk.Frame(self.gestionHumana)
        self.framePrincipal.pack(fill="both", expand=True, padx=7, pady=7)

        self.tituloF1 = tk.Label(self.framePrincipal, text="Gestión Humana", bg="medium orchid", relief="ridge", font=("Arial",16, "bold"))
        self.tituloF1.grid(row=0, column=0, sticky="nswe")
        self.tituloF1.bind('<Configure>', lambda e: self.ajustar_wraplengthhola(self.tituloF1))
        
        self.frameCambianteGHumana = tk.Frame(self.framePrincipal)
        self.frameCambianteGHumana.grid(row=1, column=0, sticky="nswe")

        ## relwidth y relheight reciben el porcentaje de tamaño respecto al contenedor
        self.descripcionF1 = tk.Label(self.frameCambianteGHumana, text="""Este área analiza la lista de todos los empleados y permite modificarla:
Se puede contratar a un nuevo empleado, establecer su salario y el rol o las funciones que cumple en la empresa.
También se puede despedir a un empleado ya existente en el equipo de trabajo.
        
Con ese fin, analizamos el rendimiento de los empleados de la empresa, y llegamos a la siguiente lista de empleados insuficientes,
estos pudieron ser cambiados de area o sede, y si estan marcados con ¿despedir?, podrá elegirlos para despedirlos en la siguiente pantalla.""".replace("\n"," "), relief="ridge", font=("Arial", 10))
        self.descripcionF1.grid(row=1, column=0, sticky="nswe",columnspan=5)
        
        self.descripcionF1.bind('<Configure>', lambda e: self.ajustar_wraplengthhola(self.descripcionF1))

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
        
        self.tituloNombre.bind('<Configure>', lambda e: self.ajustar_wraplengthhola(self.tituloNombre))
        self.tituloArea.bind('<Configure>', lambda e: self.ajustar_wraplengthhola(self.tituloArea))
        self.tituloRendimiento.bind('<Configure>', lambda e: self.ajustar_wraplengthhola(self.tituloRendimiento))
        self.tituloRendimientoEsperado.bind('<Configure>', lambda e: self.ajustar_wraplengthhola(self.tituloRendimientoEsperado))
        self.tituloAccion.bind('<Configure>', lambda e: self.ajustar_wraplengthhola(self.tituloAccion))   
             
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
        self.paginaGHumana="EleccionDespidos"
        if limpiarFrame:
            self.frameCambianteGHumana.destroy()
            self.frameCambianteGHumana = tk.Frame(self.framePrincipal)
            self.frameCambianteGHumana.grid(row=1, column=0, sticky="nswe",columnspan=4)

        empleadosMalosString=""
        
        empleadosMalosString += """Los empleados de la derecha no rinden correctamente y no pudieron ser cambiados ni de area ni de sede.\n"""

        empleadosMalosString += """También puede añadir a otros empleados, para buscar mas empleados, haga click en "Añadir empleado a la lista guía" \n"""

        empleadosMalosString+=Main.mensajePromedioHumanas()

        self.labelPreConsulta=tk.Label(self.frameCambianteGHumana, text=empleadosMalosString, relief="ridge", font=("Arial", 10))
        self.labelPreConsulta.grid(row=1, column=0, sticky="nswe",columnspan=4)
        self.labelPreConsulta.bind('<Configure>', lambda e: self.ajustar_wraplengthhola(self.labelPreConsulta))

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
        try:
            if isinstance(self.seleccionador.getValue("Cantidad de despedidos"), str) and not\
                self.seleccionador.getValue("Cantidad de despedidos").lstrip('-').replace('.', '', 1).isdigit():
                raise ExcepcionNumeroNoString(self.seleccionador.getValue("Cantidad de despedidos"))
        except ExcepcionNumeroNoString as iguana:
            messagebox.showwarning(title="Alerta", message=iguana.mensaje_completo)
            return True
        else:
            try:
               if int(self.seleccionador.getValue("Cantidad de despedidos")) < 0:
                raise ExcepcionValorNoValido(self.seleccionador.getValue("Cantidad de despedidos"))
            except ExcepcionValorNoValido as tabl:
                messagebox.showwarning(title="Alerta", message=tabl.mensaje_completo)
                return True
            else:
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
        self.paginaGHumana="AñadirDespedido"
        self.frameCambianteGHumana.destroy()

        self.frameCambianteGHumana = tk.Frame(self.framePrincipal, height=150)
        self.frameCambianteGHumana.grid(row=1, column=0, sticky="nswe")

        self.descripcionAñadirDespedido = tk.Label(self.frameCambianteGHumana, text="""Inserte los datos de el empleado a añadir a la lista, el panel de la derecha le ayudará, presione Enter al terminar de escribir un valor""", relief="ridge", font=("Arial", 10))
        self.descripcionAñadirDespedido.grid(row=0, column=0, sticky="nswe", columnspan=4)
        self.descripcionAñadirDespedido.bind('<Configure>', lambda e: self.ajustar_wraplengthhola(self.descripcionAñadirDespedido))

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
            try:
                if not isinstance(self.datosDespedido.getValue("sede"),str):
                    raise ExcepcionStringNoNumero(self.datosDespedido.getValue("sede"))
            except ExcepcionStringNoNumero as wey:
                messagebox.showwarning(title="Alerta", message=wey.mensaje_completo)
            try:
                raise ExcepcionValorNoValido(self.datosDespedido.getValue("sede"))
            except ExcepcionValorNoValido as otei:
                messagebox.showwarning(title="Alerta", message=otei.mensaje_completo)
                return True

    def actualizarDatosAñadirEmpleado(self):
        if self.sede.getEmpleado(self.datosDespedido.getValue("nombre")) is None:
            try:
                if int(self.datosDespedido.getValue("nombre")):
                    raise ExcepcionStringNoNumero(self.datosDespedido.getValue("nombre"))
            except ExcepcionStringNoNumero as yay:
                messagebox.showwarning(title="Alerta", message=yay.mensaje_completo)
                return True
            try:
                raise ExcepcionEmpleadoNoEncontrado()
            except ExcepcionEmpleadoNoEncontrado as buey:
                messagebox.showwarning(title="Alerta", message=buey.mensaje_completo)
                return True
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
        self.descripcionCambioSede.bind('<Configure>', lambda e: self.ajustar_wraplengthhola(self.descripcionCambioSede))
        Main.prepararCambioSede()
        tanda = Main.getTandaReemplazo()
        if tanda is None:
            pass
        else:
            self.dibujarTandaDeReemplazo(tanda)

        self.frameCambianteGHumana.columnconfigure(0, weight=3)
    
    def dibujarTandaDeReemplazo(self, tanda):
        self.paginaGHumana="Reemplazo"
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
        self.tituloTanda.bind('<Configure>', lambda e: self.ajustar_wraplengthhola(self.tituloTanda))

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
                self.paginaGHumana="Despedida"
                self.frameCambianteGHumana.destroy()
                self.frameCambianteGHumana = tk.Frame(self.framePrincipal)
                self.frameCambianteGHumana.grid(row=1, column=0, sticky="nswe")
                self.descripcionCambioSede = tk.Label(self.frameCambianteGHumana, text=f"""Se ha completado el reemplazo de los empleados, tenga buen día.""", relief="ridge", font=("Arial", 10))
                self.descripcionCambioSede.grid(row=0, column=0 ,sticky="nswe")
                self.descripcionCambioSede.bind('<Configure>', lambda e: self.ajustar_wraplengthhola(self.descripcionCambioSede))
                self.frameCambianteGHumana.columnconfigure(0, weight=3)
                self.frameCambianteGHumana.rowconfigure(0, weight=3)
            else:
                self.dibujarTandaDeReemplazo(Main.getTandaReemplazo())
        else:
            try:
                if int(self.seleccionadorReemplazo.getValue(f"Reemplazo {i}")):
                    raise ExcepcionStringNoNumero(self.seleccionadorReemplazo.getValue(f"Reemplazo {i}"))
            except ExcepcionStringNoNumero as estoyCansadojefe:
                messagebox.showwarning(title="Alerta", message=estoyCansadojefe.mensaje_completo)
                return True
            
            try:
                raise ExcepcionEmpleadoNoEncontrado()
            except ExcepcionEmpleadoNoEncontrado as tururu:
                messagebox.showwarning(title="Alerta", message=tururu.mensaje_completo)
                return True
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
        self.tituloF2.bind('<Configure>', lambda e: self.ajustar_wraplengthhola(self.tituloF2))

            ## relwidth y relheight reciben el porcentaje de tamaño respecto al contenedor
        self.descripcionF2 = tk.Label(self.framePrincipal, 
                            text="Registra la llegada de nuevos insumos: Incluye una predicción de ventas del siguiente mes para hacer la compra de los insumos, actualiza la deuda con los proveedores y añade los nuevos insumos a la cantidad en Stock.", 
                            relief="ridge", wraplength=600)
        self.descripcionF2.grid(row=1, column=0, sticky="nswe")
        self.descripcionF2.bind('<Configure>', lambda e: self.ajustar_wraplengthhola(self.descripcionF2))

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
        for pesimismo in pesimismos:
            if 0 > int(pesimismo) or int(pesimismo) > 100:  
                try:
                    raise ExcepcionValorNoValido(pesimismo)
                except ExcepcionValorNoValido as guagua:
                    messagebox.showwarning(title="Alerta", message=guagua.mensaje_completo)
                    return True          
            else:
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
        label3.bind('<Configure>', lambda e: self.ajustar_wraplengthhola(label3))
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
        self.descripcionF2.bind('<Configure>', lambda e: self.ajustar_wraplengthhola(self.descripcionF2))
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
        self.seguirDeTabla.bind('<Configure>', lambda e: self.ajustar_wraplengthhola(self.seguirDeTabla))
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
        self.descripcionF2.bind('<Configure>', lambda e: self.ajustar_wraplengthhola(self.descripcionF2))
        if len(criterios)>0:
            self.contenedorFieldTransferencia = tk.Frame(self.frameCambianteInsumos)
            self.contenedorFieldTransferencia.pack(anchor="s", expand=True, fill="both")

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
        if Main.errorEnRespuestas:
            try:
                raise ExcepcionValorNoValido(Main.respuestaIncorrecta)
            except ExcepcionValorNoValido as hambre:
                messagebox.showwarning(title="Alerta", message=hambre.mensaje_completo)
                return True
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
            self.explicacion.bind('<Configure>', lambda e: self.ajustar_wraplengthhola(self.explicacion))
            self.seguirADeudas=tk.Button(self.frameCambianteInsumos, text="Ver deudas", command=self.dibujarDeudas)
            self.seguirADeudas.grid(row=1, column=0)
            self.frameCambianteInsumos.rowconfigure(0, weight=1)
            self.frameCambianteInsumos.columnconfigure(0, weight=1)
    
    def comprarExtra(self):
        entradaValida=Main.terminarCompraDeInsumos(self.fieldCompraExtra.obtenerTodosLosValores())
        if not entradaValida:
            try:
                raise ExcepcionValorNoValido(Main.valor)
            except ExcepcionValorNoValido as sueñito:
                messagebox.showwarning(title="Alerta", message=sueñito.mensaje_completo)
                return True
        self.dibujarDeudas()
    
    def dibujarDeudas(self):
        self.descripcionF2.config(text="""A continuación se muestra la deuda con los proveedores, y el estado de la misma, comprar insumos aumenta la deuda.
Ya terminamos, tenga buen día.""")
        self.descripcionF2.bind('<Configure>', lambda e: self.ajustar_wraplengthhola(self.descripcionF2))
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
                    if  Porcentaje == "":
                        raise ExcepcionContenidoVacio(["Fidelidad"])
                    elif isinstance(Porcentaje, str) and not str(Porcentaje).replace(".", "", 1).isdigit():
                        raise ExcepcionNumeroNoString(Porcentaje)
                except ExcepcionNumeroNoString as uwu:
                    messagebox.showwarning(title="Alerta", message=uwu.mensaje_completo)
                    return True 
                except ExcepcionContenidoVacio as cabezaHueca:
                    messagebox.showwarning(title="Alerta", message=cabezaHueca.mensaje_completo)
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
                        if seleccion == "":
                            raise ExcepcionContenidoVacio(["Bancos"])
                        if not isinstance(seleccion, str):
                            raise ExcepcionStringNoNumero(seleccion)
                    except ExcepcionStringNoNumero as p:
                        messagebox.showwarning(title="Alerta", message=p.mensaje_completo)
                        return True
                    except ExcepcionContenidoVacio as cabezaHueca:
                        messagebox.showwarning(title="Alerta", message=cabezaHueca.mensaje_completo)
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
                if Porcentaje == "":
                    try:
                        raise ExcepcionContenidoVacio(["Descuento a futuro"]) 

                    except ExcepcionContenidoVacio as cabezaHueca:
                        messagebox.showwarning(title="Alerta", message=cabezaHueca.mensaje_completo)
                        return True
                else:
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
                    try:
                        entradas = field_frame.obtenerTodosLosValores()  
                        vacios = [] 
                        nombresCamposVacíos = []  
                        hayExcepcion = False
                        criterios = []
                        
                        for i, c in enumerate(field_frame.citerios):
                            criterios.append(c)

                        for i, valor in enumerate(entradas):
                            if valor.strip() == "":  
                                hayExcepcion = True
                                vacios.append(field_frame.valores[i])  
                                nombresCamposVacíos.append(criterios[i])
                        if  combo.get() == "":
                            raise ExcepcionContenidoVacio(nombresCamposVacíos+["Directivo"])                   
                        if hayExcepcion:
                            raise ExcepcionContenidoVacio(nombresCamposVacíos) 

                    except ExcepcionContenidoVacio as cabezaHueca:
                        messagebox.showwarning(title="Alerta", message=cabezaHueca.mensaje_completo)
                        return hayExcepcion

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
            tituloF3.bind('<Configure>', lambda e: self.ajustar_wraplengthhola(tituloF3))
            ## relwidth y relheight reciben el porcentaje de tamaño respecto al contenedor
            descripcionF3 = tk.Label(frame1, text="Se realiza una evaluación del estado financiero de la empresa haciendo el cálculo de los activos y los pasivos, para indicarle al usuario qué tan bien administrada está, mostrandole los resulatdos y su significado", relief="ridge", wraplength=600)
            descripcionF3.place(relx=1, rely=0.7, relwidth=1, relheight=0.4, anchor="e")
            descripcionF3.bind('<Configure>', lambda e: self.ajustar_wraplengthhola(descripcionF3))
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
            label7.bind('<Configure>', lambda e: self.ajustar_wraplengthhola(label7))            
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
        ["Fecha","Cliente","sede", "Vendedor","Empleado caja","Prenda", "Cantidad"],"valor", [f"Dia: {Main.fecha.getDia()}  Mes: {Main.fecha.getMes()}  Año: {Main.fecha.getAno()}","","Sede Principal", "",
        "","Camisa/Pantalon","0"],[False,True,True,False,False,True,True],ancho_entry=25, tamañoFuente=10)
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
        
        self.datosEntradasFacturacion=FieldFrame(self.freameCambianteFacturacion, "Fondos" ,["Transferir fondos a la cuenta principal","Porcentaje a transferir"],"", ["Si/No","20% o 60%"],[True,False],ancho_entry=25, tamañoFuente=10)
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

    def transferirDinero(self, event):
        self.dineroTransferido=True
        if (self.datosEntradasFacturacion.getValue("Transferir fondos a la cuenta principal").lower())=="si" or (self.datosEntradasFacturacion.getValue("Transferir fondos a la cuenta principal").lower())=="no":
            self.datosEntradasFacturacion.habilitarEntry("Porcentaje a transferir", True)
        else:
            valor = (self.datosEntradasFacturacion.getValue("Transferir fondos a la cuenta principal").lower())
            try: 
                if not isinstance(valor, str):
                    raise ExcepcionStringNoNumero((self.datosEntradasFacturacion.getValue("Transferir fondos a la cuenta principal")))
                if valor =="":
                    raise ExcepcionContenidoVacio(["Porcentaje a transferir"])
            except ExcepcionContenidoVacio as cabezaHueca:
                messagebox.showwarning(title="Alerta", message=cabezaHueca.mensaje_completo)
           
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
        

        if not (self.datosEntradasFacturacion.getValue("Porcentaje a transferir").strip("%").isdigit()):    
            try:
                raise ExcepcionNumeroNoString(self.datosEntradasFacturacion.getValue("Porcentaje a transferir"))
            except ExcepcionNumeroNoString as b:
                messagebox.showwarning(title="Alerta", message=b.mensaje_completo + " válidos")
                return True          

        else:
            if self.datosEntradasFacturacion.getValue("Porcentaje a transferir")!=None and self.datosEntradasFacturacion.getValue("Transferir fondos a la cuenta principal")!=None:
                string=self.datosEntradasFacturacion.getValue("Porcentaje a transferir").strip("%")
                if str(string).replace(".", "", 1).isdigit():
                    porcentaje=int(string)
                if self.datosEntradasFacturacion.getValue("Transferir fondos a la cuenta principal").lower()=="si" or self.datosEntradasFacturacion.getValue("Transferir fondos a la cuenta principal").lower()=="no":
                    if self.datosEntradasFacturacion.getValue("Transferir fondos a la cuenta principal").lower()=="si" and porcentaje>=20 and porcentaje <=60:
                        mensajeFinal,mensaje=Main.ingresoEmpresa(self.venta, self.datosEntradasFacturacion.getValue("Transferir fondos a la cuenta principal").lower(), porcentaje)
                    else:
                        mensajeFinal=Main.ingresoEmpresa(self.venta, self.datosEntradasFacturacion.getValue("Transferir fondos a la cuenta principal").lower(), 0)
                        mensaje="No se transfirió el dinero a la cuenta principal."
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
        try:
            entradas = [self.datosEntradasFacturacion.getValue("Código"), self.datosEntradasFacturacion.getValue("Nueva tarjeta"), self.datosEntradasFacturacion.getValue("Monto nueva Tarjeta")]  
            vacios = [] 
            nombresCamposVacíos = []  
            hayExcepcion = False
            criterios = [["Código"],["Nueva tarjeta"],["Monto nueva Tarjeta"]]

            codigos = Venta.getCodigosRegalo()
            if self.datosEntradasFacturacion.getValue("Código") is not None:
                if self.datosEntradasFacturacion.getValue("Código") != "-1" and \
                    self.datosEntradasFacturacion.getValue("Código") not in codigos:
                    try:
                        raise ExcepcionCodigoTarjetaregalo(self.datosEntradasFacturacion.getValue("Código"))
                    except ExcepcionCodigoTarjetaregalo as chacarron:
                        messagebox.showwarning(title="Alerta", message=chacarron.mensaje_completo)
                        return True

            for i, valor in enumerate(entradas):
                if valor.strip() == "":  
                    hayExcepcion = True
                    vacios.append(self.freameCambianteFacturacion.valores[i])  
                    nombresCamposVacíos.append(criterios[i])
            if hayExcepcion:
                raise ExcepcionContenidoVacio(nombresCamposVacíos) 

        except ExcepcionContenidoVacio as cabezaHueca:
            messagebox.showwarning(title="Alerta", message=cabezaHueca.mensaje_completo)
            return hayExcepcion
        try:
            nuevaTarjeta = self.datosEntradasFacturacion.getValue("Monto nueva Tarjeta")
            if isinstance(nuevaTarjeta, str) and not (nuevaTarjeta).replace(" ", "")\
                .replace("-", "", 1).replace(".", "", 1).isdigit():
                raise ExcepcionNumeroNoString(nuevaTarjeta)
        except ExcepcionNumeroNoString as b:
            messagebox.showwarning(title="Alerta", message=b.mensaje_completo)
            return True
        try:
            tarjeta = self.datosEntradasFacturacion.getValue("Nueva tarjeta").lower()
            if not isinstance(tarjeta, str) and (tarjeta).replace(" ", "")\
                .replace("-", "", 1).replace(".", "", 1).isdigit():
                raise ExcepcionStringNoNumero(tarjeta)
        except ExcepcionValorNoValido as roscon:
                    messagebox.showwarning(title="Alerta", message=roscon.mensaje_completo)
                    return True
        else:
            if self.datosEntradasFacturacion.getValue("Nueva tarjeta").lower() not in ["si", "no"]:
                try:
                    raise ExcepcionValorNoValido(self.datosEntradasFacturacion.getValue("Nueva tarjeta"))
                except ExcepcionValorNoValido as mandubia:
                    messagebox.showwarning(title="Alerta", message=mandubia.mensaje_completo)
                    return True

        if  int(self.datosEntradasFacturacion.getValue("Monto nueva Tarjeta")) < 0:
            try:
                raise ExcepcionValorNoValido(self.datosEntradasFacturacion.getValue("Monto nueva Tarjeta"))  
            except ExcepcionValorNoValido as mon:
                messagebox.showwarning(title="Alerta", message=mon.mensaje_completo)
                return True
        else:        
            if  self.datosEntradasFacturacion.getValue("Código")!=None and (self.datosEntradasFacturacion.getValue("Nueva tarjeta").lower()=="si" or  self.datosEntradasFacturacion.getValue("Nueva tarjeta").lower()=="no")and self.datosEntradasFacturacion.getValue("Monto nueva Tarjeta")!=None:
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
        try:
            cantidad = self.datosEntradasFacturacion.getValue("Cantidad a comprar")
            if isinstance(cantidad, str):
               cantidad = cantidad.strip() 
            if cantidad.startswith("-"):  
                cantidad = cantidad[1:] 
            if not cantidad.replace(".", "", 1).isdigit():
                raise ExcepcionNumeroNoString(self.datosEntradasFacturacion.getValue("Cantidad a comprar"))
        except ExcepcionNumeroNoString as b:
            messagebox.showwarning(title="Alerta", message=b.mensaje_completo)
            return True
               
        if  int(self.datosEntradasFacturacion.getValue("Cantidad a comprar")) < 0:
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
            try:
                raise ExcepcionValorNoValido(self.datosEntradasFacturacion.getValue("sede"))
            except ExcepcionValorNoValido as rarara:
                messagebox.showwarning(title="Alerta", message=rarara.mensaje_completo)
                return True
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
            if self.normalizar_texto(persona.getNombre()) == self.normalizar_texto(self.datosEntradasFacturacion.getValue("Cliente")):
                cliente=persona  
      
        try:
            error = []
            if cliente =="":
                error.append("Cliente")
            if self.sede =="":
                error.append("Sede")
            if self.datosEntradasFacturacion.getValue("Vendedor").strip()=="":
                error.append("Vendedor")
            if self.datosEntradasFacturacion.getValue("Empleado caja").strip()=="":
                error.append("Empleado caja")
            if self.datosEntradasFacturacion.getValue("Prenda").strip()=="":
                error.append("Prenda")
            if self.datosEntradasFacturacion.getValue("Cantidad").strip()=="":
                error.append("Cantidad")       
            if error != []:
                raise ExcepcionContenidoVacio(error)
        except ExcepcionContenidoVacio as cabezaHueca:
            messagebox.showwarning(title="Alerta", message=cabezaHueca.mensaje_completo)
            return True
        if error == []:
            listaClientes = []
            for clienteI in Persona.getListaPersonas():
               listaClientes.append(self.normalizar_texto(clienteI.getNombre()))
            if self.normalizar_texto(self.datosEntradasFacturacion.getValue("Cliente")) not in listaClientes:
                try:
                    if self.normalizar_texto(self.datosEntradasFacturacion.getValue("Cliente")) not in listaClientes:
                        raise ExcepcionValorNoValido(self.datosEntradasFacturacion.getValue("Cliente"))
                except ExcepcionValorNoValido as z:
                    messagebox.showwarning(title="Alerta", message=z.mensaje_completo)
                    return True
            listaVendedor = []

            for vendedorI in Sede.getListaEmpleadosTotal():
                listaVendedor.append(self.normalizar_texto(vendedorI.getNombre()))
            if self.normalizar_texto(self.datosEntradasFacturacion.getValue("Vendedor")) not in listaVendedor:
                try:
                    if self.datosEntradasFacturacion.getValue("Vendedor") not in listaVendedor:
                        raise ExcepcionValorNoValido(self.datosEntradasFacturacion.getValue("Vendedor"))
                except ExcepcionValorNoValido as z:
                    messagebox.showwarning(title="Alerta", message=z.mensaje_completo)
                    return True
            listaEmpleadoCaja = []
            for cajaI in Sede.getListaEmpleadosTotal():
                listaEmpleadoCaja.append(self.normalizar_texto(cajaI.getNombre()))
            if self.normalizar_texto(self.datosEntradasFacturacion.getValue("Empleado caja")) not in listaEmpleadoCaja:
                try:
                    raise ExcepcionValorNoValido(self.datosEntradasFacturacion.getValue("Empleado caja"))
                except ExcepcionValorNoValido as z:
                    messagebox.showwarning(title="Alerta", message=z.mensaje_completo)
                    return True
            cantidadI = self.datosEntradasFacturacion.getValue("Cantidad")
            if not (cantidadI).replace(" ", "").replace("-", "", 1).replace(".", "", 1).isdigit():
                try:
                    raise ExcepcionNumeroNoString(cantidadI)
                except ExcepcionNumeroNoString as pi:
                    messagebox.showwarning(title="Alerta", message=pi.mensaje_completo)
                    return True
            else:
                cantidadI = int(self.datosEntradasFacturacion.getValue("Cantidad"))
                try:
                    if cantidadI <= 0:
                        raise ExcepcionValorNoValido(cantidadI)
                except ExcepcionValorNoValido as wiwiwi:
                    messagebox.showwarning(title="Alerta", message=wiwiwi.mensaje_completo)
                    return True

                listaEmpleadoCaja = []
                for cajaI in Sede.getListaEmpleadosTotal():
                    listaEmpleadoCaja.append(self.normalizar_texto(cajaI.getNombre()))
                if self.normalizar_texto(self.datosEntradasFacturacion.getValue("Empleado caja")) not in listaEmpleadoCaja:
                    try:
                        raise ExcepcionValorNoValido(self.datosEntradasFacturacion.getValue("Empleado caja"))
                    except ExcepcionValorNoValido as z:
                        messagebox.showwarning(title="Alerta", message=z.mensaje_completo)
                        return True
                cantidadI = self.datosEntradasFacturacion.getValue("Cantidad")
                if not (cantidadI).replace(" ", "").replace("-", "", 1).replace(".", "", 1).isdigit():
                    try:
                        raise ExcepcionNumeroNoString(cantidadI)
                    except ExcepcionNumeroNoString as pi:
                        messagebox.showwarning(title="Alerta", message=pi.mensaje_completo)
                        return True
                else:
                    cantidadI = int(self.datosEntradasFacturacion.getValue("Cantidad"))
                    try:
                        if cantidadI < 0:
                            raise ExcepcionValorNoValido(cantidadI)
                    except ExcepcionValorNoValido as wiwiwi:
                        messagebox.showwarning(title="Alerta", message=wiwiwi.mensaje_completo)
                        return True
                            
        if error == []:
            self.cliente=cliente
            self.vendedor=self.sede.getEmpleado(self.datosEntradasFacturacion.getValue("Vendedor"))
            self.caja=self.sede.getEmpleado(self.datosEntradasFacturacion.getValue("Empleado caja"))
            prenda=None
            
            try: 
                if self.datosEntradasFacturacion.getValue("Prenda").lower() not in ["camisa","pantalon"]:
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
                    
            try:
                entradas = self.datosEntradasFacturacion.obtenerTodosLosValores()  
                vacios = [] 
                nombresCamposVacíos = []  
                hayExcepcion = False
                criterios = []
                
                for i, c in enumerate(self.datosEntradasFacturacion.citerios):
                    criterios.append(c)

                for i, valor in enumerate(entradas):
                    if valor.strip() == "":  
                        hayExcepcion = True
                        vacios.append(self.datosEntradasFacturacion.valores[i])  
                        nombresCamposVacíos.append(criterios[i])            
                if hayExcepcion:
                    raise ExcepcionContenidoVacio(nombresCamposVacíos) 

            except ExcepcionContenidoVacio as cabezaHueca:
                messagebox.showwarning(title="Alerta", message=cabezaHueca.mensaje_completo)
                return hayExcepcion

         
    def leer2Facturacion(self):
        self.cantidadBolsaGrande= self.datosEntradasFacturacion.getValue("Grande")
        self.cantidadBolsaMediana= self.datosEntradasFacturacion.getValue("Mediana")
        self.cantidadBolsaPequeña= self.datosEntradasFacturacion.getValue("Pequeña")
        error = []
        try:
            if isinstance(self.cantidadBolsaGrande, str) and not (self.cantidadBolsaGrande).replace(" ", "")\
                .replace("-", "", 1).replace(".", "", 1).isdigit():
                error.append(self.cantidadBolsaGrande)
            if isinstance(self.cantidadBolsaMediana, str) and not (self.cantidadBolsaMediana).replace(" ", "")\
                .replace("-", "", 1).replace(".", "", 1).isdigit():
                error.append(self.cantidadBolsaMediana)
            if isinstance(self.cantidadBolsaPequeña, str) and not (self.cantidadBolsaPequeña).replace(" ", "")\
                .replace("-", "", 1).replace(".", "", 1).isdigit():
                error.append(self.cantidadBolsaPequeña)

            if error != []:
                raise ExcepcionNumeroNoString(error)
        except ExcepcionNumeroNoString as chicarron:
            messagebox.showwarning(title="Alerta", message=chicarron.mensaje_completo)
            return True
        self.cantidadBolsaGrande=int(self.datosEntradasFacturacion.getValue("Grande"))
        self.cantidadBolsaMediana=int(self.datosEntradasFacturacion.getValue("Mediana"))
        self.cantidadBolsaPequeña=int(self.datosEntradasFacturacion.getValue("Pequeña"))
        if error == []:
            try:
                if self.cantidadBolsaGrande < 0:
                    error.append(self.cantidadBolsaGrande)
                if self.cantidadBolsaMediana < 0:
                    error.append(self.cantidadBolsaMediana)
                if self.cantidadBolsaPequeña < 0:
                    error.append(self.cantidadBolsaPequeña)
                if error != []:
                    raise ExcepcionValorNoValido(error)
            except ExcepcionValorNoValido as jiejie:
                messagebox.showwarning(title="Alerta", message=jiejie.mensaje_completo)
                return True
                
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



    #region produccion
#---------------------------------------------------------------------- Producción ----------------------------------------------------------------------------------------------------

    def producir(self, ventana:tk.Frame):
        StartFrame.ventanaPrincipal = ventana
        framePrincipal =  tk.Frame(ventana, bg="blue")
        framePrincipal.pack(fill="both", expand=True, padx=7, pady=7)

        frame1 = tk.Frame(framePrincipal)
        frame1.pack(side="top", fill="x")

        tituloF5 = tk.Label(frame1, text="Producción", bg="medium orchid", relief="ridge", height=2, font=("Arial",16, "bold"))
        tituloF5.pack(fill="both", expand=True) 
        ## relwidth y relheight reciben el porcentaje de tamaño respecto al contenedor

        StartFrame.descripcionF5 = tk.Label(frame1, text="Se registra la producción de prendas y actualiza su inventario: Se toma la cantidad necesaria del stock de materiales para fabricar nuevas prendas y se actualizan los datos, tanto de lo que se descontó de Stock como lo que se agregó a la cantidad de pendas.", height=3,wraplength=800, font=("Arial", 10, "italic"))
        StartFrame.descripcionF5.pack(fill="both", expand=True)

        frame2 = tk.Frame(framePrincipal, bg="white")
        frame2.pack(anchor="s",  expand=True, fill="both")
        StartFrame.frameDeTrabajo = frame2

        descripcion1 = tk.Label(frame2, text="Presiona 'CONTINUAR' para evaluar el estado de la maquinaria disponible en cada sede", wraplength=500, justify="center", font=("Arial", 14, "italic"), bg="white")
        descripcion1.place(relx=0.4, rely=0.16, anchor="center")

        botonContinuar = tk.Button(frame2, text="CONTINUAR", command=lambda : self.activar(frame2, descripcion1, botonContinuar), font=("Arial", 12, "italic"), bg="white")
        botonContinuar.place(relx=0.8, rely=0.16, anchor="center")

        StartFrame.indicaRepMalo = tk.Label(frame2, text="", bg="white")
        StartFrame.indicaRepMalo.place(relx=0.5, rely=0.35, anchor="center")

        return framePrincipal
    
    def activar(self, ventana:tk.Frame, descrip1:tk.Label, botonContinuar:tk.Button):  #creo que al poner varias variables en global no sirve para modificarlas globalmente, verificar
        from src.gestorAplicacion.bodega.maquinaria import Maquinaria
        from src.uiMain.main import Main
        StartFrame.proveedoresQueLlegan = []
        StartFrame.preciosProvQueLlegan = []
        StartFrame.totalGastado = 0
        StartFrame.nomListMaqRev = []
        StartFrame.sedesListMaqRev = []
        StartFrame.senal = 0
        StartFrame.maqDisponibless = []
        StartFrame.nomMaqProdDispSedeP = []
        StartFrame.sedeMaqProdDispSedeP = []
        StartFrame.horasUsoMaqProdDispSedeP = []
        StartFrame.nomMaqProdDispSede2 = []
        StartFrame.sedeMaqProdDispSede2 = []
        StartFrame.horasUsoMaqProdDispSede2 = []
        StartFrame.textIndicador = None
        StartFrame.senalizador = 0
        StartFrame.aProdFinal = []
        StartFrame.aProducirPaEnviar = []
        StartFrame.num3 = 0
        if Sede.getListaSedes()[0].getCantidadInsumosBodega()[0] < 200 or Sede.getListaSedes()[1].getCantidadInsumosBodega()[0] < 200:
            labelDesp = tk.Label(StartFrame.frameDeTrabajo, text="NO HAY INSUMOS SUFICIENTES\nVUELVE CUANDO HAYAS CONSEGUIDO MAS\n\nREDIRIGIENDO...", font=("Arial", 14, "bold italic"), bg="white")
            labelDesp.place(relx=0.5, rely=0.5, anchor="center")
            StartFrame.ventanaPrincipal.after(1500, self.volverMenu2)
            return
        self.buscarProveedor(ventana, descrip1, botonContinuar)

        maqPrueba = Maquinaria("sede")
        threading.Thread(target=maqPrueba.agruparMaquinasDisponibles, args=(Main.fecha,), daemon=True).start()
        
    senal= 0
    def receptor(self, texto):
        StartFrame.senal = StartFrame.senal + 1
        if StartFrame.senal == 1:
            if StartFrame.indicaRepMalo:
                StartFrame.indicaRepMalo.config(text=texto, font=("Arial", 16, "bold"))
                #self.after(100, lambda: StartFrame.indicaRepMalo.config(text=texto, font=("Arial", 16, "bold")))
                #StartFrame.ventanaPrincipal.update_idletasks()
        else:
            if StartFrame.indicaRepMalo:
                StartFrame.indicaRepMalo.config(text=texto, font=("Arial", 16, "bold"))
                StartFrame.indicaRepMalo.place(relx=0.5, rely=0.2, anchor="center")   
                #self.after(100, lambda: StartFrame.indicaRepMalo.config(text=texto, font=("Arial", 16, "bold")))
                #self.after(100, lambda: StartFrame.indicaRepMalo.place(relx=0.5, rely=0.2, anchor="center"))
                #StartFrame.ventanaPrincipal.update_idletasks()

    indicaRepMalo = None
    frameDeTrabajo = None
    proveedorB = None
    botonProveedorB = None
    descripcionF5 = None
    ventanaPrincipal = None

    senal2 = 0
    def buscarProveedor(self, ventana:tk.Frame, descrip1: tk.Label, botonContinuar:tk.Button):
        StartFrame.senal2 = StartFrame.senal2 + 1
        if StartFrame.senal2 == 1:
            StartFrame.botonProveedorB = tk.Button(ventana, text="Consultar", wraplength=250, justify="center", font=("Arial", 12, "bold"), command=lambda : (self.limpieza(ventana, descrip1, botonContinuar, StartFrame.botonProveedorB), self.mostrarProveedorB()))
            StartFrame.botonProveedorB.place(relx=0.5, rely=0.5, anchor="center")
        else:
            StartFrame.botonProveedorB = tk.Button(ventana, text="Consultar", wraplength=250, justify="center", font=("Arial", 12, "bold"), command=lambda : (self.limpieza(ventana, descrip1, botonContinuar, StartFrame.botonProveedorB), self.mostrarProveedorB()))
            StartFrame.botonProveedorB.place(relx=0.5, rely=0.5, anchor="center")
            ventana.bind("<space>", lambda event: self.eliminarBoton(event, StartFrame.botonProveedorB))

            
    def eliminarBoton(self, event, boton):
        boton.destroy()

    senal3 = 0
    def limpieza(self, ventana:tk.Frame, descrip1:tk.Label, botonContinuar:tk.Button, botonProveedorB:tk.Button):
        StartFrame.senal3 = StartFrame.senal3 + 1
        if StartFrame.senal3 == 1:
            descrip1.destroy()
            botonContinuar.destroy()
            botonProveedorB.place_forget()

            StartFrame.indicaRepMalo.place(relx=0.5, rely=0.2, anchor="center")
        else: 
            botonProveedorB.place_forget()


    proveedoresQueLlegan = []
    preciosProvQueLlegan = []
    totalGastado = 0
    def recibeProveedorB(self, proveedorBa):
        from src.gestorAplicacion.bodega.proveedor import Proveedor
        StartFrame.proveedorB = proveedorBa

        if proveedorBa is not None:
            StartFrame.proveedoresQueLlegan.append(proveedorBa.getInsumo().getNombre())
            StartFrame.preciosProvQueLlegan.append(proveedorBa.getPrecio())
            StartFrame.totalGastado += proveedorBa.getPrecio()

    def mostrarProveedorB(self):

        if StartFrame.proveedorB is None:
            StartFrame.indicaRepMalo.destroy()
            self.resultadosRev()
            return
        
        nombreP = tk.Label(StartFrame.frameDeTrabajo, text=StartFrame.proveedorB.getNombre(), font=("Arial", 12, "italic"), bg="white")
        nombreP.place(relx=0.6, rely=0.37)

        nombre = tk.Label(StartFrame.frameDeTrabajo, text="PROVEEDOR BARATO:", bg="white", font=("Arial", 12, "bold italic"))
        nombre.place(relx=0.3, rely=0.37)

        precio = tk.Label(StartFrame.frameDeTrabajo, text="PRECIO:", bg="white", font=("Arial", 12, "bold italic"))
        precio.place(relx=0.35, rely=0.45)
        precioP = tk.Label(StartFrame.frameDeTrabajo, text=str(StartFrame.proveedorB.getPrecio()), font=("Arial", 12, "italic"), bg="white")
        precioP.place(relx=0.6, rely=0.45)
        comprar = tk.Button(StartFrame.frameDeTrabajo, text="COMPRAR REPUESTO", font=("Arial", 13, "bold"))
        comprar.place(relx=0.38, rely=0.61)
        comprar.bind("<Button-1>", lambda event: self.evento(event, nombre, nombreP, precio, precioP))

    def evento(self, event, nombre, nombreP, precio, precioP):
        from src.gestorAplicacion.sede import Sede
        event.widget.destroy()

        separador = ttk.Separator(StartFrame.frameDeTrabajo, orient="horizontal")
        separador.place(relx=0.05, rely=0.55, relwidth=0.9)
        seleccionar = tk.Label(StartFrame.frameDeTrabajo, text="Seleccione la sede desde donde comprará el Repuesto:", bg="white", font=("Arial", 12, "bold"))
        seleccionar.place(relx=0.5, rely=0.63, anchor="center")
        contSedes = tk.Frame(StartFrame.frameDeTrabajo, bg="#E0A8F2", bd=4, relief="ridge")
        contSedes.place(relx=0.5, rely=0.85, anchor="center") #sede Principal
        contSedeP = tk.Frame(contSedes, bg="#E0A8F2", width=100, height=100)
        contSedeP.pack(fill="x", padx=5, pady=5)
        sedePdinero = tk.Label(contSedeP, text=str(Sede.getListaSedes()[0].getCuentaSede().getAhorroBanco()), font=("Arial", 12, "italic"), bg="#E0A8F2")
        sedePdinero.pack(side="right", padx=10, pady=5)
        sedePflecha = tk.Label(contSedeP, text="------------>", bg="#E0A8F2", font=("Arial", 12, "bold"))
        sedePflecha.pack(side="right", pady=5)    
        #sede2
        contSedes2 = tk.Frame(contSedes, bg="#E0A8F2", width=100, height=100)
        contSedes2.pack(fill="x", padx=35, pady=0)
        sede2dinero = tk.Label(contSedes2, text=str(Sede.getListaSedes()[1].getCuentaSede().getAhorroBanco()), font=("Arial", 12, "italic"), bg="#E0A8F2")
        sede2dinero.pack(side="right", padx=10, pady=5)
        sede2flecha = tk.Label(contSedes2, text="------------>", bg="#E0A8F2", font=("Arial", 12, "bold"))
        sede2flecha.pack(side="right", pady=5)
        sedePboton = tk.Button(contSedeP, text="Sede Principal", font=("Arial", 12, "italic"), bd=5, relief="ridge")
        sedePboton.pack(side="right", padx=10, pady=5)
        sedePboton.bind("<Button-1>", lambda event: self.eventoDeCompra(event, nombre, nombreP, precio, precioP, separador, seleccionar, contSedes, contSedeP, sedePdinero, sedePflecha, contSedes2, sede2dinero, sede2flecha, sede2boton))
        sede2boton = tk.Button(contSedes2, text="Sede 2", font=("Arial", 12, "italic"), bd=5, relief="ridge")
        sede2boton.pack(side="right", padx=10, pady=5)
        sede2boton.bind("<Button-1>", lambda event: self.eventoDeCompra(event, nombre, nombreP, precio, precioP, separador, seleccionar, contSedes, contSedeP, sedePdinero, sedePflecha, contSedes2, sede2dinero, sede2flecha, sedePboton))

    def eventoDeCompra(self, event, nombre, nombreP, precio, precioP, separador, seleccionar, contSedes, contSedeP, sedePdinero, sedePflecha, contSedes2, sede2dinero, sede2flecha, botonDeSede):
        from src.gestorAplicacion.sede import Sede
        textoDeBoton = botonDeSede.cget("text")
        StartFrame.indicaRepMalo.place_forget()
        nombre.destroy()
        nombreP.destroy()
        precio.destroy()
        precioP.destroy()
        separador.destroy()
        seleccionar.destroy()
        contSedes.destroy()
        contSedeP.destroy()
        sedePdinero.destroy()
        sedePflecha.destroy()
        contSedes2.destroy()
        sede2dinero.destroy()
        sede2flecha.destroy()
        botonDeSede.destroy()
        event.widget.destroy()

        if textoDeBoton == "Sede 2":
            labelDeCompraP = tk.Label(StartFrame.frameDeTrabajo, text=f"El repuesto {StartFrame.proveedorB.getInsumo().getNombre()} se compró exitosamente desde la Sede Principal", wraplength=600, font=("Arial", 18, "bold"), bg="white")
            labelDeCompraP.place(relx=0.5, rely=0.2, anchor="center")
            Sede.getListaSedes()[0].getCuentaSede().setAhorroBanco( (Sede.getListaSedes()[0].getCuentaSede().getAhorroBanco() - StartFrame.proveedorB.getPrecio()) )
            labelSaldo = tk.Label(StartFrame.frameDeTrabajo, text= f"Saldo Disponible: {Sede.getListaSedes()[0].getCuentaSede().getAhorroBanco()} pesos", font=("Arial", 14, "italic"), bg="white")
            labelSaldo.place(relx=0.5, rely=0.4, anchor="center")

            seguirAnalisis = tk.Button(StartFrame.frameDeTrabajo, text="Continuar Análisis", font=("Arial", 12, "bold"), bd=5, relief="ridge")
            seguirAnalisis.place(relx=0.5, rely=0.6, anchor="center")
            seguirAnalisis.bind("<Button-1>", lambda event: self.eventoContinuador(event, labelDeCompraP, labelSaldo))

        else:
            labelDeCompraP = tk.Label(StartFrame.frameDeTrabajo, text=f"El repuesto {StartFrame.proveedorB.getInsumo().getNombre()} se compró exitosamente desde la Sede 2", wraplength=600, font=("Arial", 18, "bold"), bg="white")
            labelDeCompraP.place(relx=0.5, rely=0.2, anchor="center")
            Sede.getListaSedes()[1].getCuentaSede().setAhorroBanco( (Sede.getListaSedes()[1].getCuentaSede().getAhorroBanco() - StartFrame.proveedorB.getPrecio()) )
            labelSaldo = tk.Label(StartFrame.frameDeTrabajo, text= f"Saldo Disponible: {Sede.getListaSedes()[1].getCuentaSede().getAhorroBanco()} pesos", font=("Arial", 14, "italic"), bg="white")
            labelSaldo.place(relx=0.5, rely=0.4, anchor="center")

            seguirAnalisis = tk.Button(StartFrame.frameDeTrabajo, text="Continuar Análisis", font=("Arial", 12, "bold"), bd=5, relief="ridge")
            seguirAnalisis.place(relx=0.5, rely=0.6, anchor="center")
            seguirAnalisis.bind("<Button-1>", lambda event: self.eventoContinuador(event, labelDeCompraP, labelSaldo))
            
        
    def eventoContinuador(self, event, labelDeCompra, labelSaldo):
        from src.uiMain.main import Main

        labelDeCompra.destroy()
        labelSaldo.destroy()
        event.widget.destroy()
        Main.evento_ui.set()
        #print(StartFrame.proveedorB)
        self.buscarProveedor(StartFrame.frameDeTrabajo, 1, 1)

    nomListMaqRev = []
    sedesListMaqRev = []
    def recibeMaqPaRevisar(self, listMaquinasRev):
        from src.gestorAplicacion.bodega.maquinaria import Maquinaria

        for maq in listMaquinasRev:
            StartFrame.nomListMaqRev.append(maq.getNombre())
            StartFrame.sedesListMaqRev.append(maq.getSede().getNombre())
        

    def resultadosRev(self):
        from src.uiMain.fieldFrame import FieldFrame
        
        criterios = StartFrame.proveedoresQueLlegan
        #print(f"\nlos proveedores que llegaron fueron: {len(StartFrame.proveedoresQueLlegan)}")
        valores = StartFrame.preciosProvQueLlegan
        habilitado = [False for _ in range(len(StartFrame.proveedoresQueLlegan))]

        containerBig = tk.Frame(StartFrame.frameDeTrabajo, bg="white")
        containerBig.pack(pady=10)

        cont = tk.Frame(containerBig, bg="medium orchid")
        cont.pack(side="left", pady=20)
        
        field_frame = FieldFrame(cont, "Los repuestos comprados fueron:", criterios, "", valores, habilitado)
        field_frame.pack(padx=10, pady=10)

        labelTotalGastado = tk.Label(cont, text=f"Total gastado: {StartFrame.totalGastado} pesos", font=("Arial", 12, "italic"))
        labelTotalGastado.pack(pady=10)

        criterios2 = StartFrame.nomListMaqRev
        valores2 = StartFrame.sedesListMaqRev
        habilitado2 = [False for _ in range(len(StartFrame.nomListMaqRev))]

        cont2 = tk.Frame(containerBig, bg="medium orchid")
        cont2.pack(side="left", pady=20, padx=5)
        
        field_frame2 = FieldFrame(cont2, "Maquinas inhabilidas\npor falta de revisión:", criterios2, "", valores2, habilitado2)
        field_frame2.pack(padx=10, pady=10)

        #labelTotalGastado = tk.Label(cont, text=f"Total gastado: {totalGastado} pesos", font=("Arial", 12, "italic"))
        #labelTotalGastado.pack(pady=10)

        botonInt2 = tk.Button(StartFrame.frameDeTrabajo, text="Maquinaria Disponible", font=("Arial", 12, "bold italic"))
        botonInt2.pack(pady=4)
        botonInt2.bind("<Button-1>", lambda event: self.inicioInt2(event, containerBig, cont, field_frame, labelTotalGastado, cont2, field_frame2))

    maqDisponibless = []

    def recibeMaqDisp(self, maqDisponibles):
        StartFrame.maqDisponibless = maqDisponibles

    nomMaqProdDispSedeP = []
    sedeMaqProdDispSedeP = []
    horasUsoMaqProdDispSedeP = []
    nomMaqProdDispSede2 = []
    sedeMaqProdDispSede2 = []
    horasUsoMaqProdDispSede2 = []
    
    def recibeMaqDispSeparadas(self, maqProdSedeP, maqProdSede2):
        for maquinasSedeP in maqProdSedeP:
            StartFrame.nomMaqProdDispSedeP.append(maquinasSedeP.getNombre())
            StartFrame.sedeMaqProdDispSedeP.append(maquinasSedeP.getSede().getNombre())
            StartFrame.horasUsoMaqProdDispSedeP.append(maquinasSedeP.getHorasUso())
        for maquinasSede2 in maqProdSede2:
            StartFrame.nomMaqProdDispSede2.append(maquinasSede2.getNombre())
            StartFrame.sedeMaqProdDispSede2.append(maquinasSede2.getSede().getNombre())
            StartFrame.horasUsoMaqProdDispSede2.append(maquinasSede2.getHorasUso())
        StartFrame.even2.set()

    textIndicador = None
    senalizador = 0
    evento_senalizador = threading.Event()
    even2 = threading.Event()
    def recibeTextIndicador(self, textRecibido, senal):
        StartFrame.textIndicador = textRecibido
        StartFrame.senalizador = senal
        StartFrame.evento_senalizador.set()

    def inicioInt2(self, event, containerBig, cont, field_frame, labelTG, cont2, field_frame2):
        from src.uiMain.fieldFrame import FieldFrame
        from src.gestorAplicacion.sede import Sede
        from src.uiMain.main import Main
        containerBig.destroy()
        cont.destroy()
        field_frame.destroy()
        labelTG.destroy()
        cont2.destroy()
        field_frame2.destroy()
        event.widget.destroy()
        StartFrame.frameDeTrabajo.config(bg="white")
        threading.Thread(target=Sede.planProduccion, args=(StartFrame.maqDisponibless, Main.fecha), daemon=True).start()

        StartFrame.even2.wait()
        StartFrame.even2.clear()
        criterios = StartFrame.nomMaqProdDispSedeP
        #print(f"\nlas maq disponiles en la sede p son: {len(StartFrame.nomMaqProdDispSedeP)}")
        valores = StartFrame.horasUsoMaqProdDispSedeP
        habilitado = [False for _ in range(len(StartFrame.nomMaqProdDispSedeP))]

        containerBig = tk.Frame(StartFrame.frameDeTrabajo, bg="white")
        containerBig.pack(pady=2)

        StartFrame.evento_senalizador.wait()
        StartFrame.evento_senalizador.clear()
        
        if StartFrame.senalizador == 2 or StartFrame.senalizador == 4:
            cont = tk.Frame(containerBig, bg="gray")
            cont.pack(side="left", padx=5, pady=10)
        else:
            cont = tk.Frame(containerBig, bg="medium orchid")
            cont.pack(side="left", padx=5, pady=10)
        
        field_frame = FieldFrame(cont, "Sede Principal", criterios, "", valores, habilitado)
        field_frame.pack(padx=10, pady=10)

        criterios2 = StartFrame.nomMaqProdDispSede2
        valores2 = StartFrame.horasUsoMaqProdDispSede2
        habilitado2 = [False for _ in range(len(StartFrame.nomMaqProdDispSede2))]

        if StartFrame.senalizador == 1 or StartFrame.senalizador == 4:
            cont2 = tk.Frame(containerBig, bg="gray")
            cont2.pack(side="left", padx=5,pady=10)
        else:
            cont2 = tk.Frame(containerBig, bg="medium orchid")
            cont2.pack(side="left", padx=5,pady=10)
        
        field_frame2 = FieldFrame(cont2, "Sede 2", criterios2, "", valores2, habilitado2)
        field_frame2.pack(padx=10, pady=10)

        contLabelYBoton = tk.Frame(StartFrame.frameDeTrabajo, bg="white")
        contLabelYBoton.pack(pady=1)

        labelTextIndicador = tk.Label(contLabelYBoton, text=StartFrame.textIndicador, font=("Arial", 14, "bold"), bg="white", wraplength=600)
        labelTextIndicador.pack(pady=0)

        btnPlanificarProd = tk.Button(StartFrame.frameDeTrabajo, text="Planificar Produccion", font=("Arial", 12, "bold italic"))
        
        if StartFrame.senalizador == 2:
            btnPlanificarProd.bind("<Button-1>", lambda event: self.planProduccionn(event, containerBig, contLabelYBoton, 1))
        elif StartFrame.senalizador == 1:
            btnPlanificarProd.bind("<Button-1>", lambda event: self.planProduccionn(event, containerBig, contLabelYBoton, 2))
        elif StartFrame.senalizador == 3:
            btnPlanificarProd.bind("<Button-1>", lambda event: self.planProduccionn(event, containerBig, contLabelYBoton, 3))
        elif StartFrame.senalizador == 4:
            # Cuando ninguna sede esta disponible, entonces aqui se debe crear un boton pa volver
            btnPlanificarProd.config(text="Volver al inicio")
            btnPlanificarProd.bind("<Button-1>", self.volverMenu)
        
        btnPlanificarProd.pack(pady=5)

    def volverMenu(self, event):
        from src.uiMain.startFrame import StartFrame
        stff = StartFrame()
        ventana = event.widget.winfo_toplevel()
        stff.cambiarFrame(stff.areaPrincipal)
        ventana.destroy()
    
    def volverMenu2(self):
        from src.uiMain.startFrame import StartFrame
        stff = StartFrame()
        stff.cambiarFrame(stff.areaPrincipal)
        StartFrame.ventanaPrincipal.destroy()

    aProdFinal = []
    def recibeProdFinal(self, aProdF):
        tempProd = []
        for listas1 in aProdF:
            for listas2 in listas1:
                for listas3 in listas2:
                    tempProd.append(listas3)
        #print("\n",len(tempProd) , f"- la produccion en una sola lista es: {tempProd}\n")
        StartFrame.aProdFinal.append(tempProd[0]); StartFrame.aProdFinal.append(tempProd[1]); StartFrame.aProdFinal.append(tempProd[4]); StartFrame.aProdFinal.append(tempProd[5])
        StartFrame.aProdFinal.append(tempProd[2]); StartFrame.aProdFinal.append(tempProd[3]); StartFrame.aProdFinal.append(tempProd[6]); StartFrame.aProdFinal.append(tempProd[7])
        #print("\n",len(StartFrame.aProdFinal) , f"- la produccion cruzada en una sola lista es: {StartFrame.aProdFinal}\n")
        StartFrame.evento_senalizador.set()

    enlacesP = [(0, 2), (0, 4), (0, 6)] ; enlacesPSede2 = [(4, 6)]
    enlacesC = [(1, 3), (1, 5), (1, 7)] ; enlacesCSede2 = [(5, 7)]
    indiceEnlaceP = 0
    indiceEnlaceC = 0
    direccion = False
    modoP = True
    idx1, idx2 = enlacesP[indiceEnlaceP]
    idx3, idx4 = enlacesPSede2[0]
    def planProduccionn(self, event, containerBig, contLyB, indicador):
        from src.uiMain.main import Main
        containerBig.destroy()
        contLyB.destroy()
        StartFrame.descripcionF5.destroy()
        event.widget.destroy()
        StartFrame.frameDeTrabajo.config(bg="white")
        contBigRecor = tk.Frame(StartFrame.frameDeTrabajo)
        contBigRecor.pack(fill="x")

        
        contRe1 = tk.Frame(contBigRecor)
        contRe1.pack(pady=3)
        recorderis = tk.Label(contRe1, text="Si en la produccion de hoy\nhay mas de 400 prendas por modista:", font=("Arial", 10, "bold italic"))
        recorderis.pack(side="left", padx=10, pady=2)
        textRecorderis = tk.Label(contRe1, text="Sobre costo = 5000 x prenda\n(para las prendas que excedan)", font=("Arial", 10, "italic"))
        textRecorderis.pack(side="left", padx=10, pady=2)
        #separador
        separador = ttk.Separator(contBigRecor, orient="horizontal")
        separador.pack(fill="x", padx=50)
        contRe2 = tk.Frame(contBigRecor)
        contRe2.pack(pady=3)
        recorderis2 = tk.Label(contRe2, text="Si en la produccion de la otra semana\nhay mas de 400 prendas por modista:", font=("Arial", 10, "bold italic"))
        recorderis2.pack(side="left", padx=10, pady=2)
        textRecorderis2 = tk.Label(contRe2, text="Sobre costo = 2500 x prenda\n(para las prendas que excedan)", font=("Arial", 10, "italic"))
        textRecorderis2.pack(side="left", padx=10, pady=2)

        Main.evento_ui.set()
                #CAMBIAR PRODUCCION A GUSTO
        StartFrame.evento_senalizador.wait()
        StartFrame.evento_senalizador.clear()
        varEntries = [tk.StringVar(value=str(StartFrame.aProdFinal[x])) for x in range(8)]
        #print(f"\nvalores de entrada de la interfaz: {[int(var.get()) for var in varEntries]}")
        entries = []
        flechas = []
        varIntermedio = tk.StringVar()

        def confirmarProduccion(event):
            from tkinter import messagebox
            from src.gestorAplicacion.sede import Sede
            from src.uiMain.fieldFrame import FieldFrame
            from src.gestorAplicacion.bodega.prenda import Prenda
            listSobreCostos = calcularSobreCostos()
            produccionPaEnviar()
            respuesta = messagebox.askyesno("Confirmación", f"¿Deseas continuar?\n\n* Sobre Costo de la Sede Principal = {listSobreCostos[0]}\n* Sobre Costo de la Sede 2 = {listSobreCostos[1]}")
            
            if respuesta:
                #print("El usuario eligió continuar.")
                contBigRecor.destroy() ; contRe1.destroy() ; recorderis.destroy() ; textRecorderis.destroy() ; separador.destroy()
                contRe2.destroy() ; recorderis2.destroy() ; textRecorderis2.destroy() ; frameGeneral.destroy() ; frameIzq.destroy() ; frameDer.destroy()
                for subf in subframes:
                    subf.destroy()
                frameBotones.destroy() ; frameEntry.destroy()
                StartFrame.ventanaPrincipal.after(100, self.inicioInt3)

            else:
                #print("El usuario canceló la acción.")
                pass

        def produccionPaEnviar():
            valores = [int(modificados.get()) for modificados in varEntries]
            list1 = [valores[0], valores[1]] ; list2 = [valores[4], valores[5]] ; listProdHoy = [list1, list2]
            list3 = [valores[2], valores[3]] ; list4 = [valores[6], valores[7]] ; listProdOWeek = [list3, list4]
            StartFrame.aProducirPaEnviar.append(listProdHoy) ; StartFrame.aProducirPaEnviar.append(listProdOWeek)
            #print(f"\nproduccion pa enviar: {StartFrame.aProducirPaEnviar}")

        def calcularSobreCostos():
            import math
            sedesSC = []
            valores = [int(modificados.get()) for modificados in varEntries]
            prendasSCHoySedeP = math.floor((valores[0] + valores[1]) / 6)
            dinero1SedeP = prendasSCHoySedeP * 5000
            prendasSCMSedeP = math.floor((valores[2] + valores[3]) / 6)
            dinero2SedeP = prendasSCMSedeP * 2500
            sobreCostoTotalSedeP = dinero1SedeP + dinero2SedeP

            prendasSCHoySede2 = math.floor((valores[4] + valores[5]) / 6)
            dinero1Sede2 = prendasSCHoySede2 * 5000
            prendasSCMSede2 = math.floor((valores[6] + valores[7]) / 6)
            dinero2Sede2 = prendasSCMSede2 * 2500
            sobreCostoTotalSede2 = dinero1Sede2 + dinero2Sede2

            sedesSC = [sobreCostoTotalSedeP, sobreCostoTotalSede2]
            return sedesSC

        def actualizarValores(event=None):
            global direccion, idx1, idx2, idx3, idx4
            try:
                valorIntermedio = int(varIntermedio.get()) if varIntermedio.get() else 0
                if indicador == 3 or indicador == 2:
                    val1 = int(varEntries[StartFrame.idx1].get())
                    val2 = int(varEntries[StartFrame.idx2].get())
                elif indicador == 1:
                    val1 = int(varEntries[StartFrame.idx3].get())
                    val2 = int(varEntries[StartFrame.idx4].get())

                if StartFrame.direccion: 
                    if val2 - valorIntermedio < 0:
                        valorIntermedio = val2
                    if indicador == 3 or indicador == 2:
                        varEntries[StartFrame.idx1].set(str(val1 + valorIntermedio))
                        varEntries[StartFrame.idx2].set(str(val2 - valorIntermedio))
                    elif indicador == 1:
                        varEntries[StartFrame.idx3].set(str(val1 + valorIntermedio))
                        varEntries[StartFrame.idx4].set(str(val2 - valorIntermedio))
                else:  
                    if val1 - valorIntermedio < 0:
                        valorIntermedio = val1
                    if indicador == 3 or indicador == 2:
                        varEntries[StartFrame.idx1].set(str(val1 - valorIntermedio))
                        varEntries[StartFrame.idx2].set(str(val2 + valorIntermedio))
                    elif indicador == 1:
                        varEntries[StartFrame.idx3].set(str(val1 - valorIntermedio))
                        varEntries[StartFrame.idx4].set(str(val2 + valorIntermedio))

                varIntermedio.set("")  # Limpiar Entry intermedio
            except ValueError:
                pass  # Ignorar valores no numéricos

        def cambiarEnlaceP():
            StartFrame.modoP = True  # Activar modo "cambiarP"
            StartFrame.idx1, StartFrame.idx2 = StartFrame.enlacesP[StartFrame.indiceEnlaceP]  # Actualizar índices
            StartFrame.idx3, StartFrame.idx4 = StartFrame.enlacesPSede2[0]
            if indicador == 3:
                StartFrame.indiceEnlaceP = (StartFrame.indiceEnlaceP + 1) % len(StartFrame.enlacesP)
            actualizarFlechas()

        def cambiarEnlaceC():
            StartFrame.modoP = False  # Activar modo "cambiarC"
            StartFrame.idx1, StartFrame.idx2 = StartFrame.enlacesC[StartFrame.indiceEnlaceC]  # Actualizar índices
            StartFrame.idx3, StartFrame.idx4 = StartFrame.enlacesCSede2[0]
            if indicador == 3:
                StartFrame.indiceEnlaceC = (StartFrame.indiceEnlaceC + 1) % len(StartFrame.enlacesC)
            actualizarFlechas()

        def cambiarDireccion():
            StartFrame.direccion = not StartFrame.direccion
            actualizarFlechas()

        def actualizarFlechas():
            for label in flechas:
                label.config(text="")
            if indicador == 3 or indicador == 2:
                flechas[StartFrame.idx1].config(text="⬅" if StartFrame.direccion else "➡")
                flechas[StartFrame.idx2].config(text="➡" if not StartFrame.direccion else "⬅")
            elif indicador == 1:
                flechas[StartFrame.idx3].config(text="⬅" if StartFrame.direccion else "➡")
                flechas[StartFrame.idx4].config(text="➡" if not StartFrame.direccion else "⬅")

        def onFocusIn(event):
            if event.widget.get() == "Modifica aquí...":
                event.widget.delete(0, tk.END)
                event.widget.config(fg="black")

        def onFocusOut(event):
            if event.widget.get() == "":
                event.widget.insert(0, "Modifica aquí...")
                event.widget.config(fg="gray")
            # Contenedores principales con títulos
        frameGeneral = tk.Frame(StartFrame.frameDeTrabajo, bg="white")
        frameGeneral.pack(pady=10)

        if indicador == 1: # Sede Principal no disponible
            frameIzq = tk.LabelFrame(frameGeneral, text="Sede Principal", padx=17, pady=3, bg="light gray", font=("Arial", 14, "bold italic"))
        elif indicador != 1 and indicador != 4:
            frameIzq = tk.LabelFrame(frameGeneral, text="Sede Principal", padx=17, pady=3, bg="#E0A8F2", font=("Arial", 14, "bold italic"))
        else:   # Para cuando es 4 el indicador ( es decir, ninguna sede esta disponible )
            frameIzq = tk.LabelFrame(frameGeneral, text="Sede Principal", padx=17, pady=3, bg="light gray", font=("Arial", 14, "bold italic"))

        if indicador == 2: # Sede 2 no disponible
            frameDer = tk.LabelFrame(frameGeneral, text="Sede 2", padx=17, pady=3, bg="light gray", font=("Arial", 14, "bold italic"))
        elif indicador != 2 and indicador != 4:
            frameDer = tk.LabelFrame(frameGeneral, text="Sede 2", padx=17, pady=3, bg="#E0A8F2", font=("Arial", 14, "bold italic"))
        else:   # Para cuando es 4 el indicador ( es decir, ninguna sede esta disponible )
            frameDer = tk.LabelFrame(frameGeneral, text="Sede 2", padx=17, pady=3, bg="light gray", font=("Arial", 14, "bold italic"))
        frameIzq.pack(side=tk.LEFT, padx=10)
        frameDer.pack(side=tk.RIGHT, padx=10)

        # Crear los sub-frames (cada uno contiene 2 Entry)
        subframes = []
        labels = ["Comenzar\nproducción", "Producir la\notra semana", "Comenzar\nproducción", "Producir la\notra semana"]
        for i in range(4):
            frame = tk.Frame(frameIzq if i < 2 else frameDer, padx=12, pady=7, bg="#E6E6FA")
            frame.pack(side=tk.LEFT, padx=12, pady=7)
            label = tk.Label(frame, text=labels[i], font=("Arial", 12, "bold"), bg="#E6E6FA")
            label.pack(pady=5)
            subframes.append(frame)

        # Crear los Entry, flechas y etiquetas "PANTALÓN" y "CAMISA"
        for i in range(8):
            text = "Pantalones" if i % 2 == 0 else "Camisas"
            etiqueta = tk.Label(subframes[i // 2], text=text, font=("Arial", 10, "bold"), bg="#E6E6FA")
            etiqueta.pack(pady=2)

            frameEntry = tk.Frame(subframes[i // 2])
            frameEntry.pack()
            
            flecha = tk.Label(frameEntry, text="", font=("Arial", 12))
            flecha.pack(side=tk.LEFT)
            flechas.append(flecha)
            
            entry = tk.Entry(frameEntry, textvariable=varEntries[i], width=10, justify="center", state="readonly")
            entry.pack(side=tk.LEFT)
            entries.append(entry)

        # Contenedor de botones
        frameBotones = tk.Frame(StartFrame.frameDeTrabajo, bg="white")
        frameBotones.pack(pady=5)

        botonModificarP = tk.Button(frameBotones, text="Modificar Pantalones", command=cambiarEnlaceP, font=("Arial", 11, "bold italic"), bg="light gray")
        entryIntermedio = tk.Entry(frameBotones, textvariable=varIntermedio, width=15, justify="center", font=("Arial", 11), fg="gray", bg="light gray")
        entryIntermedio.insert(0, "Modifica aquí...")  # Texto inicial
        entryIntermedio.bind("<FocusIn>", onFocusIn)
        entryIntermedio.bind("<FocusOut>", onFocusOut)
        entryIntermedio.bind("<Return>", actualizarValores)
        botonCambiarC = tk.Button(frameBotones, text="Modificar Camisas", command=cambiarEnlaceC, font=("Arial", 11, "bold italic"))

        botonModificarP.pack(side=tk.LEFT, padx=15, pady=1)
        entryIntermedio.pack(side=tk.LEFT, padx=15, pady=1)
        botonCambiarC.pack(side=tk.LEFT, padx=15, pady=1)

        # Entry para ingresar cantidad
        frameEntry = tk.Frame(StartFrame.frameDeTrabajo, bg="white")
        frameEntry.pack(pady=10)
        botonCambiarDir = tk.Button(frameEntry, text="Cambiar Dirección", command=cambiarDireccion, font=("Arial", 11, "bold italic"))
        botonCambiarDir.pack(side="left", padx=15)
        botonContinue = tk.Button(frameEntry, text="CONTINUAR", font=("Arial", 13, "bold italic"))
        botonContinue.pack(side="left", padx=15)
        botonContinue.bind("<Button-1>", confirmarProduccion)

        # Iniciar con los primeros enlaces resaltados
        cambiarEnlaceP()

    aProducirPaEnviar = []
    creadas = None
    def recibeCreadasOrNo(self, creadasss):
        from src.gestorAplicacion.bodega.prenda import Prenda
        StartFrame.creadas = creadasss
        #StartFrame.indicaRepMalo = None
        if not Prenda.prendasUltimaProduccion:
            #print("\nADIOS...")
            StartFrame.ventanaPrincipal.after(700, self.volverMenu2)
            return
        
        StartFrame.contenedorGrande.destroy()
        resultado = None

        prendasHoy = [] ; hoySedeP = [] ; hoySede2 = [] ; pHoySedeP = [] ; pHoySede2 = [] ; cHoySedeP = [] ; cHoySede2 = []
        prendasOW = [] ; OWSedeP = [] ; OWSede2 = [] ; pOWSedeP = [] ; pOWSede2 = [] ; cOWSedeP = [] ; cOWSede2 = []
        diaRef = Prenda.prendasUltimaProduccion[0].getFecha().getDia()
        #print(f"dia de referencia: {diaRef}")
        for prendaPorFecha in Prenda.prendasUltimaProduccion:
            if prendaPorFecha.getFecha().getDia() == diaRef:
                prendasHoy.append(prendaPorFecha)
            else:
                prendasOW.append(prendaPorFecha)
        #print(f"Numero de producidas hoy: {len(prendasHoy)}, numero de producidas la otra semana: {len(prendasOW)}")
        for lodelaP in prendasHoy:
            if lodelaP.getSede().getNombre().lower() == "sede principal":
                hoySedeP.append(lodelaP)
            else:
                hoySede2.append(lodelaP)
        for lodelaP2 in prendasOW:
            if lodelaP2.getSede().getNombre().lower() == "sede principal":
                OWSedeP.append(lodelaP2)
            else:
                OWSede2.append(lodelaP2)
        #TENIENDO LA PRODUCCION DE HOY Y DE LA OTRA SEMANA SEPARADAS, vamos separar por pantalones y camisas...
        for prendaEs in hoySedeP:
            if prendaEs.getNombre().lower() == "pantalon":
                pHoySedeP.append(prendaEs)
            else:
                cHoySedeP.append(prendaEs)
        for prendaEs2 in hoySede2:
            if prendaEs2.getNombre().lower() == "pantalon":
                pHoySede2.append(prendaEs2)
            else:
                cHoySede2.append(prendaEs2)
        for prendaEs3 in OWSedeP:
            if prendaEs3.getNombre().lower() == "pantalon":
                pOWSedeP.append(prendaEs3)
            else:
                cOWSedeP.append(prendaEs3)
        for prendaEs4 in OWSede2:
            if prendaEs4.getNombre().lower() == "pantalon":
                pOWSede2.append(prendaEs4)
            else:
                cOWSede2.append(prendaEs4)
        
        #print(f"\n[{len(pHoySedeP)}, {len(cHoySedeP)}, {len(pHoySede2)}, {len(cHoySede2)} --- {len(pOWSedeP)}, {len(cOWSedeP)}, {len(pOWSede2)}, {len(cOWSede2)}]")

        contCONTENEDOR = tk.Frame(StartFrame.frameDeTrabajo, bg="white", relief="ridge", bd=4)
        contCONTENEDOR.pack(pady=20)

        contARRIBA = tk.Frame(contCONTENEDOR, bg="#E0A8F2")
        contARRIBA.pack(side="left", pady=5, padx=5)

        labelProdSal = tk.Label(contARRIBA, text="PRODUCCIÓN\nSALIENTE", font=("Arial", 15, "bold italic"), bg="#E0A8F2")
        labelProdSal.pack(pady=7)

        contSEDES = tk.Frame(contARRIBA, bg="#E0A8F2")
        contSEDES.pack(pady=2, padx=20)

        contSedeP = tk.Frame(contSEDES, bg="#E6E6FA")
        contSedeP.pack(side="left", padx=10, pady=5)

        contSede2 = tk.Frame(contSEDES, bg="#E6E6FA")
        contSede2.pack(side="left", padx=10, pady=5)

        label1 = tk.Label(contSedeP, bg="#E6E6FA", text="Sede Principal", font=("Arial", 13, "bold italic"))
        label1.pack(pady=4, padx=4)

        label2 = tk.Label(contSedeP, bg="#E6E6FA", text=f"Pantalones: {len(pHoySedeP)}", font=("Arial", 10, "italic"))
        label2.pack(pady=2, padx=4)

        label3 = tk.Label(contSedeP, bg="#E6E6FA", text=f"Camisas: {len(cHoySedeP)}", font=("Arial", 10, "italic"))
        label3.pack(pady=2, padx=4)

        label4 = tk.Label(contSede2, bg="#E6E6FA", text="Sede 2", font=("Arial", 11, "bold italic"))
        label4.pack(pady=4, padx=4)

        label5 = tk.Label(contSede2, bg="#E6E6FA", text=f"Pantalones: {len(pHoySede2)}", font=("Arial", 10, "italic"))
        label5.pack(pady=2, padx=4)

        label6 = tk.Label(contSede2, bg="#E6E6FA", text=f"Camisas: {len(cHoySede2)}", font=("Arial", 10, "italic"))
        label6.pack(pady=2, padx=4)

            #resultados de lo de la otra semana...
        contDERECHA = tk.Frame(contCONTENEDOR, bg="#E0A8F2")
        contDERECHA.pack(side="left", pady=5, padx=5)

        labelProdSal2 = tk.Label(contDERECHA, text="PRODUCCIÓN LANZADA\nLA OTRA SEMANA", font=("Arial", 15, "bold italic"), bg="#E0A8F2")
        labelProdSal2.pack(pady=7)

        contSEDES2 = tk.Frame(contDERECHA, bg="#E0A8F2")
        contSEDES2.pack(pady=2, padx=20)

        contSedeP2 = tk.Frame(contSEDES2, bg="#E6E6FA")
        contSedeP2.pack(side="left", padx=10, pady=5)

        contSede22 = tk.Frame(contSEDES2, bg="#E6E6FA")
        contSede22.pack(side="left", padx=10, pady=5)

        label12 = tk.Label(contSedeP2, bg="#E6E6FA", text="Sede Principal", font=("Arial", 13, "bold italic"))
        label12.pack(pady=4, padx=4)

        label22 = tk.Label(contSedeP2, bg="#E6E6FA", text=f"Pantalones: {len(pOWSedeP)}", font=("Arial", 10, "italic"))
        label22.pack(pady=2, padx=4)

        label32 = tk.Label(contSedeP2, bg="#E6E6FA", text=f"Camisas: {len(cOWSedeP)}", font=("Arial", 10, "italic"))
        label32.pack(pady=2, padx=4)

        label42 = tk.Label(contSede22, bg="#E6E6FA", text="Sede 2", font=("Arial", 11, "bold italic"))
        label42.pack(pady=4, padx=4)

        label52 = tk.Label(contSede22, bg="#E6E6FA", text=f"Pantalones: {len(pOWSede2)}", font=("Arial", 10, "italic"))
        label52.pack(pady=2, padx=4)

        label62 = tk.Label(contSede22, bg="#E6E6FA", text=f"Camisas: {len(cOWSede2)}", font=("Arial", 10, "italic"))
        label62.pack(pady=2, padx=4)


        if creadasss:
            resultado = f"{Prenda.getCantidadUltimaProduccion()} Prendas creadas con éxito"
        else:
            resultado = f"No se pudo producir todo porque los insumos no alcanzaron, producimos {Prenda.getCantidadUltimaProduccion()} prendas"
        
        labelResultado = tk.Label(StartFrame.frameDeTrabajo, text=resultado, bg="white", font=("Arial", 18, "bold italic"), wraplength=500, justify="center")
        labelResultado.pack(pady=15)

        botonVOLVER = tk.Button(StartFrame.frameDeTrabajo, text="Volver al Menu", font=("Arial", 16, "bold italic"))
        botonVOLVER.pack(pady=10)
        botonVOLVER.bind("<Button-1>", self.volverMenu)

        for maquina in Sede.getListaSedes()[0].maqProduccion:
            if maquina.mantenimiento is False:
                if maquina.getHoraRevision() - maquina.getHorasUso() <= 0:
                    maquina.mantenimiento = True
                    maquina.ultFechaRevision = Main.fecha
        for maquina in Sede.getListaSedes()[1].maqProduccion:
            if maquina.mantenimiento is False:
                if maquina.getHoraRevision() - maquina.getHorasUso() <= 0:
                    maquina.mantenimiento = True
                    maquina.ultFechaRevision = Main.fecha

        
    contenedorGrande = None
    def inicioInt3(self):
        from src.gestorAplicacion.bodega.prenda import Prenda
        from src.uiMain.main import Main
        from src.gestorAplicacion.sede import Sede
        from src.uiMain.fieldFrame import FieldFrame

        criterios1 = [] ; criterios2 = [] ; valores1 = [] ; valores2 = []
        #print("\nComienzo de la interacción 3...")
        #print(f"\n Lista de insumos actual de la sede Principal: {Sede.getListaSedes()[0].getListaInsumosBodega()}, su cantidad: {Sede.getListaSedes()[0].getCantidadInsumosBodega()}")
        #print(f"\n Lista de insumos actual de la sede 2: {Sede.getListaSedes()[1].getListaInsumosBodega()}, su cantidad: {Sede.getListaSedes()[1].getCantidadInsumosBodega()}\n")
        #contenedorGrande = tk.Frame(frameDeTrabajo, bg="light gray")
        #contenedorGrande.pack(pady=5)

        StartFrame.contenedorGrande = tk.Frame(StartFrame.frameDeTrabajo, bg="light gray")
        StartFrame.contenedorGrande.pack(pady=5)

            # CONTENEDOR IZQUIERDA ------------------------------------------------------------------------
        contenedorInsumos = tk.Frame(StartFrame.contenedorGrande, bg="white")
        contenedorInsumos.pack(side="left", padx=5, pady=5)
            #field Frame de los insumos disponibles en sede Principal
        for insumosProd in Sede.getListaSedes()[0].getListaInsumosBodega():
            if insumosProd.getNombre() != "Bolsa":
                criterios1.append(insumosProd)
        for index1, valor1 in enumerate(criterios1):
            valores1.append(Sede.getListaSedes()[0].getCantidadInsumosBodega()[index1])
        habilitado1 = [False for _ in range(len(criterios1))]

        ffInsumosSedeP = FieldFrame(contenedorInsumos, "Insumos que hay en\nla Sede Principal", criterios1, "", valores1, habilitado1)
        ffInsumosSedeP.pack(pady=2)
        
            #field Frame de los insumos disponibles en sede 2
        for insumosProd2 in Sede.getListaSedes()[1].getListaInsumosBodega():
            if insumosProd2.getNombre() != "Bolsa":
                criterios2.append(insumosProd2)
        for index2, valor2 in enumerate(criterios2):
            valores2.append(Sede.getListaSedes()[1].getCantidadInsumosBodega()[index2])
        habilitado2 = [False for _ in range(len(criterios2))]

        ffInsumosSede2 = FieldFrame(contenedorInsumos, "Insumos que hay en\nla Sede 2", criterios2, "", valores2, habilitado2)
        ffInsumosSede2.pack(pady=2)
        StartFrame.frameDeTrabajo.update_idletasks()
            #CONTENEDOR DERECHA ----------------------------------------------------------------------------
        StartFrame.contSeleccionModista = tk.Frame(StartFrame.contenedorGrande, bg="white")
        StartFrame.contSeleccionModista.pack(side="left", padx=5, pady=5)
        StartFrame.frameDeTrabajo.update_idletasks()
        StartFrame.labelPrueba = tk.Label(StartFrame.contSeleccionModista, text="No hay insumos :(\n\ncompra mas para producir\n\nvolviendo...", font=("Arial", 10, "bold italic"), wraplength=300, justify="center")
        StartFrame.labelPrueba.pack(pady=5)
        StartFrame.frameDeTrabajo.update_idletasks()
        threading.Thread(target=Prenda.producirPrendas, args=(StartFrame.aProducirPaEnviar, Main.fecha), daemon=True).start()
        #print("\nsigo después del hilo")
        
        #print(f"\nla tela en la sede p es: {Sede.getListaSedes()[0].getCantidadInsumosBodega()[0]}")
        if Sede.getListaSedes()[0].getCantidadInsumosBodega()[0] < 200 or Sede.getListaSedes()[1].getCantidadInsumosBodega()[0] < 200:
            StartFrame.evento_senalizador.set()

        StartFrame.evento_senalizador.wait()
        StartFrame.evento_senalizador.clear()

        self.verificarEvento()
        contBotonesModistas = tk.Frame(StartFrame.contSeleccionModista, bg="white")
        contBotonesModistas.pack(pady=3)

        for modista in StartFrame.listModistas:
            contInternoBotones = tk.Frame(contBotonesModistas, bg="white")
            contInternoBotones.pack(pady=4)
            boton = tk.Button(contInternoBotones, text=modista.getNombre(), font=("Arial", 9, "italic"))
            boton.pack(side="left", padx=2)
            labelFlecha = tk.Label(contInternoBotones, text="------>", bg="white", font=("Arial", 9, "italic"))
            labelFlecha.pack(side="left", padx=2)
            labelPericia = tk.Label(contInternoBotones, text=f"Pericia: {round(modista.getPericia(), 2)}", bg="white", font=("Arial", 9, "italic"))
            labelPericia.pack(side="left", padx=2)
            boton.bind("<Button-1>", lambda event : self.botonesModistas(event, contBotonesModistas))

    even = threading.Event()
    printModistaGlobal = None
    listModistas = []
    labelPrueba = None
    numero = 0
    contSeleccionModista = None
    def recibePrintModista(self, printModista, modistas):
        StartFrame.listModistas = modistas
        StartFrame.printModistaGlobal = printModista
        StartFrame.indexx = 10
        StartFrame.evento_senalizador.set()
        if StartFrame.numero >= 1:
            self.verificarEvento()
        StartFrame.numero = StartFrame.numero + 1       

    num3 = 0
    def verificarEvento(self):
        from src.uiMain.main import Main
        #colocar a esperar dos segundos si no funciona
        if StartFrame.printModistaGlobal is not None:
            StartFrame.labelPrueba.config(text=StartFrame.printModistaGlobal)
            StartFrame.frameDeTrabajo.update_idletasks()
            #print("\nVOLVI A ENTRARRRRR")
            Main.evento_ui.set()
        else:
            StartFrame.ventanaPrincipal.after(100, self.verificarEvento)
        
        if StartFrame.num3 >= 1:
            self.crearBotones()
        StartFrame.num3 = StartFrame.num3 + 1


    indexx = 10
    num2 = 0
    def botonesModistas(self, event, contPaEliminar):
        from src.uiMain.main import Main
        nombreElegido = event.widget.cget("text")
        if StartFrame.num2 == 0:
            for modista in StartFrame.listModistas:
                if modista.getNombre().lower() == nombreElegido.lower():
                    StartFrame.indexx = StartFrame.listModistas.index(modista)
            #print(f"\nnumero de indice: {StartFrame.indexx}")
            contPaEliminar.destroy()
            Main.evento_ui2.set()
        else:
            for modista in StartFrame.listModistas:
                if modista.getNombre().lower() == nombreElegido.lower():
                    StartFrame.indexx = StartFrame.listModistas.index(modista)
            #print(f"\nnumero de indice: {StartFrame.indexx}")
            contPaEliminar.pack_forget()
            Main.evento_ui2.set()
        StartFrame.num2 = StartFrame.num2 + 1

    def getIndexx(self):
        if StartFrame.indexx != 10:
            return StartFrame.indexx
        
    def crearBotones(self):
        contBotonesModistas = tk.Frame(StartFrame.contSeleccionModista, bg="white")
        contBotonesModistas.pack(pady=3)

        for modista in StartFrame.listModistas:
            contInternoBotones = tk.Frame(contBotonesModistas, bg="white")
            contInternoBotones.pack(pady=4)
            boton = tk.Button(contInternoBotones, text=modista.getNombre(), font=("Arial", 9, "italic"))
            boton.pack(side="left", padx=2)
            labelFlecha = tk.Label(contInternoBotones, text="------>", bg="white", font=("Arial", 9, "italic"))
            labelFlecha.pack(side="left", padx=2)
            labelPericia = tk.Label(contInternoBotones, text=f"Pericia: {round(modista.getPericia(), 2)}", bg="white", font=("Arial", 9, "italic"))
            labelPericia.pack(side="left", padx=2)
            boton.bind("<Button-1>", lambda event : self.botonesModistas(event, contBotonesModistas))
#endregion

def pasarAVentanaPrincipal():
    if Main.deserializacionPendiente:
        from src.uiMain.main import deserializar
        deserializar()
        Main.deserializacionPendiente = False

    ventana = StartFrame()
    ventana.mainloop()