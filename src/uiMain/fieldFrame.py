from tkinter import Frame, Label, Entry, Tk, Button
from src.uiMain.Excepciones.errorAplicacion import ErrorAplicacion
from src.uiMain.Excepciones.exceptionC1 import ExcepcionContenidoVacio
from tkinter import messagebox

class FieldFrame(Frame):

    #  aceptar y borrar se refieren a los respectivos botones que se pueden añadir al final del frame
    def __init__(self, frame, tituloCriterios, criterios, tituloValores, valores=None, habilitado=None, ancho_entry=20, crecer=False, tamañoFuente=12, aceptar=False,borrar=False, callbackAceptar=None):
        super().__init__(frame)
        self.valores = [] # No guarda la lista de valores pasada, sino los Entries creados
        self.valoresPorDefecto = valores
        self.citerios= criterios
        self.crecer=crecer
        self.tamañoFuente=tamañoFuente
        self.callbackAceptar=callbackAceptar
        self.createWidgets(tituloCriterios,criterios,tituloValores,valores,habilitado,ancho_entry,aceptar,borrar)  

    def createWidgets(self,tituloCriterios,criterios,tituloValores,valores,habilitado,ancho_entry,aceptar,borrar):
        Label(self, text=tituloCriterios, font=( "Arial", self.tamañoFuente, "bold")).grid(row=0, column=1, pady=5)
        Label(self, text=tituloValores,  font=( "Arial", self.tamañoFuente, "bold")).grid(row=0, column=2, pady=5)
        self.columnconfigure(0,weight=3)
        self.columnconfigure(1,weight=1)
        self.columnconfigure(2,weight=1)
        self.columnconfigure(3,weight=3)

        for i, criterio in enumerate(criterios, start=1):
            Label(self, text=criterio, font=("Arial", self.tamañoFuente, "bold")).grid(
                row=i, column=1, pady=5, sticky="n")
            entry = Entry(self, width=ancho_entry, bg="plum3")
            entry.grid(row=i, column=2, pady=5)
            self.columnconfigure(0,weight=3)
            self.columnconfigure(1,weight=1)
            self.columnconfigure(2,weight=1)
            self.columnconfigure(3,weight=3)

            if valores is not None:
                entry.insert(0, valores[i - 1])

            if habilitado is not None and not habilitado[i - 1]:
                entry.config(state='readonly')

            self.valores.append(entry)
        
        if aceptar:
            self.aceptar=Button(self,text="Aceptar",font=("Arial", self.tamañoFuente, "bold"),command=self.callbackAceptar)
            self.aceptar.grid(row=i+1,column=1)
        if borrar:
            self.borrar=Button(self,text="Borrar",font=("Arial", self.tamañoFuente, "bold"),command=self.borrar)
            self.borrar.grid(row=i+1,column=2)
        
        if self.crecer:
            self.columnconfigure(0, weight=1)
            self.columnconfigure(3, weight=1)
    
    def aceptar(self):
        try:
            entradas = self.obtenerTodosLosValores()
            vacios = []
            hayExcepcion = False
            for valor in entradas:
               for i in range(len(self.valores)):
                if self.valores[i].get() == "" and valor.strip() == "":
                    vacios.append(self.valores[i]) 
                    hayExcepcion = True
            if hayExcepcion:
                raise ExcepcionContenidoVacio(vacios)
        except ExcepcionContenidoVacio as moscorrofio:
            messagebox.showwarning(title="Alerta",message=moscorrofio.mensaje_completo)
            return hayExcepcion

    def habilitarEntry(self, criterio, habilitar):
        entry = None
        for i, c in enumerate(self.citerios):
            if c == criterio:
                entry = self.valores[i]
                break
        if habilitar:
            return entry.config(state="normal")
        else:
            return entry.config(state="readonly")

    def getValue(self, criterio):
        entry = None
        for i, c in enumerate(self.citerios):
            if c == criterio:
                entry = self.valores[i]
                break
        return entry.get()

    def obtenerTodosLosValores(self):
        return [entry.get() for entry in self.valores]
    
    def configurarCallBack(self, criterio:str, evento, funcion):
        entry = None
        for i, c in enumerate(self.citerios):
            if c == criterio:
                entry = self.valores[i]
                break
        return entry.bind(evento, funcion)

    def borrar(self):
        if self.valoresPorDefecto is not None:
            for i, c in enumerate(self.valoresPorDefecto):
                self.valores[i].delete(0, "end")
                self.valores[i].insert(0, c)
        else:
            for i in self.valores:
                i.delete(0, "end")