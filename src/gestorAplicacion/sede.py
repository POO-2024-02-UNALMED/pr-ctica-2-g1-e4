from src.gestorAplicacion.administracion.resultado import Resultado
from src.gestorAplicacion.administracion.rol import Rol
from src.gestorAplicacion.bodega.insumo import Insumo
from .fecha import Fecha
from typing import List

class Sede:
    prendasInventadasTotal = [], listaEmpleadosTotal = [], listaSedes = [], evaluacionesFinancieras = []

    def __init__(self, nombre="Sede"):
        self.listaEmpleado = [], self.listaMaquina = [], self.historialVentas = [], self.prendasInventadas = []
        self.listaInsumosBodega = [], self.cantidadInsumosBodega = [], self.produccionAproximada = []
        self.prendasProduccion = [],self.maqProduccion = [], self.maqOficina = []
        self.nombre = nombre
        self.cuentaSede = None
        Sede.setListaSedes(self)

    @classmethod
    def verificarProductoBodega(cls, insumo, sede):
        retorno = False
        index = -1
        for x in range(len(sede.listaInsumosBodega)):
            if insumo == sede.listaInsumosBodega[x]:
                index = x
                retorno = True
                break
        resultado = Resultado(retorno, index)
        return resultado

    @classmethod
    def transferirInsumo(cls, insumo, donadora, beneficiaria, cantidadSolicitada):
        restante = 0
        idxInsumo = donadora.listaInsumosBodega.index(insumo)
        if idxInsumo == -1:
            return cantidadSolicitada  # Skip the rest of the method, because there is nothing to transfer.
        cantidadDisponible = min(donadora.cantidadInsumosBodega.index(idxInsumo), cantidadSolicitada)
        ajusteStock = Insumo.getPrecioStockTotal() - (insumo.getPrecioIndividual() * cantidadSolicitada)
        Insumo.setPrecioStockTotal(ajusteStock)
        if (cantidadDisponible - cantidadSolicitada) == 0:
            donadora.cantidadInsumosBodega[idxInsumo] = 0
        elif (cantidadDisponible - cantidadSolicitada) < 0:
            restante = (cantidadDisponible - cantidadSolicitada) * -1
            donadora.cantidadInsumosBodega[idxInsumo] = 0
        else:
            donadora.cantidadInsumosBodega[idxInsumo] = (cantidadDisponible - cantidadSolicitada)
        cls.anadirInsumo(insumo, beneficiaria, cantidadSolicitada - cantidadDisponible)
        return restante

    @classmethod
    def anadirInsumo(cls, insumo, sede, cantidad):
        for idxInsumoEnBodega in range(len(sede.getListaInsumosBodega())):
            if insumo == sede.getListaInsumosBodega()[idxInsumoEnBodega]:
                cantidadActual = sede.getCantidadInsumosBodega()[idxInsumoEnBodega]
                sede.cantidadInsumosBodega[idxInsumoEnBodega] = cantidadActual + cantidad
                ajusteStock = Insumo.getPrecioStockTotal() + (insumo.getPrecioIndividual() * cantidad)
                Insumo.setPrecioStockTotal(ajusteStock)

    @classmethod
    def verificarProductoOtraSede(cls, insumo):
        retorno = False
        index = -1
        sedeATransferir = None
        precio = 0
        for sede in cls.listaSedes:
            for x in range(len(sede.getListaInsumosBodega())):
                if insumo == sede.getListaInsumosBodega()[x]:
                    for cantidad in sede.cantidadInsumosBodega:
                        if sede.getCantidadInsumosBodega()[x] != 0:
                            index = x
                            retorno = True
                            sedeATransferir = sede
                            precio = insumo.getPrecioCompra()
                            break
        resultado = Resultado(retorno, index, sedeATransferir, precio)
        return resultado

    def actualizarHistorialVentas(self,venta):
        self.historialVentas.append(venta)
        pass
    def getRendimientoDeseado(self, area, fecha):
        from .administracion.area import Area
        Area.rendimientoDeseadoActual(self, fecha)
        return area.rendimientoDeseado
    @classmethod
    def setListaSedes(cls, sede):
        cls.listaSedes.append(sede)
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
    
    def obtenerNecesidadTransferenciaEmpleados(despedidos):  # Despedidos es A en el doc.
        rolesARevisar = [], sedeOrigen = []
        for empleado in despedidos:
            if empleado.getRol() not in rolesARevisar:
                rolesARevisar.append(empleado.getRol())
                sedeOrigen.append(empleado.getSede())

        transferirDe = [], rolesATransferir = []
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

    def reemplazarPorCambioSede(despedidos, aTransferir):
        from .bodega.maquinaria import Maquinaria
        for empleadoDespedido in despedidos:
            # Buscamos en la lista de empleados a transferir, quien pudo ser seleccionado como reemplazo.
            for empleadoReemplazo in aTransferir:
                if empleadoDespedido.getRol() == empleadoReemplazo.getRol():
                    remuneracionAPagar = Maquinaria.remuneracionDanos(empleadoReemplazo)
                    empleadoReemplazo.modificarBonificacion(remuneracionAPagar * -1)
                    empleadoReemplazo.setSede(empleadoDespedido.getSede())
                    Maquinaria.asignarMaquinaria(empleadoReemplazo)
                    aTransferir.remove(empleadoReemplazo)
                    break

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
    def cantidadPorRol(rol):
        cantidad = 0
        for empleado in Sede.listaEmpleado:
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
    def sobreCargada(self, fecha: 'Fecha') -> int:
        senal = 0
        produccionSedes = self.calcProduccionSedes(fecha)
        modistas = self.modistasQueHay()
        if modistas[0] > 0 and ((produccionSedes[0][0] + produccionSedes[0][1]) / modistas[0]) > 10:
            senal = 5
        if modistas[1] > 0 and ((produccionSedes[1][0] + produccionSedes[1][1]) / modistas[1]) > 10:
            senal += 10
        return senal

    def calcProduccionSedes(self, fecha: 'Fecha') -> List[List[int]]:
        from .venta import Venta
        prodSedesCalculada = [], prodCalculadaSedeP = [], prodCalculadaSede2 = []
        prodCalculadaSedeP.append(Venta.predecirVentas(fecha, Sede.getListaSedes()[0], "Pantalon"))
        prodCalculadaSedeP.append(Venta.predecirVentas(fecha, Sede.getListaSedes()[0], "Camisa"))
        prodCalculadaSede2.append(Venta.predecirVentas(fecha, Sede.getListaSedes()[1], "Pantalon"))
        prodCalculadaSede2.append(Venta.predecirVentas(fecha, Sede.getListaSedes()[1], "Camisa"))
        prodSedesCalculada.append(prodCalculadaSedeP)
        prodSedesCalculada.append(prodCalculadaSede2)
        return prodSedesCalculada

    def prodSedeP(self, fecha: 'Fecha') -> List[int]:
        pantalonesSedeP = self.calcProduccionSedes(fecha)[0][0] + self.calcProduccionSedes(fecha)[1][0]
        camisasSedeP = self.calcProduccionSedes(fecha)[0][1] + self.calcProduccionSedes(fecha)[1][1]
        prodAproximada = [pantalonesSedeP, camisasSedeP]
        return prodAproximada

    def prodSede2(self, fecha: 'Fecha') -> List[int]:
        pantalonesSede2 = self.calcProduccionSedes(fecha)[1][0]
        camisasSede2 = self.calcProduccionSedes(fecha)[1][1]
        prodAproximada = [pantalonesSede2, camisasSede2]
        return prodAproximada

    def insumosPorNombre(self, nombres):
        insumos = []
        for nombre in nombres:
            for insumo in self.listaInsumosBodega:
                if insumo.getNombre().lower() == nombre.lower():
                    insumos.append(insumo)
        return insumos

    def modistasQueHay(self) -> List[int]:
        modistasEnCadaSede = [0, 0]
        for empCreados in self.listaEmpleadosTotal:
            if empCreados.getAreaActual().getNombre().lower() == "corte":
                if empCreados.getSede().getNombre().lower() == "sede principal":
                    modistasEnCadaSede[0] += 1
                elif empCreados.getSede().getNombre().lower() == "sede 2":
                    modistasEnCadaSede[1] += 1
        return modistasEnCadaSede

    def prodTransferida1(self, fecha) -> List[int]:
        produccionSedes = self.calcProduccionSedes(fecha)
        return [produccionSedes[1][0], produccionSedes[1][1]]

    def prodTransferida2(self, fecha) -> List[int]:
        produccionSedes = self.calcProduccionSedes(fecha)
        return [produccionSedes[0][0], produccionSedes[0][1]]

    def planProduccion(self, maqDisponible: List, fecha: 'Fecha', scanner: 'int') -> List[List[List[int]]]:
        from .bodega.maquinaria import Maquinaria
        from src.uiMain import Main
        aProducirFinal = [], aProducir = [], listaEspera = [], listaDeCeros = [0, 0]
        listaEsperaVacia = [listaDeCeros.copy(), listaDeCeros.copy()]
        maqSedeP = [], maqSede2 = []
        senal = 0

        # Dividir las máquinas disponibles por sedes
        for todMaquinas in maqDisponible:
            if todMaquinas.getSede().getNombre().lower() == "sede principal":
                maqSedeP.append(todMaquinas)
            else:
                maqSede2.append(todMaquinas)

        # Dividir las máquinas de cada sede por función
        for todMaqSedeP in maqSedeP:
            if todMaqSedeP.esDeProduccion():
                Sede.getListaSedes()[0].maqProduccion.append(todMaqSedeP)
            else:
                Sede.getListaSedes()[0].maqOficina.append(todMaqSedeP)
        for todMaqSede2 in maqSede2:
            if todMaqSede2.esDeProduccion():
                Sede.getListaSedes()[1].maqProduccion.append(todMaqSede2)
            else:
                Sede.getListaSedes()[1].maqOficina.append(todMaqSede2)
        if len(Sede.getListaSedes()[0].maqProduccion) >= 3:
            senal = 5
        if len(Sede.getListaSedes()[1].maqProduccion) >= 3:
            senal += 10

        if senal == 5:
            Main.printsInt2(1)
            opcion = 0
            while opcion != 1 and opcion != 2:
                opcion = int(input())
                if opcion == 1:
                    aProducir.insert(0, self.prodSedeP(fecha))
                    aProducir.insert(1, listaDeCeros)
                    aProducirFinal.insert(0, aProducir)
                    aProducirFinal.insert(1, listaEsperaVacia)
                elif opcion == 2:
                    aProducir.insert(0, self.calcProduccionSedes(fecha)[0])
                    aProducir.insert(1, listaDeCeros)
                    listaEspera.insert(0, self.prodTransferida1(fecha))
                    listaEspera.insert(1, listaDeCeros)
                    aProducirFinal.insert(0, aProducir)
                    aProducirFinal.insert(1, listaEspera)
                else:
                    Main.printsInt2(2)

        elif senal == 10:
            Main.printsInt2(3)
            opcion = 0
            while opcion != 1 and opcion != 2:
                opcion = int(input())
                if opcion == 1:
                    # Producir todo en la sede 2
                    aProducir = [listaDeCeros.copy(), self.prodSede2(fecha)]
                    aProducirFinal = [aProducir, listaEsperaVacia]
                elif opcion == 2:
                    # Pasar producción a lista de espera
                    aProducir = [listaDeCeros.copy(), self.calcProduccionSedes(fecha)[1]]
                    listaEspera = [listaDeCeros.copy(), self.prodTransferida2(fecha)]
                    aProducirFinal = [aProducir, listaEspera]
                else:
                    Main.printsInt2(4)

        elif senal == 15:
            # Se produce todo entre las dos sedes
            senalRec = self.sobreCargada(fecha)
            if senalRec == 5:
                Main.printsInt2(5)
                opciom = 0
                while opciom not in [1, 2]:
                    opciom = int(input())
                    if opciom == 1:
                        nuevosPantP = self.calcProduccionSedes(fecha)[0][0] + -(- (self.calcProduccionSedes(fecha)[0][0] + self.calcProduccionSedes(fecha)[1][0]) // 2)
                        nuevosPant2 = self.calcProduccionSedes(fecha)[1][0] + ((self.calcProduccionSedes(fecha)[0][0] + self.calcProduccionSedes(fecha)[1][0]) // 2)
                        nuevasCamP = self.calcProduccionSedes(fecha)[0][1] + -(- (self.calcProduccionSedes(fecha)[0][1] + self.calcProduccionSedes(fecha)[1][1]) // 2)
                        nuevasCam2 = self.calcProduccionSedes(fecha)[1][1] + ((self.calcProduccionSedes(fecha)[0][1] + self.calcProduccionSedes(fecha)[1][1]) // 2)
                        loDeLaP = [nuevosPantP, nuevasCamP], loDeLa2 = [nuevosPant2, nuevasCam2], aProducir = [loDeLaP, loDeLa2], aProducirFinal = [aProducir, []]
                    elif opciom == 2:
                        aProducir = self.calcProduccionSedes(fecha)
                        aProducirFinal = [aProducir, []]
                    else:
                        Main.printsInt2(6)
            elif senalRec == 10:
                Main.printsInt2(7)
                opciom = 0
                while opciom not in [1, 2]:
                    opciom = int(input())
                    if opciom == 1:
                        nuevosPantP = self.calcProduccionSedes(fecha)[0][0] + ((self.calcProduccionSedes(fecha)[0][0] + self.calcProduccionSedes(fecha)[1][0]) // 2)
                        nuevosPant2 = self.calcProduccionSedes(fecha)[1][0] + -(- (self.calcProduccionSedes(fecha)[0][0] + self.calcProduccionSedes(fecha)[1][0]) // 2)
                        nuevasCamP = self.calcProduccionSedes(fecha)[0][1] + ((self.calcProduccionSedes(fecha)[0][1] + self.calcProduccionSedes(fecha)[1][1]) // 2)
                        nuevasCam2 = self.calcProduccionSedes(fecha)[1][1] + -(- (self.calcProduccionSedes(fecha)[1][1] + self.calcProduccionSedes(fecha)[0][1]) // 2)
                        loDeLaP = [nuevosPantP, nuevasCamP]
                        loDeLa2 = [nuevosPant2, nuevasCam2]
                        aProducir = [loDeLaP, loDeLa2]
                        aProducirFinal = [aProducir, []]
                    elif opciom == 2:
                        aProducir = self.calcProduccionSedes(fecha)
                        aProducirFinal = [aProducir, []]
                    else:
                        Main.printsInt2(8)
            elif senalRec == 15:
                Main.printsInt2(9)
                opciom = 0
                while opciom not in [1, 2]:
                    opciom = int(input())
                    if opciom == 1:
                        pSedePEspera = max(0, self.calcProduccionSedes(fecha)[0][0] - 10 * self.modistasQueHay()[0])
                        pSedeP = self.calcProduccionSedes(fecha)[0][0] - pSedePEspera
                        cSedePEspera = max(0, self.calcProduccionSedes(fecha)[0][1] - 10 * self.modistasQueHay()[0])
                        cSedeP = self.calcProduccionSedes(fecha)[0][1] - cSedePEspera
                        pSede2Espera = max(0, self.calcProduccionSedes(fecha)[1][0] - 10 * self.modistasQueHay()[1])
                        pSede2 = self.calcProduccionSedes(fecha)[1][0] - pSede2Espera
                        cSede2Espera = max(0, self.calcProduccionSedes(fecha)[1][1] - 10 * self.modistasQueHay()[1])
                        cSede2 = self.calcProduccionSedes(fecha)[1][1] - cSede2Espera
                        elGuardaPDeHoy = [pSedeP, cSedeP]
                        elGuarda2DeHoy = [pSede2, cSede2]
                        elGuardaPDeManana = [pSedePEspera, cSedePEspera]
                        elGuarda2DeManana = [pSede2Espera, cSede2Espera]
                        aProducir = [elGuardaPDeHoy, elGuarda2DeHoy]
                        listaEspera = [elGuardaPDeManana, elGuarda2DeManana]
                        aProducirFinal = [aProducir, listaEspera]
                    elif opciom == 2:
                        aProducir = self.calcProduccionSedes(fecha)
                        aProducirFinal = [aProducir, []]
                    else:
                        Main.printsInt2(10)
            elif senalRec == 0:
                aProducir = self.calcProduccionSedes(fecha)
                aProducirFinal = [aProducir, []]
        else:
            Main.printsInt2(11)
        return aProducirFinal

    @classmethod
    def sedeExiste(cls,nombre):
        for sede in cls.listaSedes:
            if sede.getNombre() == nombre:
                return True
        return False
    def getEmpleado(self, nombre):
        for empleado in self.listaEmpleado:
            if empleado.getNombre() == nombre:
                return empleado
        return None