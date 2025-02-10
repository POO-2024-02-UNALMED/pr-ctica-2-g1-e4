from gestorAplicacion import fecha
from typing import List

from src.gestorAplicacion.administracion.banco import Banco
from src.gestorAplicacion.fecha import Fecha
from src.gestorAplicacion.bodega.proveedor import Proveedor
from src.gestorAplicacion.bodega.pantalon import Pantalon
from src.gestorAplicacion.bodega.camisa import Camisa

class Deuda:
    lista_deudas: List['Deuda'] = []

    def __init__(self, fecha: Fecha, valor: int, entidad: str, tipo: str, cuotas: int):
        self.FECHA_CREACION = fecha
        self.valorinicial_deuda = valor
        self.entidad = entidad
        self.tipo_entidad = tipo
        self.cuotas = cuotas
        self.interes = 0.0
        self.estadode_pago = False
        self.capital_pagado = 0

        Deuda.lista_deudas.append(self)

        if tipo == "Banco":
            for banco in Banco.get_lista_bancos():
                if banco.get_nombre_entidad() == entidad:
                    self.interes = banco.get_interes()

    def deudaActual(self, año: int) -> int:
        deuda_acumulada = 0
        if not self.estadode_pago:
            años = self.cuotas - año - self.FECHA_CREACION.year
            deuda_acumulada += round((self.valorinicial_deuda - self.capital_pagado) +
                                      (self.valorinicial_deuda - self.capital_pagado) * self.interes * años)
        return deuda_acumulada

    def deudaMensual(self, año: int) -> int:
        deuda_actual = self.deudaActual(año)
        deuda_mensual = round(deuda_actual / (self.cuotas - (año - self.FECHA_CREACION.year)))
        return deuda_mensual

    @staticmethod
    def calcularDeudaMensual(fecha, eleccion: int) -> int:
        deuda_calculada = 0
        if eleccion == 1:
            for proveedor in Proveedor.getListaProveedores():
                deuda_p = proveedor.get_deuda()
                lista_insumos = Pantalon.get_tipo_insumo()
                lista_insumos.extend(Camisa.getTipoInsumo())
                if deuda_p is not None:
                    if proveedor.get_insumo().get_nombre() in lista_insumos:
                        deuda_calculada += deuda_p.deuda_mensual(fecha.year)
        elif eleccion == 2:
            for banco in Banco.get_lista_bancos():
                for deuda_b in banco.get_deuda():
                    deuda_calculada += deuda_b.deuda_mensual(fecha.year)
        elif eleccion == 3:
            for proveedor in Proveedor.getListaProveedores():
                deuda_p = proveedor.get_deuda()
                lista_insumos = Pantalon.get_tipo_insumo()
                lista_insumos.extend(Camisa.getTipoInsumo())
                if deuda_p is not None:
                    if proveedor.get_insumo().get_nombre() in lista_insumos:
                        deuda_calculada += deuda_p.deuda_mensual(fecha.year)
            for banco in Banco.get_lista_bancos():
                for deuda_b in banco.get_deuda():
                    deuda_calculada += deuda_b.deuda_mensual(fecha.year)

        return deuda_calculada

    @staticmethod
    def calcularCuotas(monto: int) -> int:
        if 0 <= monto <= 1_000_000:
            return 1
        elif 1_000_000 < monto < 10_000_000:
            return 7
        elif 10_000_000 < monto < 20_000_000:
            return 12
        elif monto > 20_000_000:
            return 25
        return 0

    def __str__(self):
        return f"La deuda con el {self.tipo_entidad} {self.entidad} inició con un valor de: {self.valorinicial_deuda}\n" + \
               f"Con un interés de: {self.interes} y se debía pagar en: {self.cuotas} cuotas\n" + \
               f"Por ahora se ha pagado {self.capital_pagado}"

    @classmethod
    def getListaDeudas(cls):
        return cls.lista_deudas

    def getValorinicialDeuda(self):
        return self.valorinicial_deuda

    def getInteres(self):
        return self.interes

    def getEstadodePago(self):
        return self.estadode_pago

    def getEntidad(self):
        return self.entidad

    def getTipoEntidad(self):
        return self.tipo_entidad

    def getCapitalPagado(self):
        return self.capital_pagado

    def getFechaCreacion(self):
        return self.FECHACREACION

    @classmethod
    def setListaDeudas(cls, lista_deudas):
        if lista_deudas is None:
            raise ValueError("La lista no puede ser nula")
        cls.lista_deudas = lista_deudas

    def setValorinicialDeuda(self, valorinicial_deuda):
        self.valorinicial_deuda = valorinicial_deuda

    def setInteres(self, interes):
        self.interes = interes

    def setEstadodePago(self, estadode_pago):
        self.estadode_pago = estadode_pago

    def setEntidad(self, entidad):
        self.entidad = entidad

    def setCapitalPagado(self, capital_pagado):
        self.capital_pagado = capital_pagado

    def actualizarDeuda(self, fecha, monto_deuda, cuotas):
        deuda_actual = self.deudaActual(fecha.get_año())
        self.valorinicial_deuda = monto_deuda + deuda_actual
        self.capital_pagado = 0
        self.cuotas = cuotas

    @staticmethod
    def compararDeudas(fecha):
        mayor_banco = None
        mayor_proveedor = None
        mayor_precio_b = 0
        mayor_precio_p = 0
        deuda_p = None
        deuda_b = None

        for deuda in Deuda.lista_deudas:
            for proveedor in Proveedor.getListaProveedores():
                if proveedor.get_deuda() is not None:
                    deudap = proveedor.get_deuda().deuda_actual(fecha.get_año())
                    if deudap != 0 and not proveedor.get_deuda().estadode_pago and deudap > mayor_precio_p:
                        mayor_precio_p = deudap
                        mayor_proveedor = proveedor
                        deuda_p = proveedor.get_deuda()

            for banco in Banco.get_lista_bancos():
                for deudaa in banco.get_deuda():
                    if deudaa is not None:
                        deudab = deudaa.deuda_actual(fecha.get_año())
                        if deudab != 0 and not deudaa.estadode_pago and deudab > mayor_precio_b:
                            mayor_precio_b = deudab
                            mayor_banco = banco
                            deuda_b = deudaa

        pago_p = deuda_p.pagar_deuda(fecha)
        deuda_p.capital_pagado += deuda_p.deuda_actual(fecha.get_año()) - pago_p
        pago_b = deuda_b.pagar_deuda(fecha)
        deuda_b.capital_pagado += deuda_b.deuda_actual(fecha.get_año()) - pago_b

    def pagarDeuda(self, fecha):
        pagar = self.deudaActual(fecha.get_año())
        for banco in Banco.get_lista_bancos():
            while banco.get_ahorro_banco() >= 3_000_000:
                if pagar > 0 and pagar - 500_000 >= 0:
                    banco.set_ahorro_banco(banco.get_ahorro_banco() - 500_000)
                    pagar -= 500_000
                elif pagar > 0:
                    banco.set_ahorro_banco(banco.get_ahorro_banco() - pagar)
                elif pagar == 0:
                    self.estadode_pago = True
                    break
        return pagar


