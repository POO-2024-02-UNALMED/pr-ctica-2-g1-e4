import os
import tkinter as tk
from tkinter.font import Font
from tkinter import ttk as ttk

from src.uiMain.fieldFrame import FieldFrame


def deudas(ventana:tk.Frame)->tk.Frame:
    
    def Siguiente():
        eleccionDeuda=0
        resultadosP=FieldFrame.getValue(field_frame,"Proveedor")
        resultadosB=FieldFrame.getValue(field_frame,"Banco")
        if resultadosP[0].lowercase()!="si/no" and resultadosB[1].lowercase()!="si/no" and entradaCombo.get()!="":
            from src.uiMain.main import Main
            Empleado=entradaCombo.get()
            if resultadosP[0].lowercase() == "si" and resultadosB[1].lowercase()=="no":
                elecionDeuda = 1
            elif resultadosP[0].lowercase() == "no" and resultadosB[1].lowercase()=="si":
                elecionDeuda = 2
            elif resultadosP[0].lowercase() == "si" and resultadosB[1].lowercase()=="si":
                elecionDeuda = 3
        from src.gestorAplicacion.sede import Sede
        for empleado_actual in Sede.getListaEmpleadosTotal():
            if empleado_actual.getNombre() == Empleado.getNombre():
                empleado = empleado_actual
            Main.calcularBalanceAnterior(empleado,eleccionDeuda)
        else:
            #Excepcion
            resultadosP[0].delete(0,"end")
            resultadosB[1].delete(0,"end")
            entradaCombo.delete(0,"end")
            
    
    def changed(event):
        entradaCombo.delete(0,"end")
        entradaCombo.insert(0,combo.get())
        

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
    field_frame = FieldFrame(frame2, "Desea calcular las siguientes deudas", criterios, "", valores, habilitado)
    field_frame.place(relx=1, rely=0.5, relwidth=1, relheight=1, anchor="e")
    
    frame3 = tk.Frame(framePrincipal)
    frame3.pack(anchor="s",  expand=True, fill="both")
    label7 = tk.Label(frame3, text="Directivos disponibles:",anchor="w", font=("Arial",12, "bold"))
    label7.place(relx=0.5, rely=0.6, relwidth=1, relheight=1, anchor="s")
    label7.config(padx=200)
    Lista=Directivos()
    combo = ttk.Combobox(master=label7,values=Lista)
    combo.bind("<<ComboboxSelected>>",changed)
    combo.place(relx=0.5, rely=0.8, relwidth=0.5, relheight=0.2, anchor="s")
    entradaCombo = tk.Entry(label7)
    entradaCombo.config(state="disabled")
    entradaCombo.grid(row=0,column=1,padx=10,pady=10,sticky="w")
    boton1 = tk.Button(frame3, text="Aceptar", command = lambda: Siguiente)
    boton1.place(relx=0.5, rely=0.8, relwidth=0.2, relheight=0.2, anchor="s")
    
    return framePrincipal

    

