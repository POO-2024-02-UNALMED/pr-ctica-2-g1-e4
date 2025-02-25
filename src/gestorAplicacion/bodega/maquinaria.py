from typing import List

from multimethod import multimethod
from ..sede import Sede
from src.gestorAplicacion.fecha import Fecha

class Maquinaria:
    
    @multimethod
    def __init__(self, maquina: 'Maquinaria', repuestos: list):
        self.nombre = maquina.nombre
        self.sede = maquina.sede
        self.valor = maquina.valor
        self.horaRevision = maquina.horaRevision
        self.repuestos = repuestos
        self.sede.getListaMaquinas().append(self)
        self.asignarRepAsedes(self.sede, repuestos)
        self.horasUso = 0
        self.user = None
        self.estado = True
        self.asignable = True
        self.mantenimiento = False
        self.horasVisitaTecnico = 0
        self.ultFechaRevision = None
    
    @multimethod
    def __init__(self, nombre: str):
        self.nombre = nombre

    @multimethod        
    def __init__(self, nombre: str, valor: int, horaRevision: int, repuestos: list, sede: Sede):
        
        self.nombre = nombre
        self.user = None
        self.horasUso = 0
        self.estado = True
        self.asignable = True
        self.mantenimiento = False
        self.sede = sede
        self.valor = valor
        self.horasVisitaTecnico = 0
        self.horaRevision = horaRevision
        self.repuestos = repuestos
        sede.getListaMaquinas().append(self)
        self.asignarRepAsedes(sede, repuestos)
        self.ultFechaRevision = None

    def copiar(self):
        nuevosRepuestos = [rep.copiar() for rep in self.repuestos]
        #return Maquinaria(self.nombre, self.valor, self.horaRevision, nuevosRepuestos, self.sede)
        return Maquinaria(self, nuevosRepuestos)
    
    @staticmethod
    def gastoMensualClase(fecha) -> int:
        gastoMaquinaria = 0
        for sede in Sede.getListaSedes():
            for maquinaria in sede.getListaMaquinas():
                for repuesto in maquinaria.repuestos:
                    gastoMaquinaria += repuesto.calcularGastoMensual(fecha)
        return gastoMaquinaria
    
    def asignarRepAsedes(self, sede, listaRepuestos):
        for rep in listaRepuestos:
            rep.setSede(sede)

    @staticmethod
    def remuneracionDanos(empleado):
        from src.gestorAplicacion.administracion.empleado import Empleado
        remuneracion = 0
        for maq in empleado.sede.getListaMaquinas():
            if maq.user == empleado and maq.estado:
                remuneracion += maq.valor
        return remuneracion

    @staticmethod
    def liberarMaquinariaDe(empleado):
        from src.gestorAplicacion.administracion.empleado import Empleado
        for maq in empleado.sede.getListaMaquinas():
            if maq.user == empleado:
                maq.user = None

    def getNombre(self) -> str:
        return self.nombre
    def getRepuestos(self):
        return self.repuestos
    def setRepuestos(self, repaCambiar):
        self.repuestos.remove(repaCambiar)
    def getHoraRevision(self) -> int:
        return self.horaRevision
    def getHorasUso(self) -> int:
        return self.horasUso
    def setHorasUso(self):
        self.horasUso = 0
    def getSede(self) -> 'Sede':
        return self.sede
    

    @staticmethod
    def asignarMaquinaria(emp):
        maquinariaPorAsignar = emp.getAreaActual().getMaquinariaNecesaria().copy()
        for maq in emp.sede.getListaMaquinas():
            if maq.nombre in maquinariaPorAsignar and maq.user is None:
                maq.user = emp
                maquinariaPorAsignar.remove(maq.nombre)
                break

    def __str__(self):
        return f"La {self.nombre} operada por {self.user.nombre} ubicada en la sede {self.sede.nombre} tiene {self.horasUso} horas de uso"

    @staticmethod
    def seleccionarDeTipo(sede, tipo):
        import random
        random.shuffle(sede.getListaMaquinas())
        for maq in sede.getListaMaquinas():
            if maq.nombre == tipo:
                return maq
        return None

    def usar(self, horas: int):
        self.horasUso += horas
        for repuesto in self.repuestos:
            repuesto.usar(horas)

    def esDeProduccion(self):
        return self.deCamisa() or self.dePantalon()
    
    def deCamisa(self):
        from src.gestorAplicacion.bodega.camisa import Camisa
        return self.nombre in Camisa.getMaquinariaNecesaria()
    
    def dePantalon(self):
        from src.gestorAplicacion.bodega.pantalon import Pantalon
        return self.nombre in Pantalon.getMaquinariaNecesaria()

    def setHorasUso(self, horas):
        self.horasUso = horas

    @classmethod
    def hanPasadoMasDeTresDias(cls, fecha1: Fecha, fecha2: Fecha) -> bool:
        diferencia = 0
        diferencia = fecha2.aDiasTotales() - fecha1.aDiasTotales()
        return diferencia > 3