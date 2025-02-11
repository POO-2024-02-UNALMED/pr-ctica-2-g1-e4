from abc import abstractmethod


class GastoMensual:
    
    @abstractmethod
    def calcularGastoMensual(self):
        pass

    def gastoMensualTipo(self, fecha, fecha_objeto, objeto):
        gasto_actual = 0
        gasto_pasado = 0
        gasto_total = [0, 0]
        
        if fecha_objeto.get_año() == fecha.get_año():
            if fecha_objeto.get_mes() == fecha.get_mes():
                gasto_actual += objeto.calcular_gasto_mensual()
                gasto_total[0] = gasto_actual
            if fecha_objeto.get_mes() == fecha.get_mes() - 1:
                gasto_pasado += objeto.calcular_gasto_mensual()
                gasto_total[1] = gasto_pasado
        
        return gasto_total

    @staticmethod
    def gastosMensuales(fecha):
        from src.gestorAplicacion.administracion.empleado import Empleado
        from src.gestorAplicacion.bodega.insumo import Insumo
        from src.gestorAplicacion.bodega.maquinaria import Maquinaria
        gastos_maquinaria = Maquinaria.gastoMensualClase(fecha)
        gastos_nomina = Empleado.gasto_mensual_clase()
        gasto_bolsa = Insumo.gastoMensualClase(fecha)
        suma = gastos_maquinaria + gastos_nomina + gasto_bolsa
        return suma