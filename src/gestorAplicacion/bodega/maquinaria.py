from typing import List

#from multimethod import multimethod
from ..sede import Sede

class Maquinaria:
    
    #@multimethod
    #def __init__(self, maquina: 'Maquinaria', repuestos: list):
        #self.nombre = maquina.nombre
        #self.sede = maquina.sede
        #self.valor = maquina.valor
        #self.horaRevision = maquina.horaRevision
        #self.repuestos = repuestos
        #self.sede.getListaMaquinas().append(self)
        #self.asignarRepAsedes(self.sede, repuestos)
        #self.horasUso = 0
        #self.user = None
        #self.estado = True
        #self.asignable = True
        #self.mantenimiento = False
        #self.horasVisitaTecnico = 0
        #self.ultFechaRevision = None
        
    #@multimethod        
    def __init__(self, nombre: str, valor: int, horaRevision: int, repuestos=[], sede: Sede=None, horasUso=0):
        
        self.nombre = nombre
        self.user = None
        self.horasUso = horasUso
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
        return Maquinaria(self.nombre, self.valor, self.horaRevision, nuevosRepuestos, self.sede)
        #return Maquinaria(self, nuevosRepuestos)
    
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
    def getSede(self) -> 'Sede':
        return self.sede
    
    @classmethod
    def agruparMaquinasDisponibles(cls, fecha) -> List['Maquinaria']:
        from .repuesto import Repuesto
        from src.uiMain.main import Main
        from src.gestorAplicacion.bodega.proveedor import Proveedor
        from src.gestorAplicacion.bodega.insumo import Insumo
        from src.uiMain.F5Produccion import receptor, recibeProveedorB, recibeMaqPaRevisar, recibeMaqDisp
        
        print(f"los repuestos mas actuales creados: {Repuesto.getListadoRepuestos()}\n y hay en total: {len(Repuesto.getListadoRepuestos())}")
        maqDisponibles = []
        todosProvBaratos = []
        encontrado = False
        proveedorBarato = None
        maquinasPaRevisar = []
        for cadaSede in Sede.getListaSedes():
            for cadaMaquina in cadaSede.getListaMaquinas():
                if (cadaMaquina.getHoraRevision() - cadaMaquina.getHorasUso()) > 0:
                    if not cadaMaquina.mantenimiento:
                        cadaMaquina.mantenimiento = False
                    for cadaRepuesto in cadaMaquina.getRepuestos():
                        if (cadaRepuesto.getHorasDeVidaUtil() - cadaRepuesto.getHorasDeUso()) <= 0:
                            receptor(Main.printsInt1(1, cadaRepuesto, cadaMaquina, cadaSede))
                            todosProvBaratos = cls.encontrarProveedoresBaratos()
                            print(len(todosProvBaratos))
                            for elMasEconomico in todosProvBaratos:
                                if elMasEconomico.getInsumo().getNombre().lower() == cadaRepuesto.getNombre().lower():
                                    print("adentro")
                                    proveedorBarato = elMasEconomico
                                    recibeProveedorB(proveedorBarato)
                                    print(proveedorBarato.getNombre())
                                    Main.recibeProveedorB(proveedorBarato)
                                    break

                            Main.evento_ui.clear()  
                            print("Esperando confirmación del usuario en la UI...")
                            Main.evento_ui.wait()
                            receptor("No hay mas repuestos por cambiar,\npresiona el boton de abajo para ver el resumen de la revisión...")
                            print("Usuario confirmó la compra. Continuando...")

                            for sedeCreada in Sede.getListaSedes():
                                if sedeCreada.getCuentaSede().getAhorroBanco() >= proveedorBarato.getPrecio():
                                    #Main.dondeRetirar()
                                    #print(f"\nla cantidad de repuestos que tiene {cadaMaquina.getNombre()} antes son: {len(cadaMaquina.getRepuestos())}")
                                    #print(f"repuestos de {cadaMaquina.getNombre()} son: {cadaMaquina.getRepuestos()}")
                                    #print(f"hay en total al iniciar {len(Repuesto.getListadoRepuestos())} repuestos creados")
                                    #print(f"soy {cadaRepuesto.getNombre()} de la maquina: {cadaMaquina.getNombre()}, de la sede: {cadaMaquina.getSede().getNombre()}")
                                    cadaMaquina.setRepuestos(cadaRepuesto)
                                    #print(f"\nla cantidad de repuestos que tiene {cadaMaquina.getNombre()} ahora mismo son: {len(cadaMaquina.getRepuestos())}")
                                    #print(f"repuestos de {cadaMaquina.getNombre()} son: {cadaMaquina.getRepuestos()}")
                                    Repuesto.removeRepuesto(cadaRepuesto)
                                    #print(f"\nahora hay {len(Repuesto.getListadoRepuestos())} repuestos creados\n")
                                    cadaMaquina.getRepuestos().append(cadaRepuesto.copiarConProveedor(proveedorBarato))
                                    #print(f"repuestos de {cadaMaquina.getNombre()} son: {cadaMaquina.getRepuestos()}")
                                    #print(f"los repuestos mas actuales creados: {Repuesto.getListadoRepuestos()}\n y hay en total: {len(Repuesto.getListadoRepuestos())}")
                                    cadaRepuesto.setPrecioCompra(proveedorBarato.getPrecio())
                                    cadaRepuesto.addFechaCompra(fecha)
                                    encontrado = True
                                    break
                            if not encontrado:
                                #llamar metodo en F5Produccion para mostrar algun label que diga que no 
                                #se pudo comprar el repuesto porque no hay plata en ninguna sede,
                                #este label iría en donde se elige de cual sede descontar la plata 
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
                if cadaMaquina.mantenimiento is False and cadaMaquina.estado is True:
                    maqDisponibles.append(cadaMaquina)
                else:
                    maquinasPaRevisar.append(cadaMaquina)
                
        recibeProveedorB(None)
        recibeMaqPaRevisar(maquinasPaRevisar)
        recibeMaqDisp(maqDisponibles)
        print("finish interaccion 1")
        return maqDisponibles

    @classmethod
    def encontrarProveedoresBaratos(cls):
        from src.gestorAplicacion.bodega.proveedor import Proveedor
        from .repuesto import Repuesto
        listProveedoresBaratos = []
        for cadaRepuesto in Repuesto.getListadoRepuestos():
            proveedorBarato = None
            for proveedores in Proveedor.getListaProveedores():
                if proveedores.getInsumo().getNombre().lower() == cadaRepuesto.getNombre().lower():
                    if proveedorBarato is None:
                        proveedorBarato = proveedores
                    elif proveedores.getInsumo().getPrecioIndividual() <= proveedorBarato.getInsumo().getPrecioIndividual():
                        proveedorBarato = proveedores
            if proveedorBarato not in listProveedoresBaratos:
                listProveedoresBaratos.append(proveedorBarato)
        return listProveedoresBaratos

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