from tkinter import Frame, Label, Entry


class FieldFrame(Frame):

    def __init__(self, frame, tituloCriterios, criterios, tituloValores, valores, habilitado, ancho_entry=20):
        super().__init__(frame, bg="burlywood1")
        self.valores = []
        self.citerios= []
        self.createWidgets(tituloCriterios,criterios,tituloValores,valores,habilitado,ancho_entry)

    def createWidgets(self,tituloCriterios,criterios,tituloValores,valores,habilitado,ancho_entry):
        Label(self, text=tituloCriterios, font=(
            "Verdana", 16, "bold")).grid(row=0, column=0)
        Label(self, text=tituloValores,  font=(
            "Verdana", 16, "bold")).grid(row=0, column=1)


        for i, criterio in enumerate(criterios, start=1):
            Label(self, text=criterio, font=("Verdana", 16, "bold")).grid(
                row=i, column=0, padx=20, pady=5, sticky="w")
            entry = Entry(self, width=ancho_entry)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky="w")

            if valores is not None:

                entry.insert(0, valores[i - 1])

            if habilitado is not None and not habilitado[i - 1]:
                entry.config(state='readonly')


            self.valores.append(entry)

    def habilitarEntry(self, criterio, habilitar):
        entry = None
        for i, c in enumerate(self.citerios):
            if c .text == criterio:
                entry = self.valores[i]
                break

        if habilitar:
            return entry.config(state="normal")
        else:
            return entry.config(state="readonly")

    def getValue(self, criterio):
        entry = None
        for i, c in enumerate(self.citerios):
            if c .text == criterio:
                entry = self.valores[i]
                break
        return entry.get()