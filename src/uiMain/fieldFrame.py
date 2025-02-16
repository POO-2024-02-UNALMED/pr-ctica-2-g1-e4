from tkinter import Frame, Label, Entry, Tk


class FieldFrame(Frame):

    def __init__(self, frame, tituloCriterios, criterios, tituloValores, valores=None, habilitado=None, ancho_entry=20, crecer=False, tamañoFuente=12):
        super().__init__(frame)
        self.valores = [] # No guarda la lista de valores pasada, sino los Entries creados
        self.valoresPorDefecto = valores
        self.citerios= criterios
        self.crecer=crecer
        self.tamañoFuente=tamañoFuente
        self.createWidgets(tituloCriterios,criterios,tituloValores,valores,habilitado,ancho_entry)  

    def createWidgets(self,tituloCriterios,criterios,tituloValores,valores,habilitado,ancho_entry):
        Label(self, text=tituloCriterios, font=(
            "Arial", self.tamañoFuente, "bold")).grid(row=0, column=1, pady=5)

        Label(self, text=tituloValores,  font=(
            "Arial", self.tamañoFuente, "bold")).grid(row=0, column=2, pady=5)
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
        
        if self.crecer:
            self.columnconfigure(0, weight=1)
            self.columnconfigure(3, weight=1)

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
    
    def configurarCallBack(self, criterio, evento, funcion):
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