# Equipo 4 grupo 1
# Clase Evaluacionfinanciera
# Representa una evaluacion financiera generada durante la funcionalidad
# de desglose economico

from typing import List
from src.gestorAplicacion.fecha import Fecha
from src.gestorAplicacion.sede import Sede;
from src.gestorAplicacion.administracion.banco import Banco
from src.gestorAplicacion.administracion.empleado import Empleado
from src.gestorAplicacion.administracion.gastoMensual import GastoMensual
from src.gestorAplicacion.administracion.area import Area
from src.gestorAplicacion.administracion.rol import Rol

class EvaluacionFinanciera:
    def __init__(self, balance: float, presidente: Empleado = None):
        self.pago_personas = 0  # deudaBanco + deudaProveedores
        self.balance = balance
        self.proyeccion = False
        self.presidente = presidente
        
        if presidente and presidente.area_actual == Area.DIRECCION:
            self.presidente = presidente
            presidente.evaluaciones.append(self)

    def informe(self) -> str:
        return f"El monto del balance a cargo de: {self.presidente} fue de: ${self.balance} pesos"

    @staticmethod
    def estimadoVentasGastos(fecha_actual: 'Fecha', porcentaje_usuario: float, balance_anterior: 'EvaluacionFinanciera') -> int:
        monto_ventas_pasado = 0
        for sede in Sede.lista_sedes:
            for venta in sede.historial_ventas:
                if (fecha_actual.comparar_año(fecha_actual.año, venta.fecha_venta.año) and 
                    fecha_actual.comparar_mes(fecha_actual.año - 1, venta.fecha_venta.año)):
                    monto_ventas_pasado += venta.subtotal + venta.costo_envio
        
        # Predecimos las ventas con un porcentaje de fidelidad 
        porcentaje_fidelidad_oro = 0.8 if balance_anterior.balance >= 0 else 0.5
        if porcentaje_usuario == 0.0:
            porcentaje_fidelidad_oro = 0.9
        
        porcentaje_fidelidad_plata = porcentaje_fidelidad_oro - 0.2
        porcentaje_fidelidad_bronce = porcentaje_fidelidad_oro - 0.4
        porcentaje_fidelidad_null = porcentaje_usuario
        
        prediccion_ventas = monto_ventas_pasado * (porcentaje_fidelidad_oro + 
                                                    porcentaje_fidelidad_plata + 
                                                    porcentaje_fidelidad_bronce + 
                                                    porcentaje_fidelidad_null)
        gastos_mensuales = GastoMensual.gastosMensuales(fecha_actual)
        diferencia_estimada = round((prediccion_ventas - gastos_mensuales * 0.8) + (Banco.total_ahorros() * 0.05))
        return diferencia_estimada

    def getPagoPersonas(self) -> int:
        return self.pago_personas

    def setPagoPersonas(self, pago: int) -> None:
        self.pago_personas = pago

    def getBalance(self) -> float:
        return self.balance

    def setBalance(self, balance: float) -> None:
        self.balance = balance

    def getProyeccion(self) -> bool:
        return self.proyeccion

    def setProyeccion(self, proyeccion: bool) -> None:
        self.proyeccion = proyeccion

    def getPresidente(self) -> Empleado:
        return self.presidente

    def setPresidente(self, presidente: Empleado) -> None:
        if presidente.area_actual == Area.DIRECCION and presidente.rol == Rol.PRESIDENTE:
            self.presidente = presidente

    @staticmethod
    def promedioBalance() -> float:
        promedio = 0
        for evaluacion in Sede.get_evaluaciones_financieras():
            promedio += evaluacion.balance
        promedio /= len(Sede.get_evaluaciones_financieras())
        return promedio