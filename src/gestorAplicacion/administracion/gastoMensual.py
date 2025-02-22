from abc import ABC, abstractmethod


class GastoMensual(ABC):
    
    @abstractmethod
    def calcularGastoMensual(self):
        pass
    def gastoMensualTipo(self, fecha, fechaObjeto, objeto):
        gastoActual = 0
        gastoPasado = 0
        gastoTotal = [0, 0]
        if fechaObjeto.getAno() == fecha.getAno():
            if fechaObjeto.getMes() == fecha.getMes():
                gastoActual += objeto.calcularGastoMensual()
                gastoTotal[0] = gastoActual
            if fechaObjeto.getMes() == fecha.getMes() - 1:
                gastoPasado += objeto.calcularGastoMensual()
                gastoTotal[1] = gastoPasado
        return gastoTotal

    @staticmethod
    def gastosMensuales(fecha):
        from src.gestorAplicacion.administracion.empleado import Empleado
        from src.gestorAplicacion.bodega.insumo import Insumo
        from src.gestorAplicacion.bodega.maquinaria import Maquinaria
        gastosMaquinaria = Maquinaria.gastoMensualClase(fecha)
        gastosNomina = Empleado.gastoMensualClase()
        gastoBolsa = Insumo.gastoMensualClase(fecha)
        suma = gastosMaquinaria + gastosNomina + gastoBolsa
        return suma