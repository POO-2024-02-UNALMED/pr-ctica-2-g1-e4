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
        self.fechasCompra = []; self.preciosCompra = []
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

    @classmethod
    def getListadoRepuestos(cls) -> List['Repuesto']:
        from src.gestorAplicacion.sede import Sede
        repustosTotales=[]
        for sede in Sede.getListaSedes():
            for repuesto in sede.getListaRepuestos():
                if repuesto not in cls.listadoRepuestos:
                    cls.listadoRepuestos.append(repuesto)
    
    @classmethod
    def reemplazarListadoRepuestos(cls,listadoRepuestos: List['Repuesto']):
        cls.listadoRepuestos = listadoRepuestos

    @classmethod
    def removeRepuesto(cls,repuesto: 'Repuesto'):
        cls.listadoRepuestos.remove(repuesto)

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
    
    def __str__(self):
        return f"{self.nombre}"
    
    def __repr__(self):
        return self.__str__()