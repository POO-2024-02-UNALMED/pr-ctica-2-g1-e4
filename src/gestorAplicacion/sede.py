from src.gestorAplicacion.administracion.rol import Rol
from src.gestorAplicacion.bodega.insumo import Insumo
from .fecha import Fecha
from typing import List

class Sede:
    prendasInventadasTotal = []; listaEmpleadosTotal = []; listaSedes = []; evaluacionesFinancieras = []

    def __init__(self, nombre="Sede"):
        self.listaEmpleado = []; self.listaMaquina = []; self.historialVentas = []; self.prendasInventadas = []
        self.listaInsumosBodega = []; self.cantidadInsumosBodega = []; self.produccionAproximada = []
        self.prendasProduccion = [];self.maqProduccion = []; self.maqOficina = []
        self.nombre = nombre
        self.cuentaSede = None
        if self.nombre.lower() != "sede":
            Sede.getListaSedes().append(self)

    @classmethod
    def verificarProductoBodega(cls, insumo, sede):
        retorno = False
        index = -1
        for x in range(len(sede.listaInsumosBodega)):
            if insumo == sede.listaInsumosBodega[x]:
                index = x
                retorno = True
                break
        
        return retorno, index

    def encontrarInsumoEnBodega(self,insumo:Insumo):
        for idxInsumo in range(len(self.listaInsumosBodega)):
            if insumo.getNombre() == self.listaInsumosBodega[idxInsumo].getNombre():
                return idxInsumo
        return

    @classmethod
    def transferirInsumo(cls, insumo, donadora, beneficiaria, cantidadSolicitada):
        restante = 0
        idxInsumo = donadora.encontrarInsumoEnBodega(insumo)
        if idxInsumo == -1:
            return cantidadSolicitada  # Skip the rest of the method, because there is nothing to transfer.
        cantidadDisponible = min(donadora.cantidadInsumosBodega[idxInsumo], cantidadSolicitada)
        ajusteStock = Insumo.getPrecioStockTotal() - (insumo.getPrecioIndividual() * cantidadSolicitada)
        Insumo.setPrecioStockTotal(ajusteStock)
        if (cantidadDisponible - cantidadSolicitada) == 0: # Si hay exactamente la cantidad solicitada
            donadora.cantidadInsumosBodega[idxInsumo] = 0
        elif (cantidadDisponible - cantidadSolicitada) < 0: # Si hay menos de la cantidad solicitada
            restante = (cantidadSolicitada - cantidadDisponible) 
            donadora.cantidadInsumosBodega[idxInsumo] = 0
        else:
            donadora.cantidadInsumosBodega[idxInsumo] = (cantidadDisponible - cantidadSolicitada)
        cantidadATransferir = cantidadSolicitada if restante<= 0 else cantidadDisponible
        cls.anadirInsumo(insumo, beneficiaria, cantidadATransferir)
        return restante

    @classmethod
    def anadirInsumo(cls, insumo, sede, cantidad):
        for idxInsumoEnBodega in range(len(sede.getListaInsumosBodega())):
            if insumo.getNombre() == sede.getListaInsumosBodega()[idxInsumoEnBodega].getNombre():
                cantidadActual = sede.getCantidadInsumosBodega()[idxInsumoEnBodega]
                sede.cantidadInsumosBodega[idxInsumoEnBodega] = cantidadActual + cantidad
                ajusteStock = Insumo.getPrecioStockTotal() + (insumo.getPrecioIndividual() * cantidad)
                Insumo.setPrecioStockTotal(ajusteStock)

    @classmethod
    def verificarProductoOtraSede(cls, insumo,excluirSede):
        retorno = False
        index = -1
        sedeATransferir = None
        precio = 0
        for sede in cls.listaSedes:
            if sede == excluirSede:
                continue
            for x in range(len(sede.getListaInsumosBodega())):
                if insumo.getNombre() == sede.getListaInsumosBodega()[x].getNombre():
                    if sede.getCantidadInsumosBodega()[x] > 0:
                        index = x
                        retorno = True
                        sedeATransferir = sede
                        precio = sede.getListaInsumosBodega()[x].getPrecioIndividual()
                        break
        
        return retorno, index, sedeATransferir, precio

    def actualizarHistorialVentas(self,venta):
        self.historialVentas.append(venta)
        pass
    def getRendimientoDeseado(self, area, fecha):
        from .administracion.area import Area
        Area.rendimientoDeseadoActual(self, fecha)
        return area.rendimientoDeseado
    @classmethod
    def setListaSedes(cls, sedes):
        cls.listaSedes=sedes
    @staticmethod
    def getListaSedes():
        return Sede.listaSedes
    def getListaEmpleados(self):
        return self.listaEmpleado
    def setListaEmpleados(self, emp):
        self.listaEmpleado = emp
    def getListaMaquinas(self):
        return self.listaMaquina
    def setListaMaquinas(self, maquinaria):
        self.listaMaquina = maquinaria
    def getHistorialVentas(self)->List:
        return self.historialVentas
    def setHistorialVentas(self, venta):
        self.historialVentas = venta
    def getPrendasInventadas(self):
        return self.prendasInventadas
    def setPrendasInventadas(self, prenda):
        self.prendasInventadas = prenda
    def getListaInsumosBodega(self):
        return self.listaInsumosBodega
    def setListaInsumosBodega(self, insumos):
        self.listaInsumosBodega = insumos
    def getCantidadInsumosBodega(self):
        return self.cantidadInsumosBodega
    def setCantidadInsumosBodega(self, cantidadIns):
        self.cantidadInsumosBodega = cantidadIns
    def getProduccionAproximada(self):
        return self.produccionAproximada
    def setProduccionAproximada(self, produccion):
        self.produccionAproximada = produccion
    def getPrendasProduccion(self):
        return self.prendasProduccion
    def setPrendasProduccion(self, prendasProduccion):
        self.prendasProduccion = prendasProduccion
    def getNombre(self):
        return self.nombre
    def setNombre(self, nombre):
        self.nombre = nombre
    def setCuentaSede(self, cuenta):
        self.cuentaSede = cuenta
    def getCuentaSede(self):
        return self.cuentaSede
    def anadirEmpleado(self, emp):
        self.listaEmpleado.append(emp)
    def quitarEmpleado(self, emp):
        self.listaEmpleado.remove(emp)
    @classmethod
    def setEvaluacionesFinancieras(cls, evaluaciones):
        cls.evaluacionesFinancieras = evaluaciones
    @classmethod
    def getEvaluacionesFinancieras(cls):
        return cls.evaluacionesFinancieras
    @classmethod
    def getListaEmpleadosTotal(cls):
        return cls.listaEmpleadosTotal
    @classmethod
    def setListaEmpleadosTotal(cls, empleados):
        cls.listaEmpleadosTotal = empleados  # Para serializacion
    @classmethod
    def getPrendasInventadasTotal(cls):
        return cls.prendasInventadasTotal
    @classmethod
    def setPrendasInventadasTotal(cls, prendas):
        cls.prendasInventadasTotal = prendas  # Para serializacion
    def getProdAproximada(self):
        return self.prodAproximada
    
    def obtenerNecesidadTransferenciaEmpleados(despedidos:List):  # Despedidos es A en el doc.
        rolesARevisar = []; sedeOrigen = []
        for empleado in despedidos:
            if empleado.getRol() not in rolesARevisar:
                rolesARevisar.append(empleado.getRol())
                sedeOrigen.append(empleado.getSede())

        transferirDe = []; rolesATransferir = []
        for idxRol in range(len(rolesARevisar)):
            rol = rolesARevisar[idxRol]
            # Revisar sedes donadoras
            for sede in Sede.listaSedes:
                if sede == sedeOrigen[idxRol]:
                    continue  # Evitar donacion de la misma sede de origen.
                if rol == Rol.MODISTA:
                    if sede.cantidadPorRol(rol) != 0:
                        produccionTotal = sum(sede.getProduccionAproximada())
                        produccionPorModista = produccionTotal / sede.cantidadPorRol(rol)
                        if produccionPorModista < 30:
                            transferirDe.append(sede)
                            rolesATransferir.append(rol)
                            break  # Salir de la revisión de sedes donadoras
                elif rol == Rol.SECRETARIA:
                    ejecutivos = sede.cantidadPorRol(Rol.EJECUTIVO)
                    secretarias = sede.cantidadPorRol(Rol.SECRETARIA)
                    empleados = len(sede.listaEmpleado)
                    if not (empleados / secretarias > 18 or ejecutivos / secretarias > 2):
                        transferirDe[idxRol] = sede
                        rolesATransferir.append(rol)
                        break  # Salir de la revisión de sedes donadoras
        retorno = []
        retorno.append(rolesATransferir)
        retorno.append(transferirDe)
        aReemplazar = despedidos.copy()
        for empleado in despedidos:
            if empleado.getRol() in rolesATransferir:
                aReemplazar.remove(empleado)
        retorno.append(aReemplazar)
        return retorno

    def reemplazarPorCambioSede(despedidos, aTransferir)->List:
        from .bodega.maquinaria import Maquinaria
        aTransferir = aTransferir.copy() # Evita efectos secundarios.
        reemplazados=[]
        for empleadoDespedido in despedidos:
            # Buscamos en la lista de empleados a transferir, quien pudo ser seleccionado como reemplazo.
            for empleadoReemplazo in aTransferir:
                if empleadoDespedido.getRol() == empleadoReemplazo.getRol():
                    remuneracionAPagar = Maquinaria.remuneracionDanos(empleadoReemplazo)
                    empleadoReemplazo.modificarBonificacion(remuneracionAPagar * -1)
                    empleadoReemplazo.setSede(empleadoDespedido.getSede())
                    Maquinaria.asignarMaquinaria(empleadoReemplazo)
                    aTransferir.remove(empleadoReemplazo)
                    reemplazados.append(empleadoDespedido)
                    break
        return reemplazados

    def quitarInsumos(self, insumos, cantidad):
        hayInsumos = True
        for insumo in insumos:
            if insumo not in self.listaInsumosBodega:
                hayInsumos = False
                break
            idxInsumoEnSede = self.listaInsumosBodega.index(insumo)
            if self.cantidadInsumosBodega[idxInsumoEnSede] < cantidad[insumos.index(insumo)]:
                hayInsumos = False
                break
        if hayInsumos:
            for insumo in insumos:
                idxInsumoEnSede = self.listaInsumosBodega.index(insumo)
                self.cantidadInsumosBodega[idxInsumoEnSede] -= cantidad[insumos.index(insumo)]
        return hayInsumos

    # Devuelve la cantidad de empleados que hay en la sede con el rol dado
    # metodo ayudante para reorganizarEmpleados
    def cantidadPorRol(self,rol):
        cantidad = 0
        for empleado in self.getListaEmpleados():
            if empleado.getRol() == rol:
                cantidad += 1
        return cantidad

    def cantidadPorArea(area):
        cantidad = 0
        for empleado in Sede.listaEmpleado:
            if empleado.getAreaActual() == area:
                cantidad += 1
        return cantidad

    def __str__(self):
        return self.nombre
    def __repr__(self):
        return self.__str__()

    # Usado para eliminar un Insumo limpiamente
    @classmethod
    def quitarInsumoDeBodegas(cls, insumo):
        for sede in cls.listaSedes:
            for idxInsumo in range(len(sede.getListaInsumosBodega())):
                if sede.getListaInsumosBodega()[idxInsumo] == insumo:
                    sede.getListaInsumosBodega().remove(sede.getListaInsumosBodega()[idxInsumo])
                    sede.getCantidadInsumosBodega().remove(sede.getCantidadInsumosBodega()[idxInsumo])

    def cantidadPorArea(self, areaActual) -> int:
        cantidad = 0
        for emp in self.getListaEmpleados():
            if emp.areaActual == areaActual:
                cantidad += 1
        return cantidad

    # PARA LA INTERACCION 2 DE PRODUCCION
    @classmethod
    def sobreCargada(cls, fecha: 'Fecha') -> int:
        senal = 0
        produccionSedes = cls.calcProduccionSedes(fecha)
        print(f"La produccion por ahora es: {produccionSedes}")
        modistas = cls.modistasQueHay()
        if modistas[0] > 0 and ((produccionSedes[0][0] + produccionSedes[0][1]) / modistas[0]) > 400:
            senal = 5
        if modistas[1] > 0 and ((produccionSedes[1][0] + produccionSedes[1][1]) / modistas[1]) > 400:
            senal += 10
        return senal

    @classmethod
    def calcProduccionSedes(cls, fecha: 'Fecha') -> List[List[int]]:
        from .venta import Venta
        prodSedesCalculada = []; prodCalculadaSedeP = []; prodCalculadaSede2 = []
        prodCalculadaSedeP.append(Venta.predecirVentas(fecha, Sede.getListaSedes()[0], "Pantalon"))
        prodCalculadaSedeP.append(Venta.predecirVentas(fecha, Sede.getListaSedes()[0], "Camisa"))
        prodCalculadaSede2.append(Venta.predecirVentas(fecha, Sede.getListaSedes()[1], "Pantalon"))
        prodCalculadaSede2.append(Venta.predecirVentas(fecha, Sede.getListaSedes()[1], "Camisa"))
        prodSedesCalculada.append(prodCalculadaSedeP)
        prodSedesCalculada.append(prodCalculadaSede2)
        return prodSedesCalculada

    @classmethod
    #def prodSedeP(cls, fecha: 'Fecha') -> List[int]:
    #    pantalonesSedeP = cls.calcProduccionSedes(fecha)[0][0] + cls.calcProduccionSedes(fecha)[1][0]
    #    camisasSedeP = cls.calcProduccionSedes(fecha)[0][1] + cls.calcProduccionSedes(fecha)[1][1]
    #    prodAproximada = [pantalonesSedeP, camisasSedeP]
    #    return prodAproximada

    @classmethod        #siento que aquí falta algo
    def prodSede2(cls, fecha: 'Fecha') -> List[int]:
        pantalonesSede2 = cls.calcProduccionSedes(fecha)[1][0]
        camisasSede2 = cls.calcProduccionSedes(fecha)[1][1]
        prodAproximada = [pantalonesSede2, camisasSede2]
        return prodAproximada

    def insumosPorNombre(self, nombres):
        insumos = []
        for nombre in nombres:
            for insumo in self.listaInsumosBodega:
                if insumo.getNombre().lower() == nombre.lower():
                    insumos.append(insumo)
        return insumos

    @classmethod
    def modistasQueHay(cls) -> List[int]:
        modistasEnCadaSede = [0, 0]
        for empCreados in Sede.listaEmpleadosTotal:
            if empCreados.getAreaActual().getNombre().lower() == "corte":
                if empCreados.getSede().getNombre().lower() == "sede principal":
                    modistasEnCadaSede[0] += 1
                elif empCreados.getSede().getNombre().lower() == "sede 2":
                    modistasEnCadaSede[1] += 1
        return modistasEnCadaSede

    @classmethod
    def prodTransferida1(cls, fecha) -> List[int]:
        produccionSedes = cls.calcProduccionSedes(fecha)
        return [produccionSedes[1][0], produccionSedes[1][1]]

    @classmethod
    def prodTransferida2(cls, fecha) -> List[int]:
        produccionSedes = cls.calcProduccionSedes(fecha)
        return [produccionSedes[0][0], produccionSedes[0][1]]

    @classmethod
    def planProduccion(cls, maqDisponible: List, fecha: 'Fecha') -> List[List[List[int]]]:
        from .bodega.maquinaria import Maquinaria
        from src.uiMain.main import Main
        from src.uiMain.F5Produccion import recibeMaqDispSeparadas, recibeTextIndicador, recibeProdFinal
        import math
        aProducirFinal = []; aProducir = []; listaEspera = []; listaDeCeros = [0, 0]
        listaEsperaVacia = [listaDeCeros.copy(), listaDeCeros.copy()]
        maqSedeP = []; maqSede2 = []
        senal = 0

        # Dividir las máquinas disponibles por sedes
        for todMaquinas in maqDisponible:
            if todMaquinas.getSede().getNombre().lower() == "sede principal":
                maqSedeP.append(todMaquinas)
            else:
                maqSede2.append(todMaquinas)

        # Dividir las máquinas de cada sede por función
        Sede.getListaSedes()[0].maqProduccion = [] ; Sede.getListaSedes()[1].maqProduccion = []
        for todMaqSedeP in maqSedeP:
            if todMaqSedeP.esDeProduccion():
                if not todMaqSedeP.mantenimiento:
                    Sede.getListaSedes()[0].maqProduccion.append(todMaqSedeP)
            else:
                Sede.getListaSedes()[0].maqOficina.append(todMaqSedeP)
        for todMaqSede2 in maqSede2:
            if todMaqSede2.esDeProduccion():
                if not todMaqSede2.mantenimiento:
                    Sede.getListaSedes()[1].maqProduccion.append(todMaqSede2)
            else:
                Sede.getListaSedes()[1].maqOficina.append(todMaqSede2)
        if len(Sede.getListaSedes()[0].maqProduccion) > 3:
            senal = 5
        if len(Sede.getListaSedes()[1].maqProduccion) > 3:
            senal += 10

        recibeMaqDispSeparadas(Sede.getListaSedes()[0].maqProduccion, Sede.getListaSedes()[1].maqProduccion)

        if senal == 5:
            recibeTextIndicador(Main.printsInt2(1), 1)
            Main.evento_ui.clear()  
            print("\nEsperando confirmación para seguir con la produccion")
            Main.evento_ui.wait()
            print("Seguir planificando produccion en la sede principal\n")
                #Envia la produccion de la sede 2 a producir la otra semana en la sede Principal
            aProducir.insert(0, cls.calcProduccionSedes(fecha)[0])
            aProducir.insert(1, listaDeCeros.copy())
            listaEspera.insert(0, cls.prodTransferida1(fecha))
            listaEspera.insert(1, listaDeCeros.copy())
            aProducirFinal.insert(0, aProducir)
            aProducirFinal.insert(1, listaEspera)
                
        elif senal == 10:
            recibeTextIndicador(Main.printsInt2(3), 2)
            Main.evento_ui.clear()  
            print("\nEsperando confirmación para seguir con la produccion")
            Main.evento_ui.wait()
            print("Seguir planificando produccion en la sede 2\n")
                    #Envia la produccion de la sede Principal a producir la otra semana en la sede 2
            aProducir.insert(0, listaDeCeros.copy())
            aProducir.insert(1, cls.calcProduccionSedes(fecha)[1])         
            listaEspera.insert(0, listaDeCeros.copy())
            listaEspera.insert(1, cls.prodTransferida2(fecha))
            aProducirFinal.insert(0, aProducir)
            aProducirFinal.insert(1, listaEspera)

        elif senal == 15:
            # Se produce todo entre las dos sedes
            recibeTextIndicador(Main.printsInt2(12), 3)
            Main.evento_ui.clear()  
            print("\nEsperando confirmación para seguir con la produccion")
            Main.evento_ui.wait()
            print("Seguir planificando produccion en las dos sedes...\n")
            senalRec = cls.sobreCargada(fecha)
            if senalRec == 5:
                #enviar Produccion con la lista de espera en cero para modificarla manualmente en la interfaz
                aProducir = cls.calcProduccionSedes(fecha)
                aProducirFinal.insert(0, aProducir) ; aProducirFinal.insert(1, listaEsperaVacia.copy())
            elif senalRec == 10:
                #enviar Produccion con la lista de espera en cero para modificarla manualmente en la interfaz
                aProducir = cls.calcProduccionSedes(fecha)
                aProducirFinal.insert(0, aProducir) ; aProducirFinal.insert(1, listaEsperaVacia.copy())
            elif senalRec == 15:
                pSedePEspera = math.ceil(cls.calcProduccionSedes(fecha)[0][0]*0.3)
                pSedeP = cls.calcProduccionSedes(fecha)[0][0] - pSedePEspera
                cSedePEspera = math.ceil(cls.calcProduccionSedes(fecha)[0][1]*0.3)
                cSedeP = cls.calcProduccionSedes(fecha)[0][1] - cSedePEspera
                pSede2Espera = math.ceil(cls.calcProduccionSedes(fecha)[1][0]*0.3)
                pSede2 = cls.calcProduccionSedes(fecha)[1][0] - pSede2Espera
                cSede2Espera = math.ceil(cls.calcProduccionSedes(fecha)[1][1]*0.3)
                cSede2 = cls.calcProduccionSedes(fecha)[1][1] - cSede2Espera
                elGuardaPDeHoy = [pSedeP, cSedeP]
                elGuarda2DeHoy = [pSede2, cSede2]
                elGuardaPDeManana = [pSedePEspera, cSedePEspera]
                elGuarda2DeManana = [pSede2Espera, cSede2Espera]
                aProducir.insert(0, elGuardaPDeHoy) ; aProducir.insert(1, elGuarda2DeHoy)
                listaEspera.insert(0, elGuardaPDeManana) ; listaEspera.insert(1, elGuarda2DeManana)
                
                aProducirFinal.insert(0, aProducir) ; aProducirFinal.insert(1, listaEspera)
                print(f"La produccion final es: {aProducirFinal}")
                
            elif senalRec == 0:
                    # Ninguna sede está sobrecargada, entonces se envia produccion normal
                aProducir = cls.calcProduccionSedes(fecha)
                aProducirFinal.insert(0, aProducir) ; aProducirFinal.insert(1, listaEsperaVacia.copy())
        else:
                #no se puede producir nada porque ninguna sede esta disponible, enviar el print siguiente a la interfaz y darle un boton para volver
            aProducirFinal = None
            recibeTextIndicador(Main.printsInt2(11), 4)
        
        if aProducirFinal is not None:
            recibeProdFinal(aProducirFinal)
        return aProducirFinal

    @classmethod
    def sedeExiste(cls,nombre):
        for sede in cls.listaSedes:
            if sede.getNombre().lower() == nombre.lower():
                return True
        return False
    def getEmpleado(self, nombre):
        for empleado in self.listaEmpleado:
            if empleado.getNombre().lower() == nombre.lower():
                return empleado
        return None
    @classmethod
    def getHistoialTotalVentas(cls):
        historial = []
        for sede in cls.listaSedes:
            for venta in sede.getHistorialVentas():
                historial.append(venta)
        return historial 
    @classmethod
    def setHistoialTotalVentas(cls,lista):
        for sede in cls.listaSedes:
            for venta in lista:
                if venta.getSede()==sede:
                    sede.getHistorialVentas().append(venta)