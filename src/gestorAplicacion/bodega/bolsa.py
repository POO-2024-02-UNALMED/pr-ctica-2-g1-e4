from src.gestorAplicacion.bodega.insumo import Insumo

class Bolsa(Insumo):
    def __init__(self, nombre, proveedor, cantidad=None, sede=None, capacidadMaxima=0):
        super().__init__(nombre, proveedor, cantidad, sede)
        self.capacidadMaxima = capacidadMaxima

    # Calcula el precio de la bolsa, que puede diferir del definido como Insumo.
    def getPrecioIndividual(self):
        return round(self.precioXUnidad - (self.precioXUnidad * self.proveedor.getDescuento() * self.capacidadMaxima))

    def getCapacidadMaxima(self):
        return self.capacidadMaxima

    def setCapacidadMaxima(self, capacidadMaxima):
        self.capacidadMaxima = capacidadMaxima