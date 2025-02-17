import math
import os
import tkinter as tk
from tkinter.font import Font

from src.gestorAplicacion.bodega import prenda
from src.gestorAplicacion.bodega.camisa import Camisa
from src.gestorAplicacion.bodega.pantalon import Pantalon
from src.gestorAplicacion.sede import Sede

from src.gestorAplicacion.venta import Venta



class F2Insumos(tk.Frame):

    def __init__(self,master):
        super().__init__(master)
        self.pesimismo()

    def pesimismo(self):

        from src.uiMain.main import Main
        from src.uiMain import fieldFrame, main

        criterios = []
        valores = []
        framePrincipal =  tk.Frame(self, bg="blue")
        framePrincipal.pack(fill="both", expand=True, padx=7, pady=7)

        frame1 = tk.Frame(framePrincipal, height=150)
        frame1.pack(side="top", fill="x")

        tituloF2 = tk.Label(frame1, text="Surtir Insumos", bg="medium orchid", relief="ridge", font=("Arial",16, "bold"))
        tituloF2.place(relx=0.5, rely=0.6, relwidth=1, relheight=0.6, anchor="s") 
        ## relwidth y relheight reciben el porcentaje de tamaño respecto al contenedor

        descripcionF2 = tk.Label(frame1, text="Registra la llegada de nuevos insumos: Incluye una predicción de ventas del siguiente mes para hacer la compra de los insumos, actualiza la deuda con los proveedores y añade los nuevos insumos a la cantidad en Stock.", relief="ridge",wraplength=600)
        descripcionF2.place(relx=1, rely=0.8, relwidth=1, relheight=0.4, anchor="e")

        frame2 = tk.Frame(framePrincipal, bg="light gray")
        frame2.pack(anchor="s",  expand=True, fill="both")

        for s in Sede.getListaSedes():
            criterios.append(s)
            valores.append(f"{round(Venta.getPesimismo()*100)}%")

        field = fieldFrame.FieldFrame(frame2, "Puede cambiar la prediccion de ventas para el siguiente mes...", criterios, "", valores, [True, True])
        field.pack(anchor="s",  expand=True, fill="both")
        fecha =main.Main.fecha
        pantalonesPredichos = False
        camisasPredichas = False

        for sede in Sede.getListaSedes():
            for prenda in Sede.getPrendasInventadas(sede):
                if isinstance(prenda, Pantalon) and not pantalonesPredichos:
                    proyeccion = Venta.predecirVentas(fecha, sede, prenda.getNombre())
                    prediccionP = proyeccion * (1 - Venta.getPesimismo())
                    print("\nLa predicción de ventas para " + str(prenda) + " es de " + str(math.ceil(prediccionP)))

                    F2Insumos.prediccion(frame2, sede, prenda, prediccionP)

                    pantalonesPredichos = True


                if isinstance(prenda, Camisa) and not camisasPredichas:
                    proyeccion = Venta.predecirVentas(fecha, sede, prenda.getNombre())
                    prediccionC = proyeccion * (1 - Venta.getPesimismo())
                    print("\nLa predicción de ventas para " + str(prenda) + " es de " + str(math.ceil(prediccionC)))

                    F2Insumos.prediccion(frame2, sede, prenda, prediccionC)

                    camisasPredichas = True

        #Main.planificarProduccion(main.Main.fecha, frame2)

    def prediccion(frame2, sede, prenda, prediccion):
        prediccion = tk.Label(frame2,text="\nLa predicción de ventas para " + str(prenda) + " es de " + str(math.ceil(prediccion)) + " en la "+ str(sede))
        prediccion.place(relx=1, rely=0.8, relwidth=1, relheight=0.4, anchor="e")

        
        
        

