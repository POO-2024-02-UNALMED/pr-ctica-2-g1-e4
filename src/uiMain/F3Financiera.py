import os
import tkinter as tk
from tkinter.font import Font
from tkinter import ttk as ttk

from src.gestorAplicacion.administracion.banco import Banco
from src.gestorAplicacion.administracion.deuda import Deuda
from src.gestorAplicacion.administracion.empleado import Empleado
from src.gestorAplicacion.administracion.evaluacionFinanciera import EvaluacionFinanciera
from src.gestorAplicacion.venta import Venta
from src.uiMain.fieldFrame import FieldFrame

class F3Financiera(tk.Frame):

    def __init__(self,master):
        super().__init__(master)
        self.SistemaFinanciero()

    def SistemaFinanciero(ventana:tk.Frame)->tk.Frame:
                    
        def LeerF2(field_frame2, confirmacion2):
            from src.uiMain.main import Main
            Porcentaje = FieldFrame.getValue(field_frame2, "Descuento")
            
            if Porcentaje != "0% / 100%":
                Porcentaje = Porcentaje.strip("%")
                b = Main.calcularEstimado(float(Porcentaje) / 100)  # Use float to handle percentage
                confirmacion2.config(text="La diferencia entre ventas y deudas futuras, fue de: $"+str(b))

        def Interaccion2():
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
            
            boton1 = tk.Button(frame5, text="Aceptar", command=lambda: LeerF2(field_frame2, confirmacion2))
            boton1.place(relx=0.4, rely=0.5, relwidth=0.1, relheight=0.1, anchor="s")            
            
            boton2 = tk.Button(frame5, text="Siguiente", command=lambda: Interaccion3(frame4, frame5))
            boton2.place(relx=0.6, rely=0.5, relwidth=0.1, relheight=0.1, anchor="s")
            
            confirmacion2 = tk.Label(frame5, text="Calculando estimado entre Ventas y Deudas para ver el estado de endeudamiento de la empresa...", anchor="center")
            confirmacion2.place(relx=0, rely=0.7, relwidth=1, relheight=0.3)

        def LeerF3(field_frame3, confirmacion3):
            from src.uiMain.main import Main
            seleccion = FieldFrame.getValue(field_frame3, "Bancos")
            banco=None
            for banco_actual in Banco.getListaBancos():
                if Banco.getNombre(banco_actual) == seleccion:
                        banco = seleccion
                        break
                c = Main.planRecuperacion(Main.diferenciaEstimado,banco)  # Use float to handle percentage
                confirmacion3.config(text=str(c),font=("Arial", 10))
                return c
            
        def listaBancos(frameb):
            
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
       
        def Interaccion3(frame4,frame5):
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
            listaBancos(labelBanco)
            
            frame7 = tk.Frame(framePrincipal)
            frame7.pack(anchor="s", expand=True, fill="both")
            boton1 = tk.Button(frame7, text="Aceptar", command=lambda: LeerF3(field_frame3, confirmacion3))
            boton1.place(relx=0.4, rely=0.7, relwidth=0.1, relheight=0.2, anchor="s")            
            
            boton2 = tk.Button(frame7, text="Siguiente", command=lambda: Interaccion4(frame6, frameb, frame7,LeerF3(field_frame3, confirmacion3)))
            boton2.place(relx=0.6, rely=0.7, relwidth=0.1, relheight=0.2, anchor="s")
            
            confirmacion3 = tk.Label(frame7, text="", anchor="center")
            confirmacion3.place(relx=0, rely=0.8, relwidth=1, relheight=0.3)
            if Main.diferenciaEstimado > 0:
                confirmacion3.config("El estimado es positivo, las ventas superan las deudas\nHay dinero suficiente para hacer el pago de algunas Deudas")
            else:
                confirmacion3.config("El estimado es negativo, la deuda supera las ventas\nNo hay Dinero suficiente para cubrir los gastos de la empresa, tendremos que pedir un préstamo")
        
        def Interaccion4(frame6,frameb, frame7,c):
            from src.uiMain.main import Main
            frame6.destroy()
            frameb.destroy()
            frame7.destroy()
            
            frame4 = tk.Frame(framePrincipal)
            frame4.pack(anchor="s", expand=True, fill="both")
            descuento = Venta.blackFriday(Main.fecha)
            resultado="si"
            if descuento <= 0.0:
                resultado="no"
                
            criterios = ["Descuento"]
            valores = [str(descuento)]
            habilitado = [True]
            
            # Creamos el FieldFrame con los botones
            field_frame2 = FieldFrame(frame4, ("Según las Ventas anteriores, aplicar descuentos"+resultado+" funcionará"), criterios, "¿Desea Cambiar el siguiente descuento:?", valores, habilitado)
            field_frame2.place(relx=1, rely=0.7, relwidth=1, relheight=1, anchor="e")
            
            frame5 = tk.Frame(framePrincipal)
            frame5.pack(anchor="s", expand=True, fill="both")
            
            boton1 = tk.Button(frame5, text="Aceptar", command=lambda: LeerF2(field_frame2, confirmacion2))
            boton1.place(relx=0.4, rely=0.5, relwidth=0.1, relheight=0.1, anchor="s")            
            
            boton2 = tk.Button(frame5, text="Siguiente", command=lambda: Interaccion3(frame4, frame5))
            boton2.place(relx=0.6, rely=0.5, relwidth=0.1, relheight=0.1, anchor="s")
            
            confirmacion2 = tk.Label(frame5, text="Calculando estimado entre Ventas y Deudas para ver el estado de endeudamiento de la empresa...", anchor="center")
            confirmacion2.place(relx=0, rely=0.7, relwidth=1, relheight=0.3)
        
        def LeerF1():
            from src.uiMain.main import Main
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
                a=Main.calcularBalanceAnterior(empleado,eleccionDeuda)
                confirmacion.config(text=EvaluacionFinanciera.informe(a))
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
            
        framePrincipal =  tk.Frame(ventana, bg="blue")
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
        boton1 = tk.Button(frame3, text="Aceptar", command = lambda: LeerF1())
        boton1.place(relx=0.4, rely=0.6, relwidth=0.1, relheight=0.1, anchor="s")
        boton2 = tk.Button(frame3, text="Siguiente", command = lambda: Interaccion2())
        boton2.place(relx=0.6, rely=0.6, relwidth=0.1, relheight=0.1, anchor="s")
        confirmacion = tk.Label(frame3, text="Calculando la diferencia entre ingresos por venta y costos de producción...",  anchor="center")
        confirmacion.place(relx=0, rely=0.7, relwidth=1, relheight=0.3)
        return framePrincipal
