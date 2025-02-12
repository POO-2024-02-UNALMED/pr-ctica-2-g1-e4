import tkinter as tk
import os
from src.uiMain.main import Main
from src.gestorAplicacion.fecha import Fecha

class frameInicial(tk.Frame):
    def __init__(self,master):
        super().__init__(master)
        self.create_widgets()

    def create_widgets(self):

        primerInicio = tk.Frame(self, height=150)
        primerInicio.pack(side="top", fill="x")

        #lbl_font = Font(family="Roboto Cn", size=17) 

        label1 = tk.Label(primerInicio, text="Sistema Operativo de Ecomoda", bg="medium orchid", relief="ridge", font=("Arial",16, "bold"))
        label1.place(relx=0.5, rely=0.6, relwidth=1, relheight=0.6, anchor="s") 
        ## relwidth y relheight reciben el porcentaje de tamaño respecto al contenedor

        label2 = tk.Label(primerInicio, text="Realiza un proceso de facturación, surte insumos, produce prendas, gestiona a tus empleados y revisa el estado financiero de tu empresa :)", relief="ridge")
        label2.place(relx=1, rely=0.8, relwidth=1, relheight=0.4, anchor="e")

        pedirFecha = tk.Frame(self, bg="light gray")
        pedirFecha.pack(fill="both", expand=True, anchor="s")

        label3 = tk.Label(
            pedirFecha, 
            text="\nPuedes hacerlo a través de la opción: Procesos y Consultas >>", 
            relief="ridge", 
            anchor="n",  # Asegura que el texto esté alineado arriba
            justify="center",  # Centra el texto horizontalmente
        )
        label3.place(relx=0.5, rely=0, relwidth=1, relheight=0.7, anchor="n")

        logo = tk.PhotoImage(master=label3, file=f"{os.getcwd()}\\src\\uiMain\\imagenes\\logoEcomoda.png")

        # Redimensionar la imagen usando subsample()
        # La imagen será reducida al tamaño deseado sin recortes
        logo_resized = logo.subsample(2, 2)  

        # Crear el label con la imagen redimensionada
        foto = tk.Label(master=label3, image=logo_resized, bg="light gray")
        foto.image = logo_resized  # Mantener la referencia de la imagen
        foto.place(relx=0.5, rely=0.24, anchor="n")

        label4 = tk.Label(pedirFecha, text="Para iniciar ingresa la fecha de hoy ", relief="ridge", anchor="w")
        label4.place(relx=0.5, rely=0.7, relwidth=1, relheight=0.3, anchor="n")
        label4.config(padx=200)  

        self.entradaDia =tk.Entry(pedirFecha, bg="plum3")
        self.entradaDia.place(relx=0.55, rely=0.8, relwidth=0.06, relheight=0.1, anchor="n")
        self.entradaDia.insert(0,"d/ ")
        self.entradaMes =tk.Entry(pedirFecha, bg="plum3")
        self.entradaMes.place(relx=0.615, rely=0.8, relwidth=0.06, relheight=0.1, anchor="n")
        self.entradaMes.insert(0,"m/ ")
        self.entradaAño =tk.Entry(pedirFecha, bg="plum3")
        self.entradaAño.place(relx=0.6849, rely=0.8, relwidth=0.07, relheight=0.1, anchor="n")
        self.entradaAño.insert(0,"a/ ")


        boton1=tk.Button(pedirFecha,text="Enviar")
        boton1.place(relx=0.820, rely=0.8, relwidth=0.1, relheight=0.1, anchor="n")
        boton1.bind("<Button-1>", self.Ok)


        # Función que se ejecutará al presionar el botón
    def Ok(self,event):
        # Leer los valores de las entradas
        FDia = self.entradaDia.get() # Obtener el texto de la entrada para el día
        FMes = self.entradaMes.get() # Obtener el texto de la entrada para el mes
        FAño = self.entradaAño.get() # Obtener el texto de la entrada para el año
        self.ingresarFecha(FDia,FMes,FAño)
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
        elif mes <= 0 or mes > 12:
            self.borrar()
        elif año <= 0:
            self.borrar()
        else:
            fecha = Fecha(dia, mes, año)
            Main.fecha=fecha
        return fecha