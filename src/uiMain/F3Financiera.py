import os
import tkinter as tk
from tkinter.font import Font
from tkinter import ttk as ttk

from src.gestorAplicacion.administracion.empleado import Empleado
from src.gestorAplicacion.administracion.evaluacionFinanciera import EvaluacionFinanciera
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
                confirmacion2.config(text=str(b))

        def Interaccion2():
            frame2.destroy()
            frame3.destroy()
            
            frame4 = tk.Frame(framePrincipal, bg="light gray")
            frame4.pack(anchor="s", expand=True, fill="both")
            
            criterios = ["Descuento"]
            valores = ["0% / 100%"]
            habilitado = [True]
            
            # Creamos el FieldFrame con los botones
            field_frame2 = FieldFrame(frame4, "Ingrese porcentaje a modificar para fidelidad de los clientes sin membresía", criterios, "", valores, habilitado)
            field_frame2.place(relx=1, rely=0.5, relwidth=1, relheight=1, anchor="e")
            
            frame5 = tk.Frame(framePrincipal)
            frame5.pack(anchor="s", expand=True, fill="both")
            
            boton1 = tk.Button(frame5, text="Aceptar", command=lambda: LeerF2(field_frame2, confirmacion2))
            boton1.place(relx=0.4, rely=0.7, relwidth=0.1, relheight=0.1, anchor="s")            
            
            boton2 = tk.Button(frame5, text="Siguiente", command=lambda: Interaccion3(frame4, frame5))
            boton2.place(relx=0.6, rely=0.7, relwidth=0.1, relheight=0.1, anchor="s")
            
            confirmacion2 = tk.Label(frame5, text="", anchor="w")
            confirmacion2.place(relx=0.5, rely=0.7, relwidth=1, relheight=0.3, anchor="n")
                
        def Interaccion3(frame4,frame5):
            frame4.destroy()
            frame5.destroy()
            frame6 = tk.Frame(framePrincipal, bg="light gray")
            frame6.pack(anchor="s",  expand=True, fill="both")
            criterios = ["Descuento"]
            valores = ["0% / 100%"]
            habilitado = [True]
            # Creamos el FieldFrame con los botones
            field_frame2 = FieldFrame(frame6, "Ingrese porcentaje a modificar para fidelidad de los clientes sin membresía", criterios, "", valores, habilitado)
            field_frame2.place(relx=1, rely=0.5, relwidth=1, relheight=1, anchor="e")
        
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
        frame2 = tk.Frame(framePrincipal, bg="light gray")
        frame2.pack(anchor="s",  expand=True, fill="both")
        criterios = ["Proveedor", "Banco"]
        valores = ["Si/No", "Si/No"]
        habilitado = [True, True]
        # Creamos el FieldFrame con los botones
        field_frame = FieldFrame(frame2, "Desea calcular las siguientes SistemaFinanciero", criterios, "", valores, habilitado)
        field_frame.place(relx=1, rely=0.5, relwidth=1, relheight=1, anchor="e")
        frame3 = tk.Frame(framePrincipal)
        frame3.pack(anchor="s",  expand=True, fill="both")
        label7 = tk.Label(frame3, text="Directivos disponibles:",anchor="w", font=("Arial",12, "bold"))
        label7.place(relx=0.5, rely=0.6, relwidth=1, relheight=1, anchor="s")
        label7.config(padx=200)
        Lista=Directivos()
        placeholder = tk.StringVar(master=label7, value="Elije al directivo")
        combo = ttk.Combobox(master=label7,values=Lista, textvariable=placeholder,state="readonly")
        combo.place(relx=0.5, rely=0.8, relwidth=0.5, relheight=0.2, anchor="s")
        boton1 = tk.Button(frame3, text="Aceptar", command = lambda: LeerF1())
        boton1.place(relx=0.4, rely=0.7, relwidth=0.1, relheight=0.1, anchor="s")
        boton2 = tk.Button(frame3, text="Siguiente", command = lambda: Interaccion2())
        boton2.place(relx=0.6, rely=0.7, relwidth=0.1, relheight=0.1, anchor="s")
        confirmacion = tk.Label(frame3, text="",  anchor="w")
        confirmacion.place(relx=0.5, rely=0.7, relwidth=1, relheight=0.3, anchor="n")
        return framePrincipal
