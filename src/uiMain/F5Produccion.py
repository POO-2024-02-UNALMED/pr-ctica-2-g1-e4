import os
import tkinter as tk
from tkinter.font import Font
from tkinter import ttk
import threading

def producir(ventana:tk.Frame):
    global indicaRepMalo
    global frameDeTrabajo
    framePrincipal =  tk.Frame(ventana, bg="blue")
    framePrincipal.pack(fill="both", expand=True, padx=7, pady=7)

    frame1 = tk.Frame(framePrincipal, height=150)
    frame1.pack(side="top", fill="x")

    tituloF5 = tk.Label(frame1, text="Producción", bg="medium orchid", relief="ridge", font=("Arial",16, "bold"))
    tituloF5.place(relx=0.5, rely=0.6, relwidth=1, relheight=0.6, anchor="s") 
    ## relwidth y relheight reciben el porcentaje de tamaño respecto al contenedor

    descripcionF5 = tk.Label(frame1, text="Se registra la producción de prendas y actualiza su inventario: Se toma la cantidad necesaria del stock de materiales para fabricar nuevas prendas y se actualizan los datos, tanto de lo que se descontó de Stock como lo que se agregó a la cantidad de pendas.", relief="ridge")
    descripcionF5.place(relx=1, rely=0.8, relwidth=1, relheight=0.4, anchor="e")

    frame2 = tk.Frame(framePrincipal, bg="light gray")
    frame2.pack(anchor="s",  expand=True, fill="both")
    frameDeTrabajo = frame2

    descripcion1 = tk.Label(frame2, text="Presiona 'CONTINUAR' para evaluar el estado de la maquinaria disponible en cada sede", wraplength=200, justify="center")
    descripcion1.place(relx=0.3, rely=0.08)

    botonContinuar = tk.Button(frame2, text="CONTINUAR", command=lambda : activar(frame2, descripcion1, botonContinuar))
    botonContinuar.place(relx=0.6, rely=0.12)

    indicaRepMalo = tk.Label(frame2, text="", bg="light gray")
    indicaRepMalo.place(relx=0.5, rely=0.35, anchor="center")
    
def activar(ventana:tk.Frame, descrip1:tk.Label, botonContinuar:tk.Button):
    from src.gestorAplicacion.bodega.maquinaria import Maquinaria
    buscarProveedor(ventana, descrip1, botonContinuar)
    #Maquinaria.agruparMaquinasDisponibles(10)

    threading.Thread(target=Maquinaria.agruparMaquinasDisponibles, args=(10,), daemon=True).start()
    
senal= 0
def receptor(texto):
    global senal
    senal = senal + 1
    if senal == 1:
        if indicaRepMalo:
            indicaRepMalo.config(text=texto, font=("Arial", 16, "bold"))
    else:
        if indicaRepMalo:
            indicaRepMalo.config(text=texto, font=("Arial", 16, "bold"))
            indicaRepMalo.place(relx=0.5, rely=0.2, anchor="center")        

indicaRepMalo = None
frameDeTrabajo = None
proveedorB = None
botonProveedorB = None

senal2 = 0
def buscarProveedor(ventana:tk.Frame, descrip1: tk.Label, botonContinuar:tk.Button):
    global botonProveedorB
    global proveedorB
    global senal2
    senal2 = senal2 + 1
    print("desdebp")
    if senal2 == 1:
        botonProveedorB = tk.Button(ventana, text="Consultar", wraplength=250, justify="center", font=("Arial", 12, "bold"), command=lambda : (limpieza(ventana, descrip1, botonContinuar, botonProveedorB), mostrarProveedorB()))
        botonProveedorB.place(relx=0.5, rely=0.5, anchor="center")
    else:
        botonProveedorB = tk.Button(ventana, text="Consultar", wraplength=250, justify="center", font=("Arial", 12, "bold"), command=lambda : (limpieza(ventana, descrip1, botonContinuar, botonProveedorB), mostrarProveedorB()))
        botonProveedorB.place(relx=0.5, rely=0.5, anchor="center")
        ventana.bind("<space>", lambda event: eliminarBoton(event, botonProveedorB))

        
def eliminarBoton(event, boton):
    boton.destroy()

senal3 = 0
def limpieza(ventana:tk.Frame, descrip1:tk.Label, botonContinuar:tk.Button, botonProveedorB=tk.Button):
    global indicaRepMalo
    global senal3
    senal3 = senal3 + 1
    if senal3 == 1:
        descrip1.destroy()
        botonContinuar.destroy()
        botonProveedorB.place_forget()

        indicaRepMalo.place(relx=0.5, rely=0.2, anchor="center")
    else: 
        botonProveedorB.place_forget()


def recibeProveedorB(proveedorBa):
    global proveedorB
    proveedorB = proveedorBa

def mostrarProveedorB():
    global frameDeTrabajo
    global proveedorB

    if proveedorB is None:
        indicaRepMalo.destroy()
        return
    
    nombreP = tk.Label(frameDeTrabajo, text=proveedorB.getNombre(), font=("Arial", 12, "italic"))
    nombreP.place(relx=0.6, rely=0.37)

    nombre = tk.Label(frameDeTrabajo, text="PROVEEDOR BARATO:", bg="light gray", font=("Arial", 12, "bold italic"))
    nombre.place(relx=0.3, rely=0.37)

    precio = tk.Label(frameDeTrabajo, text="PRECIO:", bg="light gray", font=("Arial", 12, "bold italic"))
    precio.place(relx=0.35, rely=0.45)
    precioP = tk.Label(frameDeTrabajo, text=str(proveedorB.getPrecio()), font=("Arial", 12, "italic"))
    precioP.place(relx=0.6, rely=0.45)
    comprar = tk.Button(frameDeTrabajo, text="COMPRAR REPUESTO", font=("Arial", 13, "bold"))
    comprar.place(relx=0.38, rely=0.61)
    comprar.bind("<Button-1>", lambda event: evento(event, nombre, nombreP, precio, precioP))

def evento(event, nombre, nombreP, precio, precioP):
    from src.gestorAplicacion.sede import Sede
    event.widget.destroy()

    separador = ttk.Separator(frameDeTrabajo, orient="horizontal")
    separador.place(relx=0.05, rely=0.55, relwidth=0.9)
    seleccionar = tk.Label(frameDeTrabajo, text="Seleccione la sede desde donde comprará el Repuesto:", bg="light gray", font=("Arial", 12, "bold"))
    seleccionar.place(relx=0.5, rely=0.63, anchor="center")
    contSedes = tk.Frame(frameDeTrabajo, bg="light gray", bd=4, relief="ridge")
    contSedes.place(relx=0.5, rely=0.85, anchor="center") #sede Principal
    contSedeP = tk.Frame(contSedes, bg="light gray", width=100, height=100)
    contSedeP.pack(fill="x", padx=5, pady=5)
    sedePdinero = tk.Label(contSedeP, text=str(Sede.getListaSedes()[0].getCuentaSede().getAhorroBanco()), font=("Arial", 12, "italic"))
    sedePdinero.pack(side="right", padx=10, pady=5)
    sedePflecha = tk.Label(contSedeP, text="------------>", bg="light gray", font=("Arial", 12, "bold"))
    sedePflecha.pack(side="right", pady=5)    
    #sede2
    contSedes2 = tk.Frame(contSedes, bg="light gray", width=100, height=100)
    contSedes2.pack(fill="x", padx=35, pady=0)
    sede2dinero = tk.Label(contSedes2, text=str(Sede.getListaSedes()[1].getCuentaSede().getAhorroBanco()), font=("Arial", 12, "italic"))
    sede2dinero.pack(side="right", padx=10, pady=5)
    sede2flecha = tk.Label(contSedes2, text="------------>", bg="light gray", font=("Arial", 12, "bold"))
    sede2flecha.pack(side="right", pady=5)
    sedePboton = tk.Button(contSedeP, text="Sede Principal", font=("Arial", 12, "italic"))
    sedePboton.pack(side="right", padx=10, pady=5)
    sedePboton.bind("<Button-1>", lambda event: eventoDeCompra(event, nombre, nombreP, precio, precioP, separador, seleccionar, contSedes, contSedeP, sedePdinero, sedePflecha, contSedes2, sede2dinero, sede2flecha, sede2boton))
    sede2boton = tk.Button(contSedes2, text="Sede 2", font=("Arial", 12, "italic"))
    sede2boton.pack(side="right", padx=10, pady=5)
    sede2boton.bind("<Button-1>", lambda event: eventoDeCompra(event, nombre, nombreP, precio, precioP, separador, seleccionar, contSedes, contSedeP, sedePdinero, sedePflecha, contSedes2, sede2dinero, sede2flecha, sedePboton))

def eventoDeCompra(event, nombre, nombreP, precio, precioP, separador, seleccionar, contSedes, contSedeP, sedePdinero, sedePflecha, contSedes2, sede2dinero, sede2flecha, botonDeSede):
    from src.gestorAplicacion.sede import Sede
    global indicaRepMalo
    global proveedorB
    textoDeBoton = botonDeSede.cget("text")
    indicaRepMalo.place_forget()
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
        labelDeCompraP = tk.Label(frameDeTrabajo, text=f"El repuesto {proveedorB.getInsumo().getNombre()} se compró exitosamente desde la Sede Principal", wraplength=500, font=("Arial", 14, "bold"))
        labelDeCompraP.place(relx=0.5, rely=0.2, anchor="center")
        Sede.getListaSedes()[0].getCuentaSede().setAhorroBanco( (Sede.getListaSedes()[0].getCuentaSede().getAhorroBanco() - proveedorB.getPrecio()) )
        labelSaldo = tk.Label(frameDeTrabajo, text= f"Saldo Disponible: {Sede.getListaSedes()[0].getCuentaSede().getAhorroBanco()} pesos", font=("Arial", 14, "italic"))
        labelSaldo.place(relx=0.5, rely=0.4, anchor="center")

        seguirAnalisis = tk.Button(frameDeTrabajo, text="Continuar Análisis", font=("Arial", 12, "bold"))
        seguirAnalisis.place(relx=0.5, rely=0.6, anchor="center")
        seguirAnalisis.bind("<Button-1>", lambda event: eventoContinuador(event, labelDeCompraP, labelSaldo))

    else:
        labelDeCompraP = tk.Label(frameDeTrabajo, text=f"El repuesto {proveedorB.getInsumo().getNombre()} se compró exitosamente desde la Sede 2", wraplength=500, font=("Arial", 14, "bold"))
        labelDeCompraP.place(relx=0.5, rely=0.2, anchor="center")
        Sede.getListaSedes()[1].getCuentaSede().setAhorroBanco( (Sede.getListaSedes()[1].getCuentaSede().getAhorroBanco() - proveedorB.getPrecio()) )
        labelSaldo = tk.Label(frameDeTrabajo, text= f"Saldo Disponible: {Sede.getListaSedes()[1].getCuentaSede().getAhorroBanco()} pesos", font=("Arial", 14, "italic"))
        labelSaldo.place(relx=0.5, rely=0.4, anchor="center")

        seguirAnalisis = tk.Button(frameDeTrabajo, text="Continuar Análisis", font=("Arial", 12, "bold"))
        seguirAnalisis.place(relx=0.5, rely=0.6, anchor="center")
        seguirAnalisis.bind("<Button-1>", lambda event: eventoContinuador(event, labelDeCompraP, labelSaldo))
        
    
def eventoContinuador(event, labelDeCompra, labelSaldo):
    from src.uiMain.main import Main
    global proveedorB
    global botonProveedorB

    labelDeCompra.destroy()
    labelSaldo.destroy()
    event.widget.destroy()
    Main.evento_ui.set()
    print(proveedorB)
    buscarProveedor(frameDeTrabajo, 1, 1)
    
        
    
    
    

    
    
