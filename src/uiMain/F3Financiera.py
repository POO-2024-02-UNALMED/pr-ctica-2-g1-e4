import os
import tkinter as tk
from tkinter.font import Font

def deudas(ventana:tk.Frame):

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


    elecionDeuda = None
    def elecionDeudas(event,boton):
        global elecionDeuda
        if boton.cget('text') == "Proveedor":
            elecionDeuda = 1
        elif boton.cget('text') == "Banco":
            elecionDeuda = 2
        elif boton.cget('text') == "Ambos":
            elecionDeuda = 3

    def getElecionDeuda():
        global elecionDeuda 
        return  elecionDeuda 

    def Deudas ():
        label4 = tk.Label(frame2, text="¿Qué deudas que quiere calcular?", relief="ridge", anchor="w")
        label4.place(relx=0.5, rely=0.2, relwidth=1, relheight=0.2, anchor="s")
        label4.config(padx=200)  
        boton1=tk.Button(label4,text="Proveedor")
        boton1.place(relx=0.55, rely=0.3, relwidth=0.08, relheight=0.4, anchor="n")
        boton1.bind("<Button-1>", lambda event, boton=boton1: elecionDeudas(event, boton))
        boton2=tk.Button(label4,text="Banco")
        boton2.place(relx=0.640, rely=0.3, relwidth=0.08, relheight=0.4, anchor="n")
        boton2.bind("<Button-1>", lambda event, boton=boton2: elecionDeudas(event, boton))
        boton3=tk.Button(label4,text="Ambos")
        boton3.place(relx=0.730, rely=0.3, relwidth=0.08, relheight=0.4, anchor="n")
        boton3.bind("<Button-1>", lambda event, boton=boton3: elecionDeudas(event, boton))

    Deudas()