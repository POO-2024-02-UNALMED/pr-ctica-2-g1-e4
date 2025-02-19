from src.gestorAplicacion.fecha import Fecha
import math
from multimethod import multimethod
from typing import List
 

# Puede que visual marque esto. Usa pip install multimethod en la terminal para arreglarlo.

class Venta:
    codigosRegalo = []; montosRegalo = []
    pesimismo = 0.02

    def __init__(self, sede, fecha:Fecha, cliente=None, asesor=None, encargado=None, articulos=None, subtotal=0, montoPagado=0):
        self.sede = sede
        self.fechaVenta = fecha
        self.cliente = cliente
        self.asesor = asesor
        self.encargado = encargado
        if articulos is not None:
            self.articulos = articulos
        self.bolsas = []
        self.montoPagado = montoPagado
        self.subtotal = subtotal
        self.costoEnvio = 0
        self.numero = 0
        if encargado:
            encargado.getVentasEncargadas().append(self)
        if articulos is not None:
            for prenda in articulos:
                if prenda in sede.getPrendasInventadas():
                    sede.getPrendasInventadas().remove(prenda)
        sede.actualizarHistorialVentas(self)
        if montoPagado:
            sede.getCuentaSede().setAhorroBanco(sede.getCuentaSede().getAhorroBanco() + montoPagado)
        sede.actualizarHistorialVentas(self)

    @staticmethod
    def acumuladoVentasAsesoradas(empleado):
        acumulado = 0
        for venta in empleado.getSede().getHistorialVentas():
            if venta.asesor == empleado:
                acumulado += venta.subtotal
        return acumulado

    @staticmethod
    def cantidadVentasEncargadasEnMes(empleado, fecha):
        cantidad = 0
        for venta in empleado.getVentasEncargadas():
            if venta.getFechaVenta().getMes() == fecha.getMes() and venta.getFechaVenta().getAno() == fecha.getAno():
                cantidad += 1
        return cantidad

    @staticmethod
    def acumuladoVentasEmpleadoEncargado(empleado):
        acumulado = 0
        for venta in empleado.getSede().getHistorialVentas():
            if venta.encargado == empleado:
                acumulado += venta.subtotal
        return acumulado

    @staticmethod
    def calcularBalanceVentaProduccion(fecha):
        from src.gestorAplicacion.sede import Sede
        valorCalculado = 0
        costos = 0
        for sede in Sede.getListaSedes():
            for venta in sede.getHistorialVentas():
                if Fecha.compararAno(venta.getFechaVenta().getAno(), fecha.getAno()) and Fecha.compararMes(venta.getFechaVenta().getMes(), fecha.getMes()):
                    monto = venta.montoPagado
                    descuento = venta.cliente.getMembresia().getPorcentajeDescuento()
                    valorCalculado += round(monto + (monto * descuento) + venta.costoEnvio)
                    for prenda in venta.articulos:
                        costos += prenda.calcularCostoInsumos()
        balanceCostosProduccion = valorCalculado - costos
        return balanceCostosProduccion

    @staticmethod
    def blackFriday(fecha):
        from src.gestorAplicacion.sede import Sede
        ano = fecha.getAno() if fecha.getMes() > 11 or (fecha.getMes() == 11 and fecha.getDia() >= 24) else fecha.getAno() - 1
        diasBlackFriday = [Fecha(28, 11, ano), Fecha(29, 11, ano), Fecha(30, 11, ano)]
        fechasNormales = [Fecha(23, 11, ano), Fecha(24, 11, ano), Fecha(25, 11, ano)]
        montoVentasBF = 0
        montoVentasComunes = 0
        for sede in Sede.getListaSedes():
            for venta in sede.getHistorialVentas():
                for i in range(3):
                    if diasBlackFriday[i].getAno() == venta.getFechaVenta().getAno() and diasBlackFriday[i].getMes() == venta.getFechaVenta().getMes() and diasBlackFriday[i].getDia() == venta.getFechaVenta().getDia():
                        montoVentasBF += venta.getMontoPagado()
                    elif fechasNormales[i].getAno() == venta.getFechaVenta().getAno() and fechasNormales[i].getMes() == venta.getFechaVenta().getMes() and fechasNormales[i].getDia() == venta.getFechaVenta().getDia():
                        montoVentasComunes += venta.getMontoPagado()
        diferencia = (montoVentasBF - montoVentasComunes) / float(montoVentasComunes)
        return round(min(diferencia / 3, 0.31), 3)

    @multimethod
    def filtrar(cls,ventas:List, fecha:Fecha):
        ventasMes = []
        for venta in ventas:
            if venta.fechaVenta.ano == fecha.ano and venta.fechaVenta.mes == fecha.mes:
                ventasMes.append(venta)
        return ventasMes
    from src.gestorAplicacion.administracion.empleado import Empleado

    @multimethod
    def filtrar(cls,ventas:List, empleado:Empleado):
        asesoradas = []
        for venta in ventas:
            if venta.asesor == empleado:
                asesoradas.append(venta)
        return asesoradas
    filtrar =classmethod(filtrar)

    @staticmethod
    def cantidadProducto(ventas, prenda):
        cantidad = 0
        for venta in ventas:
            for articulo in venta.getArticulos():
                if articulo.getNombre() == prenda:
                    cantidad += 1
        return cantidad

    @staticmethod
    def predecirVentas(fechaActual, sede, prenda):
        from src.gestorAplicacion.sede import Sede
        ventasMes1 = Venta.cantidadProducto(Venta.filtrar(Sede.getHistorialVentas(sede), Fecha.restarMeses(fechaActual, 3)), prenda)
        ventasMes2 = Venta.cantidadProducto(Venta.filtrar(Sede.getHistorialVentas(sede), Fecha.restarMeses(fechaActual, 2)), prenda)
        pendienteMes1a2 = ventasMes2 - ventasMes1
        ventasMes3 = Venta.cantidadProducto(Venta.filtrar(Sede.getHistorialVentas(sede), Fecha.restarMeses(fechaActual, 1)), prenda)
        pendienteMes2a3 = ventasMes3 - ventasMes2
        pendientePromedio = (pendienteMes1a2 + pendienteMes2a3) / 2
        return math.ceil(ventasMes3 + pendientePromedio)
    
    @staticmethod
    def acumulado(ventas):
        acumulado = 0
        for venta in ventas:
            acumulado += Venta.getMontoPagado(venta)
        return acumulado
    def getArticulos(self):
        return self.articulos
    def setArticulos(self, articulos):
        self.articulos = articulos
    def getBolsas(self):
        return self.bolsas
    def setBolsas(self, bolsas):
        self.bolsas = bolsas
    def getEncargado(self):
        return self.encargado
    def setEncargado(self, emp):
        self.encargado = emp
    def getAsesor(self):
        return self.asesor
    def setAsesor(self, emp):
        self.asesor = emp
    def getSede(self):
        return self.sede
    def setSede(self, sede):
        self.sede = sede
    def getFechaVenta(self):
        return self.fechaVenta
    def setFechaVenta(self, fecha):
        self.fechaVenta = fecha
    def getMontoPagado(self):
        return self.montoPagado
    def setMontoPagado(self, monto):
        if self.montoPagado == 0:
            self.Sede.getCuentaSede().setAhorroBanco(self.sede.getCuentaSede().getAhorroBanco() + monto)
            self.montoPagado = monto
        else:
            self.sede.getCuentaSede().setAhorroBanco(self.sede.getCuentaSede().getAhorroBanco() - self.montoPagado)
            self.montoPagado = monto
            self.sede.getCuentaSede().setAhorroBanco(self.sede.getCuentaSede().getAhorroBanco() - monto)
    def getCliente(self):
        return self.cliente
    def setCliente(self, persona):
        self.cliente = persona
    def getNumero(self):
        return self.numero
    def setNumero(self, numero):
        self.numero = numero
    def getCostoEnvio(self):
        return self.costoEnvio
    def setCostoEnvio(self, monto):
        self.costoEnvio = monto
    def getSubtotal(self):
        return self.subtotal
    def setSubtotal(self, monto):
        self.subtotal = monto
    @staticmethod
    def setPesimismo(newPesimismo):
        Venta.pesimismo = newPesimismo
    @staticmethod
    def getPesimismo():
        return Venta.pesimismo
    @staticmethod
    def getCodigosRegalo():
        return Venta.codigosRegalo
    @staticmethod
    def setCodigosRegalo(codigo):
        Venta.codigosRegalo = codigo
    @staticmethod
    def getMontosRegalo():
        return Venta.montosRegalo
    @staticmethod
    def setMontosRegalo(montos):
        Venta.montosRegalo = montos
