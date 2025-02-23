from src.gestorAplicacion import fecha
from typing import List

from src.gestorAplicacion.administracion.banco import Banco
from src.gestorAplicacion.fecha import Fecha
from src.gestorAplicacion.bodega.pantalon import Pantalon
from src.gestorAplicacion.bodega.camisa import Camisa

class Deuda:
    listaDeudas= []

    def __init__(self, fecha: Fecha, valor: int, entidad: str, tipo: str, cuotas: int):
        self.fechaCreacion = fecha
        self.valorInicialDeuda = valor
        self.entidad = entidad
        self.tipoEntidad = tipo
        self.cuotas = cuotas
        self.interes = 0.0
        self.estadoDePago = False
        self.capitalPagado = 0
        Deuda.listaDeudas.append(self)
        if tipo == "Banco":
            for banco in Banco.getListaBancos():
                if banco.getNombreEntidad() == entidad:
                    self.interes = banco.getInteres()

    def deudaActual(self, ano: int) -> int:
        deudaAcumulada = 0
        if self.estadoDePago != True:
            anos = self.cuotas - ano - self.fechaCreacion.ano
            deudaAcumulada += round((self.valorInicialDeuda - self.capitalPagado) +(self.valorInicialDeuda - self.capitalPagado) * self.interes * anos)
        return deudaAcumulada

    def deudaMensual(self, ano: int) -> int:
        deudaActual = self.deudaActual(ano)
        deudaMensual = round(deudaActual / (self.cuotas - (ano - self.fechaCreacion.ano)))
        return deudaMensual

    @staticmethod
    def calcularDeudaMensual(fecha, eleccion: int) -> int:
        from src.gestorAplicacion.bodega.proveedor import Proveedor
        deudaCalculada = 0
        if eleccion == 1:
            for proveedor in Proveedor.getListaProveedores():
                deudaP = proveedor.getDeuda()
                listaInsumos = Pantalon.getTipoInsumo()
                listaInsumos.extend(Camisa.getTipoInsumo())
                if deudaP is not None:
                    if proveedor.getInsumo().getNombre() in listaInsumos:
                        deudaCalculada += deudaP.deudaMensual(fecha.ano)
        elif eleccion == 2:
            for banco in Banco.getListaBancos():
                for deudaB in banco.getDeuda():
                    deudaCalculada += deudaB.deudaMensual(fecha.ano)
        elif eleccion == 3:
            for proveedor in Proveedor.getListaProveedores():
                deudaP = proveedor.getDeuda()
                listaInsumos = Pantalon.getTipoInsumo()
                listaInsumos.extend(Camisa.getTipoInsumo())
                if deudaP is not None:
                    if proveedor.getInsumo().getNombre() in listaInsumos:
                        deudaCalculada += deudaP.deudaMensual(fecha.ano)
            for banco in Banco.getListaBancos():
                for deudaB in banco.getDeuda():
                    deudaCalculada += deudaB.deudaMensual(fecha.ano)
        return deudaCalculada

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
        return f"La deuda con el {self.tipoEntidad} {self.entidad} inició con un valor de: {self.valorInicialDeuda}\n" + \
               f"Con un interés de: {self.interes} y se debía pagar en: {self.cuotas} cuotas\n" + \
               f"Por ahora se ha pagado {self.capitalPagado}"
    @classmethod
    def getListaDeudas(cls):
        return cls.listaDeudas
    def getValorInicialDeuda(self):
        return self.valorInicialDeuda
    def getInteres(self):
        return self.interes
    def getEstadoDePago(self):
        return self.estadoDePago
    def getEntidad(self):
        return self.entidad
    def getTipoEntidad(self):
        return self.tipoEntidad
    def getCapitalPagado(self):
        return self.capitalPagado
    def getFechaCreacion(self):
        return self.fechaCreacion
    @classmethod
    def setListaDeudas(cls, listaDeudas):
        if listaDeudas is None:
            raise ValueError("La lista no puede ser nula")
        cls.listaDeudas = listaDeudas
    def setValorInicialDeuda(self, valorInicialDeuda):
        self.valorInicialDeuda = valorInicialDeuda
    def setInteres(self, interes):
        self.interes = interes
    def setEstadoDePago(self, estadoDePago):
        self.estadoDePago = estadoDePago
    def setEntidad(self, entidad):
        self.entidad = entidad
    def setCapitalPagado(self, capitalPagado):
        self.capitalPagado = capitalPagado
    def actualizarDeuda(self, fecha, montoDeuda, cuotas):
        deudaActual = self.deudaActual(fecha.getAno())
        self.valorInicialDeuda = montoDeuda + deudaActual
        self.capitalPagado = 0
        self.cuotas = cuotas

    @staticmethod
    def compararDeudas(fecha):
        from src.gestorAplicacion.bodega.proveedor import Proveedor
        mayorBanco = None
        mayorProveedor = None
        mayorPrecioB = 1
        mayorPrecioP = 1
        deudaP = None
        deudaB = None
        for deuda in Deuda.getListaDeudas():
            for proveedor in Proveedor.getListaProveedores():
                deudaA=Proveedor.getDeuda(proveedor)
                if deudaA is not None:
                    valdeudaP = Deuda.deudaActual(deudaA,fecha.getAno())
                    if valdeudaP != 0 and Deuda.getEstadoDePago(deudaA)!=True and valdeudaP > mayorPrecioP:
                        mayorPrecioP = valdeudaP
                        mayorProveedor = proveedor
                        deudaP = deudaA
                        
            for banco in Banco.getListaBancos():
                for deudaA in banco.getDeuda():
                    if deudaA is not None:
                        valdeudaB = Deuda.deudaActual(deudaA,fecha.getAno())
                        if valdeudaB != 0 and Deuda.getEstadoDePago(deudaA)!=True and valdeudaB > mayorPrecioB:
                            mayorPrecioB = valdeudaB
                            mayorBanco = banco
                            deudaB = deudaA
    
        pagoP = Deuda.pagarDeuda(deudaP,fecha)
        deudaP.capitalPagado += deudaP.deudaActual(fecha.getAno()) - pagoP
        pagoB = Deuda.pagarDeuda(deudaB,fecha)
        deudaB.capitalPagado += deudaB.deudaActual(fecha.getAno()) - pagoB
        
        return "Se pagaron las deudas con el Banco: "+str(mayorBanco.getNombreCuenta())+" y con el Proveedor: "+str(mayorProveedor.getNombre())

    def pagarDeuda(self, fecha):
        pagar = self.deudaActual(fecha.getAno())
        for banco in Banco.getListaBancos():
            while banco.getAhorroBanco() >= 3_000_000:
                if pagar > 0 and pagar - 500_000 >= 0:
                    banco.setAhorroBanco(banco.getAhorroBanco() - 500_000)
                    pagar -= 500_000
                elif pagar > 0:
                    banco.setAhorroBanco(banco.getAhorroBanco() - pagar)
                elif pagar == 0:
                    self.estadoDePago = True
                    break
        return pagar


