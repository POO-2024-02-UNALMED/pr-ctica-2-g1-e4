import os
import tkinter as tk
from tkinter.font import Font
from tkinter import ttk
import threading

def producir(ventana:tk.Frame):
    global indicaRepMalo, frameDeTrabajo, descripcionF5
    framePrincipal =  tk.Frame(ventana, bg="blue")
    framePrincipal.pack(fill="both", expand=True, padx=7, pady=7)

    frame1 = tk.Frame(framePrincipal)
    frame1.pack(side="top", fill="x")

    tituloF5 = tk.Label(frame1, text="Producción", bg="medium orchid", relief="ridge", height=2, font=("Arial",16, "bold"))
    tituloF5.pack(fill="both", expand=True) 
    ## relwidth y relheight reciben el porcentaje de tamaño respecto al contenedor

    descripcionF5 = tk.Label(frame1, text="Se registra la producción de prendas y actualiza su inventario: Se toma la cantidad necesaria del stock de materiales para fabricar nuevas prendas y se actualizan los datos, tanto de lo que se descontó de Stock como lo que se agregó a la cantidad de pendas.", height=3,wraplength=800, font=("Arial", 10, "italic"))
    descripcionF5.pack(fill="both", expand=True)

    frame2 = tk.Frame(framePrincipal, bg="light gray")
    frame2.pack(anchor="s",  expand=True, fill="both")
    frameDeTrabajo = frame2

    descripcion1 = tk.Label(frame2, text="Presiona 'CONTINUAR' para evaluar el estado de la maquinaria disponible en cada sede", wraplength=200, justify="center")
    descripcion1.place(relx=0.3, rely=0.08)

    botonContinuar = tk.Button(frame2, text="CONTINUAR", command=lambda : activar(frame2, descripcion1, botonContinuar))
    botonContinuar.place(relx=0.6, rely=0.12)

    indicaRepMalo = tk.Label(frame2, text="", bg="light gray")
    indicaRepMalo.place(relx=0.5, rely=0.35, anchor="center")

    return framePrincipal
    
def activar(ventana:tk.Frame, descrip1:tk.Label, botonContinuar:tk.Button):  #creo que al poner varias variables en global no sirve para modificarlas globalmente, verificar
    from src.gestorAplicacion.bodega.maquinaria import Maquinaria
    from src.uiMain.main import Main
    global proveedoresQueLlegan, preciosProvQueLlegan, totalGastado
    global nomListMaqRev, sedesListMaqRev
    global maqDisponibless
    global nomMaqProdDispSedeP, sedeMaqProdDispSedeP, horasUsoMaqProdDispSedeP
    global nomMaqProdDispSede2, sedeMaqProdDispSede2, horasUsoMaqProdDispSede2
    global textIndicador, senalizador
    global aProdFinal, aProducirPaEnviar
    proveedoresQueLlegan = []
    preciosProvQueLlegan = []
    totalGastado = 0
    nomListMaqRev = []
    sedesListMaqRev = []
    
    maqDisponibless = []
    nomMaqProdDispSedeP = []
    sedeMaqProdDispSedeP = []
    horasUsoMaqProdDispSedeP = []
    nomMaqProdDispSede2 = []
    sedeMaqProdDispSede2 = []
    horasUsoMaqProdDispSede2 = []
    textIndicador = None
    senalizador = 0
    aProdFinal = [] ; aProducirPaEnviar = []
    buscarProveedor(ventana, descrip1, botonContinuar)
    #Maquinaria.agruparMaquinasDisponibles(10)

    threading.Thread(target=Maquinaria.agruparMaquinasDisponibles, args=(Main.fecha,), daemon=True).start()
    
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
descripcionF5 = None

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


proveedoresQueLlegan = []
preciosProvQueLlegan = []
totalGastado = 0
def recibeProveedorB(proveedorBa):
    from src.gestorAplicacion.bodega.proveedor import Proveedor
    global proveedorB
    global proveedoresQueLlegan
    global preciosProvQueLlegan
    global totalGastado
    proveedorB = proveedorBa

    if proveedorBa is not None:
        proveedoresQueLlegan.append(proveedorBa.getInsumo().getNombre())
        preciosProvQueLlegan.append(proveedorBa.getPrecio())
        totalGastado += proveedorBa.getPrecio()
    #elif proveedorBa is None:
    #    proveedoresQueLlegan = []
    #    preciosProvQueLlegan = []
    #    totalGastado = 0



def mostrarProveedorB():
    global frameDeTrabajo
    global proveedorB

    if proveedorB is None:
        indicaRepMalo.destroy()
        resultadosRev()
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

nomListMaqRev = []
sedesListMaqRev = []
def recibeMaqPaRevisar(listMaquinasRev):
    from src.gestorAplicacion.bodega.maquinaria import Maquinaria
    global nomListMaqRev
    global sedesListMaqRev

    for maq in listMaquinasRev:
        nomListMaqRev.append(maq.getNombre())
        sedesListMaqRev.append(maq.getSede().getNombre())
    

def resultadosRev():
    from src.uiMain.fieldFrame import FieldFrame
    global proveedoresQueLlegan
    global preciosProvQueLlegan
    global totalGastado
    global nomListMaqRev
    global sedesListMaqRev
    
    criterios = proveedoresQueLlegan
    valores = preciosProvQueLlegan
    habilitado = [False for _ in range(len(proveedoresQueLlegan))]

    containerBig = tk.Frame(frameDeTrabajo, bg="light gray")
    containerBig.pack(pady=10)

    cont = tk.Frame(containerBig, bg="medium orchid")
    cont.pack(side="left", pady=20)
    
    field_frame = FieldFrame(cont, "Los repuestos comprados fueron:", criterios, "", valores, habilitado)
    field_frame.pack(padx=10, pady=10)

    labelTotalGastado = tk.Label(cont, text=f"Total gastado: {totalGastado} pesos", font=("Arial", 12, "italic"))
    labelTotalGastado.pack(pady=10)

    criterios2 = nomListMaqRev
    valores2 = sedesListMaqRev
    habilitado2 = [False for _ in range(len(nomListMaqRev))]

    cont2 = tk.Frame(containerBig, bg="medium orchid")
    cont2.pack(side="left", pady=20, padx=5)
    
    field_frame2 = FieldFrame(cont2, "Maquinas inhabilidas\npor falta de revisión:", criterios2, "", valores2, habilitado2)
    field_frame2.pack(padx=10, pady=10)

    #labelTotalGastado = tk.Label(cont, text=f"Total gastado: {totalGastado} pesos", font=("Arial", 12, "italic"))
    #labelTotalGastado.pack(pady=10)

    botonInt2 = tk.Button(frameDeTrabajo, text="Maquinaria Disponible", font=("Arial", 12, "bold italic"))
    botonInt2.pack(pady=4)
    botonInt2.bind("<Button-1>", lambda event: inicioInt2(event, containerBig, cont, field_frame, labelTotalGastado, cont2, field_frame2))

maqDisponibless = []

def recibeMaqDisp(maqDisponibles):
    global maqDisponibless
    maqDisponibless = maqDisponibles
    

nomMaqProdDispSedeP = []
sedeMaqProdDispSedeP = []
horasUsoMaqProdDispSedeP = []
nomMaqProdDispSede2 = []
sedeMaqProdDispSede2 = []
horasUsoMaqProdDispSede2 = []
def recibeMaqDispSeparadas(maqProdSedeP, maqProdSede2):
    global nomMaqProdDispSedeP, sedeMaqProdDispSedeP, horasUsoMaqProdDispSedeP
    global nomMaqProdDispSede2, sedeMaqProdDispSede2, horasUsoMaqProdDispSede2
    for maquinasSedeP in maqProdSedeP:
        nomMaqProdDispSedeP.append(maquinasSedeP.getNombre())
        sedeMaqProdDispSedeP.append(maquinasSedeP.getSede().getNombre())
        horasUsoMaqProdDispSedeP.append(maquinasSedeP.getHorasUso())
    for maquinasSede2 in maqProdSede2:
        nomMaqProdDispSede2.append(maquinasSede2.getNombre())
        sedeMaqProdDispSede2.append(maquinasSede2.getSede().getNombre())
        horasUsoMaqProdDispSede2.append(maquinasSede2.getHorasUso())

textIndicador = None
senalizador = 0
evento_senalizador = threading.Event()
def recibeTextIndicador(textRecibido, senal):
    global textIndicador, senalizador, evento_senalizador
    textIndicador = textRecibido
    senalizador = senal
    evento_senalizador.set()

def inicioInt2(event, containerBig, cont, field_frame, labelTG, cont2, field_frame2):
    global maqDisponibless
    global nomMaqProdDispSedeP, sedeMaqProdDispSedeP, horasUsoMaqProdDispSedeP
    global nomMaqProdDispSede2, sedeMaqProdDispSede2, horasUsoMaqProdDispSede2
    global textIndicador, senalizador, evento_senalizador
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
    frameDeTrabajo.config(bg="white")
    threading.Thread(target=Sede.planProduccion, args=(maqDisponibless, Main.fecha), daemon=True).start()

    criterios = nomMaqProdDispSedeP
    valores = horasUsoMaqProdDispSedeP
    habilitado = [False for _ in range(len(nomMaqProdDispSedeP))]

    containerBig = tk.Frame(frameDeTrabajo, bg="white")
    containerBig.pack(pady=2)

    evento_senalizador.wait()
    evento_senalizador.clear()
    #print(f"\nsenalizador = {senalizador}")
    if senalizador == 2 or senalizador == 4:
        cont = tk.Frame(containerBig, bg="gray")
        cont.pack(side="left", padx=5, pady=10)
    else:
        cont = tk.Frame(containerBig, bg="medium orchid")
        cont.pack(side="left", padx=5, pady=10)
    
    field_frame = FieldFrame(cont, "Sede Principal", criterios, "", valores, habilitado)
    field_frame.pack(padx=10, pady=10)

    criterios2 = nomMaqProdDispSede2
    valores2 = horasUsoMaqProdDispSede2
    habilitado2 = [False for _ in range(len(nomMaqProdDispSede2))]

    if senalizador == 1 or senalizador == 4:
        cont2 = tk.Frame(containerBig, bg="gray")
        cont2.pack(side="left", padx=5,pady=10)
    else:
        cont2 = tk.Frame(containerBig, bg="medium orchid")
        cont2.pack(side="left", padx=5,pady=10)
    
    field_frame2 = FieldFrame(cont2, "Sede 2", criterios2, "", valores2, habilitado2)
    field_frame2.pack(padx=10, pady=10)

    contLabelYBoton = tk.Frame(frameDeTrabajo, bg="white")
    contLabelYBoton.pack(pady=1)

    labelTextIndicador = tk.Label(contLabelYBoton, text=textIndicador, font=("Arial", 14, "bold"), bg="white", wraplength=600)
    labelTextIndicador.pack(pady=0)

    btnPlanificarProd = tk.Button(frameDeTrabajo, text="Planificar Produccion", font=("Arial", 12, "bold italic"))
    
    if senalizador == 2:
        btnPlanificarProd.bind("<Button-1>", lambda event: planProduccionn(event, containerBig, contLabelYBoton, 1))
    elif senalizador == 1:
        btnPlanificarProd.bind("<Button-1>", lambda event: planProduccionn(event, containerBig, contLabelYBoton, 2))
    elif senalizador == 3:
        btnPlanificarProd.bind("<Button-1>", lambda event: planProduccionn(event, containerBig, contLabelYBoton, 3))
    elif senalizador == 4:
        # Cuando ninguna sede esta disponible, entonces aqui se debe crear un boton pa volver
        btnPlanificarProd.config(text="Volver al inicio")
        btnPlanificarProd.bind("<Button-1>", volverMenu)
    
    btnPlanificarProd.pack(pady=5)

def volverMenu(event):
    from src.uiMain.startFrame import startFrame
    stf = startFrame()
    ventana = event.widget.winfo_toplevel()
    ventana.destroy()
    stf.cambiarFrame(stf.areaPrincipal)

aProdFinal = []
def recibeProdFinal(aProdF):
    global aProdFinal
    tempProd = []
    for listas1 in aProdF:
        for listas2 in listas1:
            for listas3 in listas2:
                tempProd.append(listas3)
    print("\n",len(tempProd) , f"- la produccion en una sola lista es: {tempProd}\n")
    aProdFinal.append(tempProd[0]); aProdFinal.append(tempProd[1]); aProdFinal.append(tempProd[4]); aProdFinal.append(tempProd[5])
    aProdFinal.append(tempProd[2]); aProdFinal.append(tempProd[3]); aProdFinal.append(tempProd[6]); aProdFinal.append(tempProd[7])
    print("\n",len(aProdFinal) , f"- la produccion cruzada en una sola lista es: {aProdFinal}\n")
    evento_senalizador.set()

enlacesP = [(0, 2), (0, 4), (0, 6)] ; enlacesPSede2 = [(4, 6)]
enlacesC = [(1, 3), (1, 5), (1, 7)] ; enlacesCSede2 = [(5, 7)]
indiceEnlaceP = 0
indiceEnlaceC = 0
direccion = False
modoP = True
idx1, idx2 = enlacesP[indiceEnlaceP]
idx3, idx4 = enlacesPSede2[0]
def planProduccionn(event, containerBig, contLyB, indicador):
    from src.uiMain.main import Main
    global descripcionF5, aProdFinal
    containerBig.destroy()
    contLyB.destroy()
    descripcionF5.destroy()
    event.widget.destroy()
    frameDeTrabajo.config(bg="white")
    contBigRecor = tk.Frame(frameDeTrabajo)
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
    evento_senalizador.wait()
    evento_senalizador.clear()
    varEntries = [tk.StringVar(value=str(aProdFinal[x])) for x in range(8)]
    #print(f"\nvalores de entrada de la interfaz: {[int(var.get()) for var in varEntries]}")
    entries = []
    flechas = []
    varIntermedio = tk.StringVar()

    def confirmarProduccion(event):
        from tkinter import messagebox
        listSobreCostos = calcularSobreCostos()
        produccionPaEnviar()
        respuesta = messagebox.askyesno("Confirmación", f"¿Deseas continuar?\n\n* Sobre Costo de la Sede Principal = {listSobreCostos[0]}\n* Sobre Costo de la Sede 2 = {listSobreCostos[1]}")
        
        if respuesta:
            messagebox.showinfo("Continuar", "¡Listo, vamos a producir las prendas!")
            print("El usuario eligió continuar.")
            contBigRecor.destroy() ; contRe1.destroy() ; recorderis.destroy() ; textRecorderis.destroy() ; separador.destroy()
            contRe2.destroy() ; recorderis2.destroy() ; textRecorderis2.destroy() ; frameGeneral.destroy() ; frameIzq.destroy() ; frameDer.destroy()
            for subf in subframes:
                subf.destroy()
            frameBotones.destroy() ; frameEntry.destroy()
            inicioInt3()
        else:
            print("El usuario canceló la acción.")

    def produccionPaEnviar():
        global aProducirPaEnviar
        valores = [int(modificados.get()) for modificados in varEntries]
        list1 = [valores[0], valores[1]] ; list2 = [valores[4], valores[5]] ; listProdHoy = [list1, list2]
        list3 = [valores[2], valores[3]] ; list4 = [valores[6], valores[7]] ; listProdOWeek = [list3, list4]
        aProducirPaEnviar = [listProdHoy, listProdOWeek]
        print(f"\nproduccion pa enviar: {aProducirPaEnviar}")

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
                val1 = int(varEntries[idx1].get())
                val2 = int(varEntries[idx2].get())
            elif indicador == 1:
                val1 = int(varEntries[idx3].get())
                val2 = int(varEntries[idx4].get())

            if direccion: 
                if val2 - valorIntermedio < 0:
                    valorIntermedio = val2
                if indicador == 3 or indicador == 2:
                    varEntries[idx1].set(str(val1 + valorIntermedio))
                    varEntries[idx2].set(str(val2 - valorIntermedio))
                elif indicador == 1:
                    varEntries[idx3].set(str(val1 + valorIntermedio))
                    varEntries[idx4].set(str(val2 - valorIntermedio))
            else:  
                if val1 - valorIntermedio < 0:
                    valorIntermedio = val1
                if indicador == 3 or indicador == 2:
                    varEntries[idx1].set(str(val1 - valorIntermedio))
                    varEntries[idx2].set(str(val2 + valorIntermedio))
                elif indicador == 1:
                    varEntries[idx3].set(str(val1 - valorIntermedio))
                    varEntries[idx4].set(str(val2 + valorIntermedio))

            varIntermedio.set("")  # Limpiar Entry intermedio
        except ValueError:
            pass  # Ignorar valores no numéricos

    def cambiarEnlaceP():
        global indiceEnlaceP, modoP, idx1, idx2, idx3, idx4
        modoP = True  # Activar modo "cambiarP"
        idx1, idx2 = enlacesP[indiceEnlaceP]  # Actualizar índices
        idx3, idx4 = enlacesPSede2[0]
        if indicador == 3:
            indiceEnlaceP = (indiceEnlaceP + 1) % len(enlacesP)
        actualizarFlechas()

    def cambiarEnlaceC():
        global indiceEnlaceC, modoP, idx1, idx2, idx3, idx4
        modoP = False  # Activar modo "cambiarC"
        idx1, idx2 = enlacesC[indiceEnlaceC]  # Actualizar índices
        idx3, idx4 = enlacesCSede2[0]
        if indicador == 3:
            indiceEnlaceC = (indiceEnlaceC + 1) % len(enlacesC)
        actualizarFlechas()

    def cambiarDireccion():
        global direccion
        direccion = not direccion
        actualizarFlechas()

    def actualizarFlechas():
        for label in flechas:
            label.config(text="")
        if indicador == 3 or indicador == 2:
            flechas[idx1].config(text="⬅" if direccion else "➡")
            flechas[idx2].config(text="➡" if not direccion else "⬅")
        elif indicador == 1:
            flechas[idx3].config(text="⬅" if direccion else "➡")
            flechas[idx4].config(text="➡" if not direccion else "⬅")

    def onFocusIn(event):
        if event.widget.get() == "Modifica aquí...":
            event.widget.delete(0, tk.END)
            event.widget.config(fg="black")

    def onFocusOut(event):
        if event.widget.get() == "":
            event.widget.insert(0, "Modifica aquí...")
            event.widget.config(fg="gray")
        # Contenedores principales con títulos
    frameGeneral = tk.Frame(frameDeTrabajo, bg="white")
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
    frameBotones = tk.Frame(frameDeTrabajo, bg="white")
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
    frameEntry = tk.Frame(frameDeTrabajo, bg="white")
    frameEntry.pack(pady=10)
    botonCambiarDir = tk.Button(frameEntry, text="Cambiar Dirección", command=cambiarDireccion, font=("Arial", 11, "bold italic"))
    botonCambiarDir.pack(side="left", padx=15)
    botonContinue = tk.Button(frameEntry, text="CONTINUAR", font=("Arial", 13, "bold italic"))
    botonContinue.pack(side="left", padx=15)
    botonContinue.bind("<Button-1>", confirmarProduccion)

    # Iniciar con los primeros enlaces resaltados
    cambiarEnlaceP()

aProducirPaEnviar = []

def inicioInt3():
    print("\nComienzo de la interacción 3...")
