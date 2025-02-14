import os
import tkinter as tk
from tkinter.font import Font
from tkinter import ttk as ttk


def deudas(ventana:tk.Frame):
    
    def Siguiente(event):
        eleccionDeuda=0
        if OProveedor.cget()!="" and OBanco.cget()!="" and entradaCombo.get()!="":
            from src.uiMain.main import Main
            Empleado=entradaCombo.get()
            if OProveedor.cget().lowercase() == "si" and OBanco.cget().lowercase()=="no":
                elecionDeuda = 1
            elif OProveedor.cget().lowercase() == "no" and OProveedor.cget().lowercase()=="si":
                elecionDeuda = 2
            elif OProveedor.cget().lowercase() == "si" and OBanco.cget().lowercase()=="si":
                elecionDeuda = 3
            Main.calcularBalanceAnterior(Empleado,eleccionDeuda)
        else:
            #Excepcion
            OProveedor.delete(0,"end")
            OBanco.delete(0,"end")
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
        print (elegible_empleados)
        return elegible_empleados
        

    framePrincipal =  tk.Frame(ventana, bg="blue")
    framePrincipal.pack(fill="both", expand=True, padx=7, pady=7)

    frame1 = tk.Frame(framePrincipal, height=150)
    frame1.pack(side="top", fill="x")

    tituloF3 = tk.Label(frame1, text="Gestión Financiera", bg="medium orchid", relief="ridge", font=("Arial",16, "bold"))
    tituloF3.place(relx=0.5, rely=0.6, relwidth=1, relheight=0.6, anchor="s") 
    ## relwidth y relheight reciben el porcentaje de tamaño respecto al contenedor

    descripcionF3 = tk.Label(frame1, text="Se realiza una evaluación del estado financiero de la empresa haciendo el cálculo de los activos y los pasivos, para indicarle al usuario qué tan bien administrada está, mostrandole los resulatdos y su significado", relief="ridge")
    descripcionF3.place(relx=1, rely=0.8, relwidth=1, relheight=0.4, anchor="e")

    frame2 = tk.Frame(framePrincipal, bg="light gray")
    frame2.pack(anchor="s",  expand=True, fill="both")


    label4 = tk.Label(frame2, text="Desea calcular deudas con:", relief="ridge", anchor="w")
    label4.place(relx=0.5, rely=0.2, relwidth=1, relheight=0.2, anchor="s")
    label4.config(padx=200)
    label5 = tk.Label(frame2, text="Proveedor", relief="ridge", anchor="w")
    label5.place(relx=0.5, rely=0.4, relwidth=1, relheight=0.2, anchor="s")
    label5.config(padx=200)
    OProveedor=tk.Entry(label5,textvariable="Si/No")
    OProveedor.grid(row=0,column=1,padx=10,pady=10,sticky="n")
    label6 = tk.Label(frame2, text="Banco", relief="ridge", anchor="w")
    label6.place(relx=0.5, rely=0.6, relwidth=1, relheight=0.2, anchor="s")
    label6.config(padx=200)
    OBanco=tk.Entry(label6,textvariable="Si/No")
    OBanco.grid(row=0,column=1,padx=10,pady=10,sticky="n")
    label7 = tk.Label(frame2, text="Directivo:", relief="ridge", anchor="w")
    label7.place(relx=0.5, rely=0.8, relwidth=1, relheight=0.2, anchor="s")
    label7.config(padx=200)
    Lista=Directivos()
    combo = ttk.Combobox(master=label7,values=Lista)
    combo.bind("<<ComboboxSelected>>",changed)
    combo.grid(row=0,column=0,padx=10,pady=10,sticky="w")
    entradaCombo = tk.Entry(label7)
    entradaCombo.grid(row=0,column=1,padx=10,pady=10,sticky="w")
    boton1 = tk.Button(frame2, text="Aceptar", command=Siguiente)
    

