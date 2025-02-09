from enum import Enum

from src.gestorAplicacion.sede import Sede
from src.gestorAplicacion.venta import Venta

class Area(Enum):
    DIRECCION = ("Direccion", ["gerente","subgerente","director","subdirector"])
    OFICINA = ("Oficina", ["computador","registradora"])
    VENTAS = ("Ventas", ["escaner"])
    CORTE = ("Corte", ["maquina de coser","maquina de corte","plancha industrial"])

    def __init__(self, nombre, Maquinaria):
        self.nombre = nombre
        self.MaquinariaNecesaria = Maquinaria
        self.rendimiento_deseado = 0
    
    def rendimientoDeseadoActual(sede, fecha):
        rendimiento_sede = []
        for area in Area:
            if area == Area.DIRECCION:
                area.rendimiento_deseado = (3 / 5) * 100
            elif area == Area.OFICINA:
                cantidad_empleados_oficina = sede.cantidad_por_area(Area.OFICINA)
                area.rendimiento_deseado = len(Venta.filtrar(sede.getHistorialVentas(), fecha)) / cantidad_empleados_oficina
            elif area == Area.VENTAS:
                monto_total = 0
                for venta in Venta.filtrar(sede.getHistorialVentas(), fecha):
                    monto_pagado = venta.get_monto_pagado()
                    monto_total += monto_pagado
                cantidad_ventas = len(Venta.filtrar(sede.getHistorialVentas(), fecha))
                area.rendimiento_deseado = (monto_total / cantidad_ventas) * 0.8
            elif area == Area.CORTE:
                prendas_descartadas = 0
                prendas_producidas = 0

                for empleado in sede.get_lista_empleados():
                    prendas_descartadas += empleado.get_prendas_descartadas()
                    prendas_producidas += empleado.get_prendas_producidas()

                area.rendimiento_deseado = (prendas_producidas / (prendas_descartadas + prendas_producidas)) * 90

            rendimiento_sede.append(area.rendimiento_deseado)

        return rendimiento_sede