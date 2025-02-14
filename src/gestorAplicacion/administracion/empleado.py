from src.gestorAplicacion.administracion.banco import Banco
from src.gestorAplicacion.administracion.gastoMensual import GastoMensual
from src.gestorAplicacion.administracion.rol import Rol
from src.gestorAplicacion.bodega.maquinaria import Maquinaria
from src.gestorAplicacion.membresia import Membresia
from src.gestorAplicacion.persona import Persona
from ..fecha import Fecha
from ..sede import Sede
from ..venta import Venta
from .area import Area
from typing import List

class Empleado(Persona,GastoMensual):
    def __init__(self, area_actual:Area, fecha: Fecha, sede: Sede, nombre: str, documento:int, rol: Rol, experiencia: int, membresia: Membresia, maquinaria: Maquinaria):
        super().__init__(nombre,  documento, rol, experiencia, True, membresia)
        self.area_actual = area_actual
        self.traslados = None
        self.areas = None
        self.sede = sede
        self.maquinaria = maquinaria
        self.fecha_contratacion = fecha
        def modificarBonificacion(self, bonificacion):
            self.bonificacion += bonificacion
            
        self.prendas_descartadas=0
        self.prendas_producidas=0
        self.pericia=0
        self.bonificacion = 0
        self.evaluaciones=[]
        self.ventas_encargadas=[]


    def calcularRendimiento(self, fecha: Fecha) -> float:
        rendimiento = 0
        match self.area_actual:
            case Area.CORTE:
                if self.prendas_descartadas == 0:
                    rendimiento = 100
                else:
                    rendimiento = (self.prendas_producidas / self.prendas_descartadas) * 100
            case Area.VENTAS:
                ventas_asesoradas = Venta.filtrar_por_mes(Venta.filtrar_por_empleado(self.sede.historial_ventas, self),fecha)
                if ventas_asesoradas:
                    rendimiento = Venta.acumulado(ventas_asesoradas) / len(ventas_asesoradas)
                else:
                    rendimiento = 0
            case Area.OFICINA:
                acumulado_ventas_sede = sum(venta.valor for venta in self.sede.historial_ventas if venta.fecha <= fecha)
                promedio_ventas_sede = acumulado_ventas_sede / self.sede.cantidad_por_area('Oficina')
                ventas_encargadas = sum(venta.valor for venta in self.ventas_encargadas if venta.fecha <= fecha)
                rendimiento = (ventas_encargadas / promedio_ventas_sede) * 100
            case Area.DIRECCION:

                balances_positivos = sum(1.0 for evaluacion in self.evaluaciones if evaluacion.balance > 0)
                balances_negativos = sum(1.0 for evaluacion in self.evaluaciones if evaluacion.balance <= 0)
                if balances_negativos + balances_positivos == 0:
                    rendimiento = 100
                else:
                    rendimiento = (balances_positivos / (balances_negativos + balances_positivos)) * 100
        
        return rendimiento

    # Parte de la interacción 1 de gestion humana
    @classmethod
    def listaInicialDespedirEmpleado(cls, fecha: Fecha) -> List[List]:
        lista_a_despedir = []
        mensajes = []
        retorno = [lista_a_despedir, mensajes]
        lista_a_transferir = [[] for _ in sede.get_lista_sedes()]

        for sede in Sede.get_lista_sedes():
            for emp in sede.get_lista_empleados():
                rendimiento = emp.calcular_rendimiento(Fecha)
                se_va_a_despedir = False

                rendimiento_deseado = emp.sede.get_rendimiento_deseado(emp.area_actual, Fecha)
                if rendimiento < rendimiento_deseado:
                    se_va_a_despedir = True
                    lista_a_despedir.append(emp)
                    mensajes.append(f"El empleado {emp.nombre} tiene un rendimiento insuficiente, con un rendimiento de {rendimiento:.2f} y un rendimiento deseado de {rendimiento_deseado:.2f}")

                if se_va_a_despedir and sede.cantidad_por_area(emp.area_actual) == 1:
                    for idx_sede, sede_destino in enumerate(sede.get_lista_sedes()):
                        if sede_destino.get_rendimiento_deseado(emp.area_actual, Fecha) <= rendimiento + 20 and se_va_a_despedir:
                            mensajes.append(f"El empleado {emp.nombre} ha sido transferido a la sede {sede_destino.nombre}")
                            lista_a_despedir.remove(emp)
                            lista_a_transferir[idx_sede].append(emp)
                            se_va_a_despedir = False

                if se_va_a_despedir and emp.area_actual != Area.CORTE and emp.traslados < 2 and sede.cantidad_por_area(emp.area_actual) != 1:
                    puede_cambiar_area = True
                    for area_pasada in emp.areas:
                        if area_pasada > emp.area_actual:
                            puede_cambiar_area = False
                            break
                    if puede_cambiar_area and emp.areaActual:
                        emp.area_actual = emp.areas[emp.areas.index(emp.area_actual) -1]
                        emp.traslados += 1
                        se_va_a_despedir = False
                        lista_a_despedir.remove(emp)

        for idx_sede, sede in enumerate(Sede.get_lista_sedes()):
            for emp in lista_a_transferir[idx_sede]:
                mensajes += emp.transferir(sede)
                

        return retorno
    
    def trasladarEmpleado(self, sede_nueva) -> List[str]:
        from src.gestorAplicacion.bodega.maquinaria import Maquinaria
        mensajes = []
        a_pagar = Maquinaria.remuneracionDanos(self)
        if Banco.get_cuenta_principal() is not None:
            Banco.get_cuenta_principal().transaccion(a_pagar)
        else:
            mensajes.append("Perdonenos pero disculpenos: No se ha podido recibir la remuneración de daños, no hay cuenta principal, sugerimos añadir una.")
        self.modificarBonificacion(a_pagar * -1)
        Maquinaria.liberarMaquinariaDe(self)

        self.traslados += 1
        self.setSede(sede_nueva)

        Maquinaria.asignarMaquinaria(self)
        return mensajes

    def __str__(self):
        return f"{super().__str__()}\nArea: {self.area_actual} - Sede: {self.sede} - Traslados: {self.traslados}"

    def modificarBonificacion(self, bonificacion):
        self.bonificacion += bonificacion

    def getTraslados(self):
        return self.traslados

    def setTraslados(self, traslados):
        self.traslados = traslados

    def getPrendasDescartadas(self):
        return self.prendas_descartadas

    def setPrendasDescartadas(self, prendas):
        self.prendas_descartadas = prendas

    def getPrendasProducidas(self):
        return self.prendas_producidas

    def setPrendasProducidas(self, prendas_producidas):
        self.prendas_producidas = prendas_producidas

    def getPericia(self):
        return self.pericia

    def setPericia(self, pericia):
        self.pericia = pericia

    def getAreaActual(self):
        return self.area_actual

    def setAreaActual(self, area):
        self.area_actual = area

    def getFechaContratacion(self):
        return self.fecha_contratacion

    def setFechaContratacion(self, fecha):
        self.fecha_contratacion = fecha

    def getSede(self):
        return self.sede

    def setSede(self, sede):
        if self.sede is not None:
            self.sede.quitar_empleado(self)
        self.sede = sede
        self.sede.anadir_empleado(self)

    def getMaquinaria(self):
        return self.maquinaria

    def setMaquinaria(self, maquinaria):
        self.maquinaria = maquinaria

    def getAreas(self):
        return self.areas

    def setAreas(self, areas):
        self.areas = areas

    def getBonificacion(self):
        return self.bonificacion

    def setRendimientoBonificacion(self, boni):
        self.bonificacion = boni

    def setSalario(self, salario):
        self.salario = salario

    def setEvaluacionesFinancieras(self, evaluaciones):
        self.evaluaciones = evaluaciones

    def getEvaluacionesFinancieras(self):
        return self.evaluaciones

    def getVentasEncargadas(self):
        return self.ventas_encargadas

    @staticmethod
    def get_emp_creados():
        return Sede.getListaEmpleadosTotal()