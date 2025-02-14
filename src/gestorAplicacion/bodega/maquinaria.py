from typing import List
from ..sede import Sede

class Maquinaria:
    def __init__(self, nombre: str, valor: int, horaRevision: int, repuestos, sede: 'Sede'):
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
        self.listProveedoresBaratos = []
        self.ultFechaRevision = None

    def copiar(self):
        nuevosRepuestos = [rep.copiar() for rep in self.repuestos]
        return Maquinaria(self.nombre, self.valor, self.horaRevision, nuevosRepuestos, self.sede)

    @staticmethod
    def gastoMensualClase(fecha) -> int:
        gastoMaquinaria = 0
        for sede in Sede.getListaSedes():
            for maquinaria in sede.getListaMaquinas():
                for repuesto in maquinaria.repuestos:
                    gastoMaquinaria += repuesto.calcularGastoMensual(fecha)
        return gastoMaquinaria

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

    def getSede(self) -> 'Sede':
        return self.sede

    def agruparMaquinasDisponibles(self, fecha) -> List['Maquinaria']:
        from .repuesto import Repuesto
        maqDisponibles = []
        todosProvBaratos = []
        encontrado = False
        proveedorBarato = None
        for cadaSede in Sede.getListaSedes():
            for cadaMaquina in cadaSede.getListaMaquinas():
                if (cadaMaquina.getHoraRevision() - cadaMaquina.getHorasUso()) > 0:
                    cadaMaquina.mantenimiento = False
                    for cadaRepuesto in cadaMaquina.getRepuestos():
                        if (cadaRepuesto.getHorasDeVidaUtil() - cadaRepuesto.getHorasDeUso()) <= 0:
                            todosProvBaratos = self.encontrarProveedoresBaratos()
                            for elMasEconomico in todosProvBaratos:
                                if elMasEconomico.getInsumo().getNombre().lower() == cadaRepuesto.getNombre().lower():
                                    proveedorBarato = elMasEconomico
                                    break
                            for sedeCreada in Sede.getListaSedes():
                                if sedeCreada.getCuentaSede().getAhorroBanco() >= proveedorBarato.getInsumo().getPrecioIndividual():
                                    self.dondeRetirar()
                                    cadaMaquina.setRepuestos(cadaRepuesto)
                                    Repuesto.setListadoRepuestos(cadaRepuesto)
                                    cadaMaquina.getRepuestos().add(cadaRepuesto.copiar(proveedorBarato))
                                    cadaRepuesto.setPrecioCompra(proveedorBarato.getPrecio())
                                    cadaRepuesto.setFechasCompra(fecha)
                                    encontrado = True
                                    break
                            if not encontrado:
                                cadaRepuesto.setEstado()
                else:
                    cadaMaquina.mantenimiento = True
                    cadaMaquina.ultFechaRevision = fecha

                pista = 0
                for rep in cadaMaquina.getRepuestos():
                    if rep.isEstado():
                        pista += 1
                if len(cadaMaquina.getRepuestos()) == pista:
                    cadaMaquina.estado = True
                else:
                    cadaMaquina.estado = False

                if not cadaMaquina.mantenimiento and cadaMaquina.estado:
                    maqDisponibles.append(cadaMaquina)

                cadaMaquina.mantenimiento = False

        return maqDisponibles

    def encontrarProveedoresBaratos(self):
        from src.gestorAplicacion.bodega.proveedor import Proveedor
        from .repuesto import Repuesto
        for cadaRepuesto in Repuesto.getListadoRepuestos():
            proveedorBarato = None
            for proveedores in Proveedor.getListaProveedores():
                if proveedores.getInsumo().getNombre().lower() == cadaRepuesto.getNombre().lower():
                    if proveedorBarato is None:
                        proveedorBarato = proveedores
                    elif proveedores.getInsumo().getPrecioIndividual() <= proveedorBarato.getInsumo().getPrecioIndividual():
                        proveedorBarato = proveedores
            self.listProveedoresBaratos.append(proveedorBarato)
        return self.listProveedoresBaratos

    @staticmethod
    def asignarMaquinaria(emp):
        maquinariaPorAsignar = list(emp.getAreaActual().getMaquinariaNecesaria())
        for maq in emp.sede.getListaMaquinas():
            if maq.nombre in maquinariaPorAsignar or maq.user is None:
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

