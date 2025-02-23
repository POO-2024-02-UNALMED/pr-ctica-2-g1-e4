from typing import List, Optional

from typing import List
from src.gestorAplicacion.fecha import Fecha
from src.gestorAplicacion.bodega.insumo import Insumo
from src.gestorAplicacion.administracion.deuda import Deuda

class Proveedor:
    listaProveedores = []
    def __init__(self, precio: int = 0, nombre: str = "", insumo: Optional[Insumo] = None):
        self.precio = precio
        self.nombre = nombre
        self.descuento = 0.0
        self.deuda = Deuda(Fecha(10,1,25), 0, nombre, "Proveedor", 0)
        self.tipoInsumo = insumo
        Proveedor.listaProveedores.append(self)

    @staticmethod
    def buscarPorNombreInsumo(nombre: str) -> Optional['Proveedor']:
        for proveedor in Proveedor.listaProveedores:
            if proveedor.tipoInsumo.getNombre() == nombre:
                return proveedor
        return None

    @staticmethod
    def costoDeLaCantidad(insumo: Insumo, cantidad: int) -> int:
        precioTotal = 0
        for proveedor in Proveedor.listaProveedores:
            if proveedor.tipoInsumo.getNombre() == insumo.getNombre():
                bolsa = insumo  # Assuming Insumo is a Bolsa in this context
                precioTotal = (proveedor.precio - round(proveedor.precio * proveedor.descuento * bolsa.getCapacidadMaxima())) * cantidad
        return precioTotal

    def unificarDeudasXProveedor(self, fecha: Fecha, montoDeuda: int):
        cuotas = Deuda.calcularCuotas(montoDeuda + self.deuda.getValorInicialDeuda() - self.deuda.getCapitalPagado())
        if self.deuda.getEntidad() == self.getNombre() and not self.deuda.getEstadoDePago():
            self.deuda.actualizarDeuda(fecha, montoDeuda, cuotas)

    @classmethod
    def getListaProveedores(cls):
        return cls.listaProveedores
    @classmethod
    def setListaProveedores(cls, lista):
        cls.listaProveedores = lista
    def getDeuda(self) -> Optional[Deuda]:
        return self.deuda
    def setDeuda(self, deuda: Deuda):
        self.deuda = deuda
    def getInsumo(self) -> Optional[Insumo]:
        return self.tipoInsumo
    def setInsumo(self, insumo: Insumo):
        self.tipoInsumo = insumo
    def getPrecio(self) -> int:
        return self.precio
    def setPrecio(self, monto: int):
        self.precio = monto
    def getNombre(self) -> str:
        return self.nombre
    def setNombre(self, nombre: str):
        self.nombre = nombre
    def getDescuento(self) -> float:
        return self.descuento
    def setDescuento(self, monto: float):
        self.descuento = monto
    def __str__(self):
        return f"El proveedor {self.nombre} vende insumos de tipo {self.tipoInsumo.getNombre()} y valen {self.precio}"