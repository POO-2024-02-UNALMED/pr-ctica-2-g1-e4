from typing import List

from src.gestorAplicacion.administracion.empleado import Empleado
from src.gestorAplicacion.bodega.camisa import Camisa
from src.gestorAplicacion.bodega.pantalon import Pantalon
from src.gestorAplicacion.bodega.proveedor import Proveedor
from .repuesto import Repuesto
from ..sede import Sede

class Maquinaria:
    def __init__(self, nombre: str, valor: int, hora_revision: int, repuestos: List[Repuesto], sede: 'Sede'):
        self.nombre = nombre
        self.user = None
        self.horas_uso = 0
        self.estado = True
        self.asignable = True
        self.mantenimiento = False
        self.sede = sede
        self.valor = valor
        self.horas_visita_tecnico = 0
        self.hora_revision = hora_revision
        self.repuestos = repuestos
        self.list_proveedores_baratos = []
        self.ult_fecha_revision = None

    def copiar(self):
        nuevos_repuestos = [rep.copiar() for rep in self.repuestos]
        return Maquinaria(self.nombre, self.valor, self.hora_revision, nuevos_repuestos, self.sede)

    @staticmethod
    def gastoMensualClase(fecha: datetime) -> int:
        gasto_maquinaria = 0
        for sede in Sede.get_lista_sedes():
            for maquinaria in sede.get_lista_maquinas():
                for repuesto in maquinaria.repuestos:
                    gasto_maquinaria += repuesto.calcular_gasto_mensual(fecha)
        return gasto_maquinaria

    @staticmethod
    def remuneracionDanos(empleado: 'Empleado') -> int:
        remuneracion = 0
        for maq in empleado.sede.get_lista_maquinas():
            if maq.user == empleado and maq.estado:
                remuneracion += maq.valor
        return remuneracion

    @staticmethod
    def liberarMaquinariaDe(empleado: 'Empleado'):
        for maq in empleado.sede.get_lista_maquinas():
            if maq.user == empleado:
                maq.user = None

    def getNombre(self) -> str:
        return self.nombre

    def getRepuestos(self) -> List['Repuesto']:
        return self.repuestos

    def setRepuestos(self, repa_cambiar: 'Repuesto'):
        self.repuestos.remove(repa_cambiar)

    def getHoraRevision(self) -> int:
        return self.hora_revision

    def getHorasUso(self) -> int:
        return self.horas_uso

    def getSede(self) -> 'Sede':
        return self.sede

    def agruparMaquinasDisponibles(self, fecha: datetime) -> List['Maquinaria']:
        maq_disponibles = []
        todos_prov_baratos = []
        encontrado = False
        proveedor_barato = None
        for cada_sede in Sede.get_lista_sedes():
            for cada_maquina in cada_sede.get_lista_maquinas():
                if (cada_maquina.get_hora_revision() - cada_maquina.get_horas_uso()) > 0:
                    cada_maquina.mantenimiento = False
                    for cada_repuesto in cada_maquina.get_repuestos():
                        if (cada_repuesto.get_horas_de_vida_util() - cada_repuesto.get_horas_de_uso()) <= 0:
                            todos_prov_baratos = self.encontrarProveedoresBaratos()
                            for el_mas_economico in todos_prov_baratos:
                                if el_mas_economico.getInsumo().get_nombre().lower() == cada_repuesto.get_nombre().lower():
                                    proveedor_barato = el_mas_economico
                                    break
                            for sede_creada in Sede.get_lista_sedes():
                                if sede_creada.get_cuenta_sede().get_ahorro_banco() >= proveedor_barato.getInsumo().get_precio_individual():
                                    self.donde_retirar()
                                    cada_maquina.set_repuestos(cada_repuesto)
                                    Repuesto.setListadoRepuestos(cada_repuesto)
                                    cada_maquina.get_repuestos().add(cada_repuesto.copiar(proveedor_barato))
                                    cada_repuesto.set_precio_compra(proveedor_barato.getPrecio())
                                    cada_repuesto.set_fechas_compra(fecha)
                                    encontrado = True
                                    break
                            if not encontrado:
                                cada_repuesto.set_estado()
                else:
                    cada_maquina.mantenimiento = True
                    cada_maquina.ult_fecha_revision = fecha

                pista = 0
                for rep in cada_maquina.get_repuestos():
                    if rep.is_estado():
                        pista += 1
                if len(cada_maquina.get_repuestos()) == pista:
                    cada_maquina.estado = True
                else:
                    cada_maquina.estado = False

                if not cada_maquina.mantenimiento and cada_maquina.estado:
                    maq_disponibles.append(cada_maquina)

                cada_maquina.mantenimiento = False

        return maq_disponibles

    def encontrarProveedoresBaratos(self) -> List['Proveedor']:
        for cada_repuesto in Repuesto.getListadoRepuestos():
            proveedor_barato = None
            for proveedores in Proveedor.getListaProveedores():
                if proveedores.get_insumo().get_nombre().lower() == cada_repuesto.getNombre().lower():
                    if proveedor_barato is None:
                        proveedor_barato = proveedores
                    elif proveedores.get_insumo().get_precio_individual() <= proveedor_barato.get_insumo().get_precio_individual():
                        proveedor_barato = proveedores
            self.list_proveedores_baratos.append(proveedor_barato)
        return self.list_proveedores_baratos

    @staticmethod
    def asignarMaquinaria(emp):
        maquinaria_por_asignar = list(emp.get_area_actual().get_maquinaria_necesaria())
        for maq in emp.sede.get_lista_maquinas():
            if maq.nombre in maquinaria_por_asignar or maq.user is None:
                maq.user = emp
                maquinaria_por_asignar.remove(maq.nombre)
                break

    def __str__(self):
        return f"La {self.nombre} operada por {self.user.nombre} ubicada en la sede {self.sede.nombre} tiene {self.horas_uso} horas de uso"

    @staticmethod
    def seleccionarDeTipo(sede, tipo):
        import random
        random.shuffle(sede.get_lista_maquinas())
        for maq in sede.get_lista_maquinas():
            if maq.nombre == tipo:
                return maq
        return None

    def usar(self, horas: int):
        self.horas_uso += horas
        for repuesto in self.repuestos:
            repuesto.usar(horas)

    def esDeProduccion(self):
        return self.nombre in Camisa.getMaquinariaNecesaria() or self.nombre in Pantalon.getMaquinariaNecesaria()
