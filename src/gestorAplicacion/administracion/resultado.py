class Resultado:
    # Resultado de una busqueda de un Insumo en una Sede.

    def __init__(self, encontrado=False, indice=None, sede=None, precio=None):
        self.encontrado = encontrado
        self.index = indice
        self.precio = precio
        self.sede = sede

    def getPrecio(self):
        return self.precio
    def setPrecio(self, precio):
        self.precio = precio
    def getEncontrado(self):
        return self.encontrado
    def setEncontrado(self, encontrado):
        self.encontrado = encontrado
    def getIndex(self):
        return self.index
    def setIndex(self, index):
        self.index = index
    def getSede(self):
        return self.sede
    def setSede(self, sede):
        self.sede = sede