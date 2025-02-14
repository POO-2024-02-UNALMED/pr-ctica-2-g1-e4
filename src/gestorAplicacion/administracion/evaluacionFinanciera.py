# Equipo 4 grupo 1
# Clase Evaluacionfinanciera
# Representa una evaluacion financiera generada durante la funcionalidad
# de desglose economico

from typing import List
from src.gestorAplicacion.fecha import Fecha
from src.gestorAplicacion.sede import Sede
from src.gestorAplicacion.administracion.banco import Banco
from src.gestorAplicacion.administracion.empleado import Empleado
from src.gestorAplicacion.administracion.gastoMensual import GastoMensual
from src.gestorAplicacion.administracion.area import Area
from src.gestorAplicacion.administracion.rol import Rol

class EvaluacionFinanciera:
    def __init__(self, balance: float, presidente: Empleado = None):
        self.pagoPersonas = 0  # deudaBanco + deudaProveedores
        self.balance = balance
        self.proyeccion = False
        self.presidente = presidente
        
        if presidente and presidente.areaActual == Area.DIRECCION:
            self.presidente = presidente
            presidente.evaluaciones.append(self)

    def informe(self) -> str:
        return f"El monto del balance a cargo de: {self.presidente} fue de: ${self.balance} pesos"

    @staticmethod
    def estimadoVentasGastos(fechaActual: 'Fecha', porcentajeUsuario: float, balanceAnterior: 'EvaluacionFinanciera') -> int:
        montoVentasPasado = 0
        for sede in Sede.listaSedes:
            for venta in sede.historialVentas:
                if (fechaActual.compararAno(fechaActual.ano, venta.fechaVenta.ano) and 
                    fechaActual.compararMes(fechaActual.ano - 1, venta.fechaVenta.ano)):
                    montoVentasPasado += venta.subtotal + venta.costoEnvio
        
        # Predecimos las ventas con un porcentaje de fidelidad 
        porcentajeFidelidadOro = 0.8 if balanceAnterior.balance >= 0 else 0.5
        if porcentajeUsuario == 0.0:
            porcentajeFidelidadOro = 0.9
        
        porcentajeFidelidadPlata = porcentajeFidelidadOro - 0.2
        porcentajeFidelidadBronce = porcentajeFidelidadOro - 0.4
        porcentajeFidelidadNull = porcentajeUsuario
        
        prediccionVentas = montoVentasPasado * (porcentajeFidelidadOro + 
                                                porcentajeFidelidadPlata + 
                                                porcentajeFidelidadBronce + 
                                                porcentajeFidelidadNull)
        gastosMensuales = GastoMensual.gastosMensuales(fechaActual)
        diferenciaEstimada = round((prediccionVentas - gastosMensuales * 0.8) + (Banco.totalAhorros() * 0.05))
        return diferenciaEstimada

    def getPagoPersonas(self) -> int:
        return self.pagoPersonas

    def setPagoPersonas(self, pago: int) -> None:
        self.pagoPersonas = pago

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
        if presidente.areaActual == Area.DIRECCION and presidente.rol == Rol.PRESIDENTE:
            self.presidente = presidente

    @staticmethod
    def promedioBalance() -> float:
        promedio = 0
        for evaluacion in Sede.getEvaluacionesFinancieras():
            promedio += evaluacion.balance
        promedio /= len(Sede.getEvaluacionesFinancieras())
        return promedio