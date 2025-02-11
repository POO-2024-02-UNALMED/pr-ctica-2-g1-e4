import os
import tkinter as tk
from tkinter.font import Font


ventana = tk.Tk()
ventana.title("Ecomoda")
ventana.geometry("800x500")

opciones = tk.Frame(ventana, height=25)
opciones.pack(side= "top", fill="x", padx=15, pady=2)

archivoButton = tk.Button(opciones, text="Archivo")
archivoButton.place(relx=0, rely=0.5, relwidth=0.1, relheight=1, anchor="w")

procesosButton = tk.Button(opciones, text="Procesos y Consultas")
procesosButton.place(relx=0.1, rely=0.5, relwidth=0.2, relheight=1, anchor="w")

ayudaButton = tk.Button(opciones, text="Ayuda")
ayudaButton.place(relx=0.3, rely=0.5, relwidth=0.1, relheight=1, anchor="w")

inicio =  tk.Frame(ventana, bg="blue")
inicio.pack(fill="both", expand=True, padx=7, pady=7)

primerInicio = tk.Frame(inicio, height=150)
primerInicio.pack(side="top", fill="x")

label1 = tk.Label(primerInicio, text="Sistema Operativo de Ecomoda", bg="medium orchid", relief="ridge", font=("Arial",16, "bold"))
label1.place(relx=0.5, rely=0.6, relwidth=1, relheight=0.6, anchor="s") 
## relwidth y relheight reciben el porcentaje de tamaño respecto al contenedor

label2 = tk.Label(primerInicio, text="Realiza un proceso de facturación, surte insumos, produce prendas, gestiona a tus empleados y revisa el estado financiero de tu empresa :)", relief="ridge")
label2.place(relx=1, rely=0.8, relwidth=1, relheight=0.4, anchor="e")

pedirFecha = tk.Frame(inicio, bg="light gray")
pedirFecha.pack(anchor="s",  expand=True, fill="both")

label3 = tk.Label(
    pedirFecha, 
    text="\nPuedes hacerlo a través de la opción: Procesos y Consultas >>", 
    relief="ridge", 
    anchor="n",  # Asegura que el texto esté alineado arriba
    justify="center",  # Centra el texto horizontalmente
)
label3.place(relx=1, rely=1, relwidth=1, relheight=1, anchor="n")

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
    label4 = tk.Label(pedirFecha, text="¿Qué deudas que quiere calcular?", relief="ridge", anchor="w")
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
ventana.mainloop()
