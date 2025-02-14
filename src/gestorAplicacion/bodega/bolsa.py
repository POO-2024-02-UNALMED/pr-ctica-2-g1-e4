from src.gestorAplicacion.bodega.insumo import Insumo

class Bolsa(Insumo):
    def __init__(self, nombre, proveedor, cantidad=None,  sede=None, capacidad_maxima=0):
        super().__init__(nombre, proveedor, cantidad, sede)
        self.capacidad_maxima = capacidad_maxima

    # Calcula el precio de la bolsa, que puede diferir del definido como Insumo.
    def getPrecioIndividual(self):
        return round(self.precio_x_unidad - (self.precio_x_unidad * self.proveedor.get_descuento() * self.capacidad_maxima))

    def getCapacidadMaxima(self):
        return self.capacidad_maxima

    def setCapacidadMaxima(self, capacidad_maxima):
        self.capacidad_maxima = capacidad_maxima