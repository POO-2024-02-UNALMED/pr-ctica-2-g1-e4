from src.gestorAplicacion.administracion.gastoMensual import GastoMensual

class Insumo(GastoMensual):
    precioStockTotal = 0

    def __init__(self, nombre, proveedor=None, cantidad=None, horasDeVidaUtil=None, sede=None):
        self.nombre = nombre
        self.proveedor = proveedor
        self.sede = sede
        if cantidad is not None and proveedor is not None and sede is not None:
            self.precioCompra = proveedor.getPrecio() * round(cantidad)
            self.precioXUnidad = round(self.precioCompra / cantidad)
            self.ultimoPrecio = self.precioXUnidad
            Insumo.precioStockTotal += self.precioCompra
            sede.getListaInsumosBodega().append(self)
            sede.getCantidadInsumosBodega().append(round(cantidad))
        elif proveedor is not None:
            self.precioXUnidad = proveedor.getPrecio()
        if horasDeVidaUtil is not None:
            self.horasDeVidaUtil = horasDeVidaUtil

    @staticmethod
    def gastoMensualClase(fecha):
        from src.gestorAplicacion.sede import Sede
        gastoInsumo = 0
        gastoActual = 0
        gastoPasado = 0
        for sede in Sede.getListaSedes():
            for venta in sede.getHistorialVentas():
                for insumo in venta.getBolsas():
                    lista = insumo.gastoMensualTipo(fecha, venta.getFechaVenta(), insumo)
                    gastoActual += lista[0]
                    gastoPasado += lista[1]
                    if gastoActual != 0:
                        gastoInsumo = gastoActual
                    else:
                        gastoInsumo = gastoPasado
        return gastoInsumo

    def calcularGastoMensual(self):
        valor = 0
        for i in range(len(self.sede.getListaInsumosBodega())):
            if self.sede.getListaInsumosBodega()[i] == self:
                valor = self.getPrecioIndividual() * self.sede.getCantidadInsumosBodega()[i]
        return valor

    @staticmethod
    def getPrecioStockTotal():
        return Insumo.precioStockTotal
    @staticmethod
    def setPrecioStockTotal(precioStockTotal):
        Insumo.precioStockTotal = precioStockTotal
    def getNombre(self):
        return self.nombre
    def setNombre(self, nombre):
        self.nombre = nombre
    def getProveedor(self):
        return self.proveedor
    def setProveedor(self, proveedor):
        self.proveedor = proveedor
    def getSede(self):
        return self.sede
    def setSede(self, sede):
        self.sede = sede
    def getPrecioCompra(self):
        return self.precioCompra
    def setPrecioCompra(self, precio):
        self.precioCompra = precio
    def getPrecioIndividual(self):
        return self.precioXUnidad
    def setUltimoPrecio(self, precio):
        self.ultimoPrecio = precio
    def getUltimoPrecio(self):
        return self.ultimoPrecio
    def __str__(self):
        return f"Insumo: {self.nombre}"