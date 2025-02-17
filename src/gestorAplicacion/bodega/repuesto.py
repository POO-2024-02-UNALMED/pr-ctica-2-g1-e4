from typing import List
from ..fecha import Fecha
from .insumo import Insumo
from .proveedor import Proveedor

class Repuesto(Insumo):
    listadoRepuestos = []

    def __init__(self, nombre: str, proveedor: Proveedor, horasDeVidaUtil: int, cantidad=None, sede=None, horasDeUso=0):
        super().__init__(nombre, proveedor, cantidad, sede)
        self.nombre = nombre
        self.horasDeVidaUtil = horasDeVidaUtil
        self.proveedor = proveedor
        self.fechasCompra = []
        self.preciosCompra = []
        self.horasDeUso = horasDeUso
        self.estado = True
        Repuesto.listadoRepuestos.append(self)
        

    def getFechasCompra(self) -> List[Fecha]:
        return self.fechasCompra
    def addFechaCompra(self, fechaCompra: Fecha):
        self.fechasCompra.append(fechaCompra)
    def getPreciosCompra(self) -> List[int]:
        return self.preciosCompra
    def addPrecioCompra(self, precio: int):
        self.preciosCompra.append(precio)
    def getNombre(self) -> str:
        return self.nombre
    def getHorasDeVidaUtil(self) -> int:
        return self.horasDeVidaUtil
    def addHorasDeUso(self, horas: int):
        self.horasDeUso += horas
    def getHorasDeUso(self) -> int:
        return self.horasDeUso
    @staticmethod
    def getListadoRepuestos() -> List['Repuesto']:
        return Repuesto.listadoRepuestos
    @staticmethod
    def reemplazarListadoRepuestos(listadoRepuestos: List['Repuesto']):
        Repuesto.listadoRepuestos = listadoRepuestos
    @staticmethod
    def removeRepuesto(repuesto: 'Repuesto'):
        Repuesto.listadoRepuestos.remove(repuesto)
    def setEstado(self):
        self.estado = False
    def isEstado(self) -> bool:
        return self.estado
    
    def copiar(self) -> 'Repuesto':
        return Repuesto(self.nombre, self.proveedor, self.horasDeVidaUtil)

    def copiarConProveedor(self, provBarato: 'Proveedor') -> 'Repuesto':
        return Repuesto(self.nombre, provBarato, self.horasDeVidaUtil)

    def calcularGastoMensual(self, fecha: Fecha) -> int:
        gastoMensual = 0
        for i in range(len(self.fechasCompra)):
            if self.fechasCompra[i].year == fecha.year and self.fechasCompra[i].month == fecha.month:
                gastoMensual += self.preciosCompra[i]
        return gastoMensual

    def usar(self, horas: int):
        self.horasDeUso += horas