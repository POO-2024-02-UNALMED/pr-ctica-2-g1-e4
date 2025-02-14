from typing import List
from ..fecha import Fecha
from .insumo import Insumo
from .proveedor import Proveedor

class Repuesto(Insumo):
    listado_repuestos = []

    def __init__(self, nombre: str, proveedor: Proveedor, horas_de_vida_util: int, cantidad=None,sede=None):
        super().__init__(nombre, proveedor, cantidad, sede)
        self.nombre = nombre
        self.horas_de_vida_util = horas_de_vida_util
        self.proveedor = proveedor
        self.fechas_compra = []
        self.precios_compra = []
        self.horas_de_uso = 0
        self.estado = True
        Repuesto.listado_repuestos.append(self)

    def getFechasCompra(self) -> List[Fecha]:
        return self.fechas_compra

    def getFechasCompra(self, fecha_compra: Fecha):
        self.fechas_compra.append(fecha_compra)

    def getPreciosCompra(self) -> List[int]:
        return self.precios_compra

    def setPreciosCompra(self, precio: int):
        self.precios_compra.append(precio)

    def getNombre(self) -> str:
        return self.nombre

    def getHorasDeVidaUtil(self) -> int:
        return self.horas_de_vida_util

    def setHorasDeUso(self, horas: int):
        self.horas_de_uso += horas

    def getHorasDeUso(self) -> int:
        return self.horas_de_uso

    @staticmethod
    def getListadoRepuestos() -> List['Repuesto']:
        return Repuesto.listado_repuestos

    @staticmethod
    def reemplazarListadoRepuestos(listado_repuestos: List['Repuesto']):
        Repuesto.listado_repuestos = listado_repuestos

    @staticmethod
    def setListadoRepuestos(repa_retirar: 'Repuesto'):
        Repuesto.listado_repuestos.remove(repa_retirar)

    def setEstado(self):
        self.estado = False

    def isEstado(self) -> bool:
        return self.estado

    def copiar(self) -> 'Repuesto':
        return Repuesto(self.nombre, self.proveedor, self.horas_de_vida_util,)

    def copiar_con_proveedor(self, prov_barato: 'Proveedor') -> 'Repuesto':
        return Repuesto(self.nombre, self.horas_de_vida_util, prov_barato)

    def calcularGastoMensual(self, fecha: Fecha) -> int:
        gasto_mensual = 0
        for i in range(len(self.fechas_compra)):
            if self.fechas_compra[i].year == fecha.year and self.fechas_compra[i].month == fecha.month:
                gasto_mensual += self.precios_compra[i]
        return gasto_mensual

    def usar(self, horas: int):
        self.horas_de_uso += horas