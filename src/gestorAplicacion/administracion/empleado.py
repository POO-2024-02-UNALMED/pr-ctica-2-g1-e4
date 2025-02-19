from src.gestorAplicacion.administracion.banco import Banco
from src.gestorAplicacion.administracion.gastoMensual import GastoMensual
from src.gestorAplicacion.administracion.rol import Rol
from src.gestorAplicacion.bodega.maquinaria import Maquinaria
from src.gestorAplicacion.membresia import Membresia
from src.gestorAplicacion.persona import Persona
from ..fecha import Fecha
from ..sede import Sede
from .area import Area
from typing import List
from typing_extensions import override 

class Empleado(Persona, GastoMensual):
    def __init__(self, areaActual: Area, fecha: Fecha, sede: Sede, nombre: str, documento: int, rol: Rol, experiencia: int, membresia: Membresia=Membresia.NULA, maquinaria: Maquinaria=[]):
        super().__init__(nombre, documento, rol, experiencia, True, membresia)
        self.areaActual = areaActual
        self.traslados = 0
        self.areas = [] # Areas por las que ha pasado
        self.sede = sede
        self.maquinaria = maquinaria
        self.fechaContratacion = fecha
        self.prendasDescartadas = 0
        self.prendasProducidas = 0
        self.pericia = 0
        self.bonificacion = 0
        self.evaluaciones = []; self.ventasEncargadas = []
        sede.anadirEmpleado(self)
        Sede.getListaEmpleadosTotal().append(self)

    @override
    def calcularGastoMensual(self):
        gasto=super().calcularSalario()
        return gasto
    

    def gastoMensualClase():
        gasto=0
        for emp in Sede.getListaEmpleadosTotal():
            gasto+=emp.calcularGastoMensual()
        return gasto
    
    def calcularRendimiento(self, fecha: Fecha) -> float:
        from ..venta import Venta
        rendimiento = 0
        match self.areaActual:
            case Area.CORTE:
                if self.prendasDescartadas == 0:
                    rendimiento = 100
                else:
                    rendimiento = (self.prendasProducidas / self.prendasDescartadas) * 100
            case Area.VENTAS:
                ventasAsesoradas = Venta.filtrar(Venta.filtrar(self.sede.historialVentas,self), fecha)
                if ventasAsesoradas:
                    rendimiento = Venta.acumulado(ventasAsesoradas) / len(ventasAsesoradas)
                else:
                    rendimiento = 0
            case Area.OFICINA:
                acumuladoVentasSede = len(Venta.filtrar(self.sede.historialVentas, fecha))
                promedioVentasSede = acumuladoVentasSede / self.sede.cantidadPorArea(Area.OFICINA)
                ventasEncargadas = Venta.cantidadVentasEncargadasEnMes(self, fecha)
                rendimiento = (ventasEncargadas / promedioVentasSede) * 100
            case Area.DIRECCION:
                balancesPositivos = sum(1.0 for evaluacion in self.evaluaciones if evaluacion.balance > 0)
                balancesNegativos = sum(1.0 for evaluacion in self.evaluaciones if evaluacion.balance <= 0)
                if balancesNegativos + balancesPositivos == 0:
                    rendimiento = 100
                else:
                    rendimiento = (balancesPositivos / (balancesNegativos + balancesPositivos)) * 100
        return rendimiento

    # Parte de la interacción 1 de gestion humana
    @classmethod
    def listaInicialDespedirEmpleado(cls, fecha: Fecha) -> List[List]:
        listaADespedir = [];empleadosInsuficientes = [];rendimientoInsufuciencias= [];acciones = []
        mensajes = [] # Heredado de la versión de java, usada para reportar a la funcion que la llama de errores o del proceso en general.
        retorno = [listaADespedir, mensajes, empleadosInsuficientes, rendimientoInsufuciencias, acciones]
        listaATransferir = [[] for _ in Sede.getListaSedes()]

        for sede in Sede.getListaSedes():
            for emp in sede.getListaEmpleados():
                rendimiento = emp.calcularRendimiento(fecha)
                seVaADespedir = False
                rendimientoDeseado = emp.sede.getRendimientoDeseado(emp.areaActual, fecha)
                if rendimiento < rendimientoDeseado:
                    seVaADespedir = True
                    listaADespedir.append(emp)
                    mensajes.append(f"El empleado {emp.nombre} tiene un rendimiento insuficiente, con un rendimiento de {rendimiento:.2f} y un rendimiento deseado de {rendimientoDeseado:.2f}")
                    empleadosInsuficientes.append(emp)
                    rendimientoInsufuciencias.append(rendimiento)
                if seVaADespedir and sede.cantidadPorArea(emp.areaActual) == 1:
                    for idxSede, sedeDestino in enumerate(Sede.getListaSedes()):
                        if sedeDestino.getRendimientoDeseado(emp.areaActual, fecha) <= rendimiento + 20 and seVaADespedir:
                            mensajes.append(f"El empleado {emp.nombre} ha sido transferido a la sede {sedeDestino.nombre}")
                            listaADespedir.remove(emp)
                            listaATransferir[idxSede].append(emp)
                            seVaADespedir = False
                            acciones.append("transferencia-sede")
                if seVaADespedir and emp.areaActual != Area.CORTE and emp.traslados < 2 and sede.cantidadPorArea(emp.areaActual) != 1:
                    puedeCambiarArea = True
                    for areaPasada in emp.areas:
                        if areaPasada > emp.areaActual:
                            puedeCambiarArea = False
                            break
                    if puedeCambiarArea and emp.areaActual.jerarquia>0:
                        emp.areaActual = Area.obtenerPorJerarquia(emp.areaActual.jerarquia - 1)
                        emp.traslados += 1
                        seVaADespedir = False
                        listaADespedir.remove(emp)
                        acciones.append("traslado-area")
                if seVaADespedir:
                    acciones.append("sugerencia-despido")
        for idxSede, sede in enumerate(Sede.getListaSedes()):
            for emp in listaATransferir[idxSede]:
                mensajes += emp.trasladarEmpleado(sede)

        return retorno

    def trasladarEmpleado(self, sedeNueva) -> List[str]:
        from src.gestorAplicacion.bodega.maquinaria import Maquinaria
        mensajes = []
        aPagar = Maquinaria.remuneracionDanos(self)
        if Banco.getCuentaPrincipal() is not None:
            Banco.getCuentaPrincipal().transaccion(aPagar)
        else:
            mensajes.append("Perdonenos pero disculpenos: No se ha podido recibir la remuneración de daños, no hay cuenta principal, sugerimos añadir una.")
        self.modificarBonificacion(aPagar * -1)
        Maquinaria.liberarMaquinariaDe(self)
        self.traslados += 1
        self.setSede(sedeNueva)
        Maquinaria.asignarMaquinaria(self)
        return mensajes
    
    @classmethod
    def despedirEmpleados(cls, empleados:List, conTransaccciones:bool, fecha:Fecha):
        for empleado in empleados:
            empleado.sede.quitarEmpleado(empleado)
            Sede.getListaEmpleadosTotal().remove(empleado)
            if conTransaccciones:
                aPagar:int = Maquinaria.remuneracionDanos(empleado)
                cesantias:int = empleado.salario*(empleado.fechaContratacion.getAno()-fecha.getAno())/360
                Banco.getCuentaPrincipal().transaccion(aPagar-cesantias)
            Maquinaria.liberarMaquinariaDe(empleado)

    def __str__(self):
        return f"{super().__str__()}\nArea: {self.areaActual} - Sede: {self.sede} - Traslados: {self.traslados}"
    def modificarBonificacion(self, bonificacion):
        self.bonificacion += bonificacion
    def getTraslados(self):
        return self.traslados
    def setTraslados(self, traslados):
        self.traslados = traslados
    def getPrendasDescartadas(self):
        return self.prendasDescartadas
    def setPrendasDescartadas(self, prendas):
        self.prendasDescartadas = prendas
    def getPrendasProducidas(self):
        return self.prendasProducidas
    def setPrendasProducidas(self, prendasProducidas):
        self.prendasProducidas = prendasProducidas
    def getPericia(self):
        return self.pericia
    def setPericia(self, pericia):
        self.pericia = pericia
    def getAreaActual(self):
        return self.areaActual
    def setAreaActual(self, area):
        self.areaActual = area
    def getFechaContratacion(self):
        return self.fechaContratacion
    def setFechaContratacion(self, fecha):
        self.fechaContratacion = fecha
    def getSede(self):
        return self.sede
    def setSede(self, sede):
        if self.sede is not None:
            self.sede.quitarEmpleado(self)
        self.sede = sede
        self.sede.anadirEmpleado(self)
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
        return self.ventasEncargadas
    @staticmethod
    def getEmpCreados():
        return Sede.getListaEmpleadosTotal()