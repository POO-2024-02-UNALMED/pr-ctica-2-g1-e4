from enum import Enum

from src.gestorAplicacion.sede import Sede
from src.gestorAplicacion.fecha import Fecha

class Area(Enum):
    DIRECCION = ("Direccion", ["Computador","Impresora"],3); 
    OFICINA = ("Oficina", ["Computador", "Caja Registradora"],2);
    VENTAS = ("Ventas", ["escaner"],1); 
    CORTE = ("Corte", ["Maquina de Coser Industrial", "Maquina de Corte", "Plancha Industrial"],0)

    def __init__(self, nombre, maquinaria, jerarquia):
        self.nombre = nombre
        self.maquinariaNecesaria = maquinaria
        self.rendimientoDeseado = 0
        self.jerarquia = jerarquia
    
    def rendimientoDeseadoActual(sede:Sede, fecha:Fecha):
        from src.gestorAplicacion.venta import Venta
        rendimientoSede = []
        for area in Area:
            if area == Area.DIRECCION:
                area.rendimientoDeseado = (3 / 5) * 100
            elif area == Area.OFICINA:
                cantidadEmpleadosOficina = sede.cantidadPorArea(Area.OFICINA)
                if cantidadEmpleadosOficina!=0:
                    area.rendimientoDeseado = len(Venta.filtrar(sede.getHistorialVentas(), fecha)) / cantidadEmpleadosOficina
                else:
                    area.rendimientoDeseado = 0
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
    
    @classmethod
    def obtenerPorJerarquia(cls, jerarquia):
        for area in Area:
            if area.jerarquia == jerarquia:
                return area

    def getMaquinariaNecesaria(self):
        return self.maquinariaNecesaria