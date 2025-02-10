from typing import List, Optional

from typing import List
from src.gestorAplicacion.fecha import Fecha
from src.gestorAplicacion.bodega.insumo import Insumo
from src.gestorAplicacion.administracion.deuda import Deuda

class Proveedor:
    lista_proveedores=[]

    def __init__(self, precio: int = 0, nombre: str = "", insumo: Optional[Insumo] = None):
        self.precio = precio
        self.nombre = nombre
        self.descuento = 0.0
        self.deuda = None
        self.tipo_insumo = insumo
        Proveedor.lista_proveedores.append(self)

    @staticmethod
    def buscarPorNombreInsumo(nombre: str) -> Optional['Proveedor']:
        for proveedor in Proveedor.lista_proveedores:
            if proveedor.tipo_insumo.get_nombre() == nombre:
                return proveedor
        return None

    @staticmethod
    def costoDeLaCantidad(insumo: Insumo, cantidad: int) -> int:
        precio_total = 0
        for proveedor in Proveedor.lista_proveedores:
            if proveedor.tipo_insumo == insumo:
                bolsa = insumo  # Assuming Insumo is a Bolsa in this context
                precio_total = (proveedor.precio - round(proveedor.precio * proveedor.descuento * bolsa.get_capacidad_maxima())) * cantidad
        return precio_total

    def unificarDeudasXProveedor(self, fecha: Fecha, monto_deuda: int):
        cuotas = Deuda.calcularCuotas(monto_deuda + self.deuda.get_valor_inicial_deuda() - self.deuda.getCapitalPagado())
        if self.deuda.getEntidad() == self.getNombre() and not self.deuda.get_estado_de_pago():
            self.deuda.actualizarDeuda(fecha, monto_deuda, cuotas)

    @classmethod
    def getListaProveedores(cls):
        return cls.lista_proveedores

    @classmethod
    def setListaProveedores(cls, lista):
        cls.lista_proveedores = lista

    def getDeuda(self) -> Optional[Deuda]:
        return self.deuda

    def setDeuda(self, deuda: Deuda):
        self.deuda = deuda

    def getInsumo(self) -> Optional[Insumo]:
        return self.tipo_insumo

    def setInsumo(self, insumo: Insumo):
        self.tipo_insumo = insumo

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
        return f"El proveedor {self.nombre} vende insumos de tipo {self.tipo_insumo.getNombre()} y valen {self.precio}"