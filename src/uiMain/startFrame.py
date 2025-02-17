# Dibuja la ventana y la parte externa, y la parte interna la saca de las clases F.
# O en el caso respectivo, no dibuja una funcionalidad, sino frameInicial.
import os
import tkinter as tk
from tkinter.font import Font
import sys
from src.gestorAplicacion.administracion.empleado import Empleado
from src.uiMain.F2Insumos import F2Insumos
from src.uiMain.F4Facturaccion import Facturar
from src.uiMain.exceptionC1 import ExceptionC1
from src.uiMain.main import Main
from src.uiMain.F3Financiera import F3Financiera
from src.uiMain.F5Produccion import producir
from src.uiMain.fieldFrame import FieldFrame
from src.gestorAplicacion.fecha import Fecha
from src.gestorAplicacion.sede import Sede

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
# Inicializar pygame para el audio
#pygame.mixer.init() # Función para reproducir el audio #def reproducir_audio(): #ruta_audio = os.path.join("src", "uiMain", "imagenes", "EcomodaALaOrden.mp3") #pygame.mixer.music.load(ruta_audio)  # Cambia la ruta del archivo de audio #pygame.mixer.music.play()

class startFrame(tk.Tk):
    def __init__(self):
        self.pagina="ninguna"
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
        self.procesosMenu.add_command(label="Pedir insumos", command = lambda : self.eliminarF2())
        self.procesosMenu.add_command(label="Ver el desglose economico de la empresa", command = lambda : self.eliminarF3())
        self.procesosMenu.add_command(label="Facturacion", command = lambda : self.eliminarF4())
        self.procesosMenu.add_command(label="Producir prendas", command= lambda : self.iniciarProduccion())

        self.ayudaMenu = tk.Menu(self.barraMenus, tearoff=0)
        self.barraMenus.add_cascade(label="Ayuda", menu=self.ayudaMenu)
        self.ayudaMenu.add_command(label="Acerca de", command= lambda : self.acercaDe())

        self.abrirFrameInicial()

    #-----------------Listeners para el menú superior-----------------
    def abrirGestionHumana(self):
        self.areaPrincipal.destroy()
        self.pagina="gestionHumana"
        self.cambiarFrame(self.crearGestionHumana())
    
    def eliminarF2(self):
        self.areaPrincipal.destroy()
        self.cambiarFrame(F2Insumos(self))
        
    def eliminarF4(self):
        self.areaPrincipal.destroy()
        self.cambiarFrame(Facturar(self))
        
    def eliminarF3(self):
        self.areaPrincipal.destroy()
        self.cambiarFrame(F3Financiera(self))

    def iniciarProduccion(self):
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
#-----------------Frame Inicial-----------------

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

        self.enviarFecha=tk.Button(self.contenedorFecha,text="Enviar")
        self.enviarFecha.place(relx=0.820, rely=0.8, relwidth=0.1, relheight=0.1, anchor="n")
        self.enviarFecha.bind("<Button-1>", self.Ok)
        
        self.frameInicial.rowconfigure(0, weight=1)
        self.frameInicial.rowconfigure(1, weight=3)
        self.frameInicial.rowconfigure(2, weight=3)



        # Función que se ejecutará al presionar el botón
    def Ok(self,event):
        # Leer los valores de las entradas
        FDia = self.entradaDia.get() # Obtener el texto de la entrada para el día
        FMes = self.entradaMes.get() # Obtener el texto de la entrada para el mes
        FAño = self.entradaAño.get() # Obtener el texto de la entrada para el año
        if not FDia or not FMes or not FAño:
                error = ExceptionC1("Debes ingresar una fecha antes de continuar.")
                error.contenidoVacio()
                self.borrar()
                self.after(100, self.Ok)
                return 
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
        if dia <= 0 or dia > 31:
            self.borrar()
            error = ExceptionC1("El día ingresado no es válido.")
            error.fechaNoValidada()
            self.after(100, self.Ok) 
        elif mes <= 0 or mes > 12:
            self.borrar()
            error = ExceptionC1("El mes ingresado no es válido.")
            error.fechaNoValidada()
            self.after(100, self.Ok) 
        elif año <= 0:
            self.borrar()
            error = ExceptionC1("El año ingresado no es válido.")
            error.fechaNoValidada()
            self.after(100, self.Ok) 
        else:
            fecha = Fecha(dia, mes, año)
            Main.fecha=fecha
            self.fechaValida = True
        return fecha
    
#-----------------Gestión Humana-----------------
    def crearGestionHumana(self):
        self.gestionHumana=tk.Frame(self)
        self.posiblesDespedidos=[]
        self.sede=None
        self.inicialGestionHumana()
        self.empleadosADespedir=[] # Se llena al dar aceptar en la pantalla de seleccion.
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
        
        empleadosMalosString += """Estos empleados tienen un rendimiento menor al esperado, y no puedieron ser transferidos ni cambiados de cargo.\n"""

        empleadosMalosString += """Puede elegir despedir a estos empleados si lo desea, insertando SI en el campo de texto, o puede añadir mas empleados a la lista de despedibles"""

        self.labelPreConsulta=tk.Label(self.frame1, text=empleadosMalosString, relief="ridge", font=("Arial", 10))
        self.labelPreConsulta.grid(row=1, column=0, sticky="nswe",columnspan=4)

        nombres=[]
        for empleado in self.posiblesDespedidos:
            nombres.append(Empleado.getNombre(empleado))

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
        self.empleadosADespedir=[]
        for empleado in self.posiblesDespedidos:
            if self.seleccionador.getValue(Empleado.getNombre(empleado)).lower()=="si":
                self.empleadosADespedir.append(empleado)
        Main.despedirEmpleados(self.empleadosADespedir)
        self.reemplazarPorCambioSede()

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
        self.descripcionCambioSede = tk.Label(self.frame1, text=f"""Se han despedido {len(self.empleadosADespedir)} empleados""", relief="ridge", font=("Arial", 10))
        self.descripcionCambioSede.grid(row=0, column=0, sticky="nswe", columnspan=4)
        nececidades=Sede.obtenerNecesidadTransferenciaEmpleados(self.empleadosADespedir)
        rolesATransferir=nececidades[0]
        transferirDe=nececidades[1]
        aContratar=nececidades[2]



def pasarAVentanaPrincipal():
    ventana = startFrame()
    ventana.mainloop()