from src.gestorAplicacion.administracion.gastoMensual import GastoMensual
from src.gestorAplicacion.sede import Sede;

class Insumo(GastoMensual):
    precio_stock_total = 0

    def __init__(self, nombre, cantidad=None, proveedor=None, sede=None, horas_de_vida_util=None):
        self.nombre = nombre
        self.proveedor = proveedor
        self.sede = sede
        if cantidad is not None and proveedor is not None:
            self.precio_compra = proveedor.get_precio() * round(cantidad)
            self.precio_x_unidad = round(self.precio_compra / cantidad)
            self.ultimo_precio = self.precio_x_unidad
            Insumo.precio_stock_total += self.precio_compra
            sede.get_lista_insumos_bodega().append(self)
            sede.get_cantidad_insumos_bodega().append(round(cantidad))
        elif proveedor is not None:
            self.precio_x_unidad = proveedor.get_precio()
        if horas_de_vida_util is not None:
            self.horas_de_vida_util = horas_de_vida_util

    @staticmethod
    def gastoMensualClase(fecha):
        gasto_insumo = 0
        gasto_actual = 0
        gasto_pasado = 0
        for sede in Sede.get_lista_sedes():
            for venta in sede.get_historial_ventas():
                for insumo in venta.get_bolsas():
                    lista = insumo.gasto_mensual_tipo(fecha, venta.get_fecha_venta(), insumo)
                    gasto_actual += lista[0]
                    gasto_pasado += lista[1]
                    if gasto_actual != 0:
                        gasto_insumo = gasto_actual
                    else:
                        gasto_insumo = gasto_pasado
        return gasto_insumo

    def calcularGastoMensual(self):
        valor = 0
        for i in range(len(self.sede.get_lista_insumos_bodega())):
            if self.sede.get_lista_insumos_bodega()[i] == self:
                valor = self.getPrecioIndividual() * self.sede.get_cantidad_insumos_bodega()[i]
        return valor

    @staticmethod
    def getPrecioStockTotal():
        return Insumo.precio_stock_total

    @staticmethod
    def setPrecioStockTotal(precio_stock_total):
        Insumo.precio_stock_total = precio_stock_total

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
        return self.precio_compra

    def setPrecioCompra(self, precio):
        self.precio_compra = precio

    def getPrecioIndividual(self):
        return self.precio_x_unidad

    def setUltimoPrecio(self, precio):
        self.ultimo_precio = precio

    def getUltimoPrecio(self):
        return self.ultimo_precio

    def __str__(self):
        return f"Insumo: {self.nombre}"