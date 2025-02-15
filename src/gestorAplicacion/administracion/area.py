from enum import Enum

from src.gestorAplicacion.sede import Sede
from src.gestorAplicacion.fecha import Fecha

class Area(Enum):
    DIRECCION = ("Direccion", ["gerente", "subgerente", "director", "subdirector"])
    OFICINA = ("Oficina", ["computador", "registradora"])
    VENTAS = ("Ventas", ["escaner"])
    CORTE = ("Corte", ["maquina de coser", "maquina de corte", "plancha industrial"])

    def __init__(self, nombre, maquinaria):
        self.nombre = nombre
        self.maquinariaNecesaria = maquinaria
        self.rendimientoDeseado = 0
    
    def rendimientoDeseadoActual(sede:Sede, fecha:Fecha):
        from src.gestorAplicacion.venta import Venta
        rendimientoSede = []
        for area in Area:
            if area == Area.DIRECCION:
                area.rendimientoDeseado = (3 / 5) * 100
            elif area == Area.OFICINA:
                cantidadEmpleadosOficina = sede.cantidadPorArea(Area.OFICINA)
                area.rendimientoDeseado = len(Venta.filtrar(sede.getHistorialVentas(), fecha)) / cantidadEmpleadosOficina
            elif area == Area.VENTAS:
                montoTotal = 0
                for venta in Venta.filtrar(sede.getHistorialVentas(), fecha):
                    montoPagado = venta.getMontoPagado()
                    montoTotal += montoPagado
                cantidadVentas = len(Venta.filtrar(sede.getHistorialVentas(), fecha))
                area.rendimientoDeseado = (montoTotal / cantidadVentas) * 0.8
            elif area == Area.CORTE:
                prendasDescartadas = 0
                prendasProducidas = 0

                for empleado in sede.getListaEmpleados():
                    prendasDescartadas += empleado.getPrendasDescartadas()
                    prendasProducidas += empleado.getPrendasProducidas()

                area.rendimientoDeseado = (prendasProducidas / (prendasDescartadas + prendasProducidas)) * 90

            rendimientoSede.append(area.rendimientoDeseado)

        return rendimientoSede