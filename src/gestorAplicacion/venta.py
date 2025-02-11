from src.gestorAplicacion.bodega import Bolsa, Prenda
from src.gestorAplicacion import Fecha, Sede, Persona
import math

class Venta:
    codigos_regalo = []
    montos_regalo = []
    pesimismo = 0.02

    def __init__(self, sede, fecha, cliente, asesor=None, encargado=None, articulos=None, subtotal=0, monto_pagado=0):
        self.sede = sede
        self.fecha_venta = fecha
        self.cliente = cliente
        self.asesor = asesor
        self.encargado = encargado
        self.articulos = articulos if articulos else []
        self.bolsas = []
        self.monto_pagado = monto_pagado
        self.subtotal = subtotal
        self.costo_envio = 0
        self.numero = 0
        if encargado:
            encargado.get_ventas_encargadas().append(self)
        if articulos:
            for prenda in articulos:
                sede.get_prendas_inventadas().remove(prenda)
        sede.actualizar_historial_ventas(self)
        if monto_pagado:
            sede.get_cuenta_sede().set_ahorro_banco(sede.get_cuenta_sede().get_ahorro_banco() + monto_pagado)

    @staticmethod
    def acumuladoVentasAsesoradas(empleado):
        acumulado = 0
        for venta in empleado.get_sede().get_historial_ventas():
            if venta.asesor == empleado:
                acumulado += venta.subtotal
        return acumulado

    @staticmethod
    def cantidadVentasEncargadasEnMes(empleado, fecha):
        cantidad = 0
        for venta in empleado.get_ventas_encargadas():
            if venta.get_fecha_venta().get_mes() == fecha.get_mes() and venta.get_fecha_venta().get_ano() == fecha.get_ano():
                cantidad += 1
        return cantidad

    @staticmethod
    def acumuladoVentasEmpleadoEncargado(empleado):
        acumulado = 0
        for venta in empleado.get_sede().get_historial_ventas():
            if venta.encargado == empleado:
                acumulado += venta.subtotal
        return acumulado

    @staticmethod
    def calcularBalanceVentaProduccion(fecha):
        valor_calculado = 0
        costos = 0
        for sede in Sede.get_lista_sedes():
            for venta in sede.get_historial_ventas():
                if Fecha.comparar_ano(venta.get_fecha_venta().get_ano(), fecha.get_ano()) and Fecha.comparar_mes(venta.get_fecha_venta().get_mes(), fecha.get_mes()):
                    monto = venta.monto_pagado
                    descuento = venta.cliente.get_membresia().get_porcentaje_descuento()
                    valor_calculado += round(monto + (monto * descuento) + venta.costo_envio)
                    for prenda in venta.articulos:
                        costos += prenda.calcular_costo_insumos()
        balance_costos_produccion = valor_calculado - costos
        return balance_costos_produccion

    @staticmethod
    def blackFriday(fecha):
        ano = fecha.get_ano() if fecha.get_mes() > 11 or (fecha.get_mes() == 11 and fecha.get_dia() >= 24) else fecha.get_ano() - 1
        dias_black_friday = [Fecha(28, 11, ano), Fecha(29, 11, ano), Fecha(30, 11, ano)]
        fechas_normales = [Fecha(23, 11, ano), Fecha(24, 11, ano), Fecha(25, 11, ano)]
        monto_ventas_bf = 0
        monto_ventas_comunes = 0
        for sede in Sede.get_lista_sedes():
            for venta in sede.get_historial_ventas():
                for i in range(3):
                    if dias_black_friday[i].get_ano() == venta.get_fecha_venta().get_ano() and dias_black_friday[i].get_mes() == venta.get_fecha_venta().get_mes() and dias_black_friday[i].get_dia() == venta.get_fecha_venta().get_dia():
                        monto_ventas_bf += venta.get_monto_pagado()
                    elif fechas_normales[i].get_ano() == venta.get_fecha_venta().get_ano() and fechas_normales[i].get_mes() == venta.get_fecha_venta().get_mes() and fechas_normales[i].get_dia() == venta.get_fecha_venta().get_dia():
                        monto_ventas_comunes += venta.get_monto_pagado()
        diferencia = (monto_ventas_bf - monto_ventas_comunes) / float(monto_ventas_comunes)
        return round(min(diferencia / 3, 0.31), 3)

    @staticmethod
    def filtrar_por_mes(ventas, fecha:Fecha):
        ventas_mes = []
        for venta in ventas:
            if venta.fecha_venta.año == fecha.año and venta.fecha_venta.mes == fecha.mes:
                ventas_mes.append(venta)
        return ventas_mes

    @staticmethod
    def filtrar_por_empleado(ventas, empleado):
        asesoradas = []
        for venta in ventas:
            if venta.asesor == empleado:
                asesoradas.append(venta)
        return asesoradas

    @staticmethod
    def cantidadProducto(ventas, prenda):
        cantidad = 0
        for venta in ventas:
            for articulo in venta.get_articulos():
                if articulo.get_nombre() == prenda:
                    cantidad += 1
        return cantidad

    @staticmethod
    def predecirVentas(fecha_actual, sede, prenda):
        ventas_mes1 = Venta.cantidadProducto(Venta.filtrar(sede.get_historial_ventas(), fecha_actual.restar_meses(3)), prenda)
        ventas_mes2 = Venta.cantidadProducto(Venta.filtrar(sede.get_historial_ventas(), fecha_actual.restar_meses(2)), prenda)
        pendiente_mes1a2 = ventas_mes2 - ventas_mes1

        ventas_mes3 = Venta.cantidadProducto(Venta.filtrar(sede.get_historial_ventas(), fecha_actual.restar_meses(1)), prenda)
        pendiente_mes2a3 = ventas_mes3 - ventas_mes2

        pendiente_promedio = (pendiente_mes1a2 + pendiente_mes2a3) / 2
        return math.ceil(ventas_mes3 + pendiente_promedio)

    @staticmethod
    def acumulado(ventas):
        acumulado = 0
        for venta in ventas:
            acumulado += venta.monto_pagado
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
        return self.fecha_venta

    def setFechaVenta(self, fecha):
        self.fecha_venta = fecha

    def getMontoPagado(self):
        return self.monto_pagado

    def setMontoPagado(self, monto):
        if self.monto_pagado == 0:
            self.sede.get_cuenta_sede().set_ahorro_banco(self.sede.get_cuenta_sede().get_ahorro_banco() + monto)
            self.monto_pagado = monto
        else:
            self.sede.get_cuenta_sede().set_ahorro_banco(self.sede.get_cuenta_sede().get_ahorro_banco() - self.monto_pagado)
            self.monto_pagado = monto
            self.sede.get_cuenta_sede().set_ahorro_banco(self.sede.get_cuenta_sede().get_ahorro_banco() - monto)

    def getCliente(self):
        return self.cliente

    def setCliente(self, persona):
        self.cliente = persona

    def getNumero(self):
        return self.numero

    def setNumero(self, numero):
        self.numero = numero

    def getCostoEnvio(self):
        return self.costo_envio

    def setCostoEnvio(self, monto):
        self.costo_envio = monto

    def getsubtotal(self):
        return self.subtotal

    def setsubtotal(self, monto):
        self.subtotal = monto

    @staticmethod
    def setPesimismo(new_pesimism):
        Venta.pesimismo = new_pesimism

    @staticmethod
    def getPesimismo():
        return Venta.pesimismo

    @staticmethod
    def getCodigosRegalo():
        return Venta.codigos_regalo

    @staticmethod
    def setCodigosRegalo(codigo):
        Venta.codigos_regalo = codigo

    @staticmethod
    def getMontosRegalo():
        return Venta.montos_regalo

    @staticmethod
    def setMontosRegalo(montos):
        Venta.montos_regalo = montos
