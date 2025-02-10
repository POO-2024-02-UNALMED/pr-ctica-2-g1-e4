from src.gestorAplicacion.administracion.resultado import Resultado
from src.gestorAplicacion.administracion.rol import Rol
from src.gestorAplicacion.bodega.insumo import Insumo
from .administracion.area import Area
from .fecha import Fecha
from .venta import Venta
from .bodega.maquinaria import Maquinaria
from typing import List

class Sede:
    prendasInventadasTotal=[]
    listaEmpleadosTotal=[]
    listaSedes=[]
    evaluacionesFinancieras=[]
    
    def __init__(self, nombre="Sede"):
        self.listaEmpleado=[]
        self.listaMaquina=[]
        self.historialVentas=[]
        self.prendasInventadas=[]
        self.listaInsumosBodega=[]
        self.cantidadInsumosBodega=[]
        self.produccionAproximada=[]
        self.prendasProduccion=[]
        self.nombre=nombre
        self.cuentaSede=None
        self.maqProduccion = []
        self.maqOficina = []
        Sede.setListaSedes(self)

    @classmethod
    def verificarProductoBodega(cls,insumo, sede):
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
    def transferirInsumo(cls,insumo,  donadora, beneficiaria, cantidadSolicitada):
        restante = 0
        idxInsumo =  donadora.listaInsumosBodega.index(insumo)

        if idxInsumo == -1:
            return cantidadSolicitada  # Skip the rest of the method, because there is nothing to transfer.

        cantidadDisponible = min( donadora.cantidadInsumosBodega.index(idxInsumo), cantidadSolicitada)
        ajusteStock = Insumo.getPrecioStockTotal() - (insumo.getPrecioIndividual() * cantidadSolicitada)
        Insumo.setPrecioStockTotal(ajusteStock)

        if (cantidadDisponible - cantidadSolicitada) == 0:
             donadora.cantidadInsumosBodega[idxInsumo] = 0
            
        elif (cantidadDisponible - cantidadSolicitada) < 0:
            restante = (cantidadDisponible - cantidadSolicitada) * -1
            donadora.cantidadInsumosBodega[idxInsumo] = 0
            
        else:
             donadora.cantidadInsumosBodega[idxInsumo] = (cantidadDisponible - cantidadSolicitada)

        cls.añadirInsumo(insumo, beneficiaria, cantidadSolicitada - cantidadDisponible)
        return restante

    @classmethod
    def añadirInsumo(cls,insumo, sede, cantidad):
        for idxInsumoEnBOdega in range(len(sede.getListaInsumosBodega())):
            if insumo == sede.getListaInsumosBodega()[idxInsumoEnBOdega]:
                cantidad_actual = sede.get_cantidad_insumos_bodega()[idxInsumoEnBOdega]
                sede.cantidadInsumosBodega[idxInsumoEnBOdega] = cantidad_actual + cantidad
                ajuste_stock = Insumo.getPrecioStockTotal() + (insumo.getPrecioIndividual() * cantidad)
                Insumo.setPrecioStockTotal(ajuste_stock)
    @classmethod
    def verificar_producto_otra_sede(cls,insumo):
        retorno = False
        index = -1
        sede_a_transferir = None
        precio = 0

        for sede in cls.listaSedes:
            for x in range(len(sede.getListaInsumosBodega())):
                if insumo == sede.getListaInsumosBodega()[x]:
                    for cantidad in sede.cantidadInsumosBodega:
                        if sede.getCantidadInsumosBodega()[x] != 0:
                            index = x
                            retorno = True
                            sede_a_transferir = sede
                            precio = insumo.getPrecioCompra()
                            break

        resultado = Resultado(retorno, index, sede_a_transferir, precio)
        return resultado

    def actualizarHistorialVentas(self,venta):
        self.historialVentas.add(venta)
        pass
    
    def getRendimientoDeseado(self,area,fecha):
        Area.rendimientoDeseadoActual(self,fecha)
        return area.rendimiento_deseado
    
    @classmethod
    def setListaSedes(cls,sede):
       cls.listaSedes.append(sede)
 
    @staticmethod
    def getListaSedes():
        return Sede.listaSedes

    def getListaEmpleados(self):
        # Placeholder for actual implementation
        return self.listaEmpleados

    def setlistaEmpleados(self,Emp):
        self.listaEmpleado = Emp

    def getlistaMaquinas(self):
        return self.listaMaquina

    def setlistaMaquinas(self,Maquinaria):
        self.listaMaquina = Maquinaria

    def getHistorialVentas(self):
        return self.historialVentas

    def setHistorialVentas(self,venta):
        self.historialVentas = venta

    def getPrendasInventadas(self):
        return self.prendasInventadas

    def setPrendasInventadas(self, prenda):
        self.prendasInventadas = prenda

    def getListaInsumosBodega(self):
        return self.listaInsumosBodega

    def setlistaInsumosBodega (self,Insumos):
        self.listaInsumosBodega = Insumos

    def getCantidadInsumosBodega(self,):
        return self.cantidadInsumosBodega

    def setCantidadInsumosBodega(self,CantidadIns):
        self.cantidadInsumosBodega = CantidadIns

    def getProduccionAproximada(self):
        return self.produccionAproximada

    def setProduccionAproximada(self,produccion):
        self.produccionAproximada = produccion

    def etPrendasProduccion(self):
        return self.prendasProduccion

    def setPrendasProduccion(self,Prendasp):
        self.prendasProduccion = Prendasp

    def getNombre(self):
        return self.nombre

    def setNombre(self, nombre):
        self.nombre = nombre

    def setCuentaSede(self, cuenta):
        self.cuentaSede = cuenta

    def getCuentaSede(self):
        return self.cuentaSede

    def anadirEmpleado(self, emp):
        self.listaEmpleado.add(emp)

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
    def setListaEmpleadosTotal(cls,empleados):
        cls.listaEmpleadosTotal = empleados  # Para serializacion

    @classmethod
    def getPrendasInventadasTotal(cls):
        return cls.prendasInventadasTotal

    @classmethod
    def setPrendasInventadasTotal(cls,prendas):
        cls.prendasInventadasTotal = prendas  # Para serializacion

    def getProdAproximada(self):
        return self.prodAproximada


    def obtenerNececidadTransferenciaEmpleados(despedidos):  # Despedidos es A en el doc.
        roles_a_revisar = []
        sede_origen = []
        
        for empleado in despedidos:
            if empleado.getRol() not in roles_a_revisar:
                roles_a_revisar.append(empleado.getRol())
                sede_origen.append(empleado.getSede())
        
        transferir_de = []
        roles_a_transferir = []

        for idx_rol in range(len(roles_a_revisar)):
            rol = roles_a_revisar[idx_rol]

            # Revisar sedes donadoras
            for sede in Sede.listaSedes:
                if sede == sede_origen[idx_rol]:
                    continue  # Evitar donacion de la misma sede de origen.
                
                if rol == Rol.MODISTA:
                    if sede.cantidadPorRol(rol) != 0:
                        produccion_total = sum(sede.getProduccionAproximada())
                        produccion_por_modista = produccion_total / sede.cantidadPorRol(rol)

                        if produccion_por_modista < 30:
                            transferir_de.append(sede)
                            roles_a_transferir.append(rol)
                            break  # Salir de la revisión de sedes donadoras
                
                elif rol == Rol.SECRETARIA:
                    ejecutivos = sede.cantidadPorRol(Rol.EJECUTIVO)
                    secretarias = sede.cantidadPorRol(Rol.SECRETARIA)
                    empleados = len(sede.lista_empleado)
                    if not (empleados / secretarias > 18 or ejecutivos / secretarias > 2):
                        transferir_de[idx_rol] = sede
                        roles_a_transferir.append(rol)
                        break  # Salir de la revisión de sedes donadoras

        retorno = []
        retorno.append(roles_a_transferir)
        retorno.append(transferir_de)

        a_reemplazar = despedidos.copy()
        for empleado in despedidos:
            if empleado.getRol() in roles_a_transferir:
                a_reemplazar.remove(empleado)

        retorno.append(a_reemplazar)
        return retorno

    def reemplazarPorCambioSede(despedidos, a_transferir):
        for empleado_despedido in despedidos:
            # Buscamos en la lista de empleados a transferir, quien pudo ser seleccionado como reemplazo.
            for empleado_reemplazo in a_transferir:
                if empleado_despedido.getRol() == empleado_reemplazo.getRol():
                    remuneracion_a_pagar = Maquinaria.remuneracionDanos(empleado_reemplazo)
                    empleado_reemplazo.modificarBonificacion(remuneracion_a_pagar * -1)
                    empleado_reemplazo.setSede(empleado_despedido.get_sede())
                    Maquinaria.asignarMaquinaria(empleado_reemplazo)
                    a_transferir.remove(empleado_reemplazo)
                    break

        if senal == 5:
            Main.prints_int_2(1)
            opcion = 0
            while opcion != 1 and opcion != 2:
                opcion = int(input())
                if opcion == 1:
                    a_producir.insert(0, self.prod_sede_p(fecha))
                    a_producir.insert(1, lista_de_ceros)

                    a_producir_final.insert(0, a_producir)
                    a_producir_final.insert(1, lista_espera_vacia)
                elif opcion == 2:
                    a_producir.insert(0, self.calc_produccion_sedes(fecha)[0])
                    a_producir.insert(1, lista_de_ceros)

                    lista_espera.insert(0, self.prod_transferida1(fecha))
                    lista_espera.insert(1, lista_de_ceros)

                    a_producir_final.insert(0, a_producir)
                    a_producir_final.insert(1, lista_espera)
                else:
                    Main.prints_int_2(2)
        
        elif senal == 10:
            Main.prints_int2(3)

            opcion = 0
            while opcion != 1 and opcion != 2:
                opcion = int(input())

                if opcion == 1:
                    # Producir todo en la sede 2
                    a_producir = [lista_de_ceros.copy(), self.prod_sede2(fecha)]
                    a_producir_final = [a_producir, lista_espera_vacia]

                elif opcion == 2:
                    # Pasar producción a lista de espera
                    a_producir = [lista_de_ceros.copy(), self.calc_produccion_sedes(fecha)[1]]
                    lista_espera = [lista_de_ceros.copy(), self.prod_transferida2(fecha)]
                    a_producir_final = [a_producir, lista_espera]

                else:
                    Main.prints_int2(4)

        elif senal == 15:
            # Se produce todo entre las dos sedes
            senal_rec = self.sobre_cargada(fecha)

            if senal_rec == 5:
                Main.prints_int2(5)

                opciom = 0
                while opciom not in [1, 2]:
                    opciom = int(input())

                    if opciom == 1:
                        nuevos_pant_p = self.calc_produccion_sedes(fecha)[0][0] + -(- (self.calc_produccion_sedes(fecha)[0][0] + self.calc_produccion_sedes(fecha)[1][0]) // 2)
                        nuevos_pant_2 = self.calc_produccion_sedes(fecha)[1][0] + ((self.calc_produccion_sedes(fecha)[0][0] + self.calc_produccion_sedes(fecha)[1][0]) // 2)

                        nuevas_cam_p = self.calc_produccion_sedes(fecha)[0][1] + -(- (self.calc_produccion_sedes(fecha)[0][1] + self.calc_produccion_sedes(fecha)[1][1]) // 2)
                        nuevas_cam_2 = self.calc_produccion_sedes(fecha)[1][1] + ((self.calc_produccion_sedes(fecha)[0][1] + self.calc_produccion_sedes(fecha)[1][1]) // 2)

                        lo_de_la_p = [nuevos_pant_p, nuevas_cam_p]
                        lo_de_la_2 = [nuevos_pant_2, nuevas_cam_2]

                        a_producir = [lo_de_la_p, lo_de_la_2]
                        a_producir_final = [a_producir, []]

                    elif opciom == 2:
                        a_producir = self.calc_produccion_sedes(fecha)
                        a_producir_final = [a_producir, []]

                    else:
                        Main.prints_int2(6)

            elif senal_rec == 10:
                Main.prints_int2(7)

                opciom = 0
                while opciom not in [1, 2]:
                    opciom = int(input())

                    if opciom == 1:
                        nuevos_pant_p = self.calc_produccion_sedes(fecha)[0][0] + ((self.calc_produccion_sedes(fecha)[0][0] + self.calc_produccion_sedes(fecha)[1][0]) // 2)
                        nuevos_pant_2 = self.calc_produccion_sedes(fecha)[1][0] + -(- (self.calc_produccion_sedes(fecha)[0][0] + self.calc_produccion_sedes(fecha)[1][0]) // 2)

                        nuevas_cam_p = self.calc_produccion_sedes(fecha)[0][1] + ((self.calc_produccion_sedes(fecha)[0][1] + self.calc_produccion_sedes(fecha)[1][1]) // 2)
                        nuevas_cam_2 = self.calc_produccion_sedes(fecha)[1][1] + -(- (self.calc_produccion_sedes(fecha)[1][1] + self.calc_produccion_sedes(fecha)[0][1]) // 2)

                        lo_de_la_p = [nuevos_pant_p, nuevas_cam_p]
                        lo_de_la_2 = [nuevos_pant_2, nuevas_cam_2]

                        a_producir = [lo_de_la_p, lo_de_la_2]
                        a_producir_final = [a_producir, []]

                    elif opciom == 2:
                        a_producir = self.calc_produccion_sedes(fecha)
                        a_producir_final = [a_producir, []]

                    else:
                        Main.prints_int2(8)

            elif senal_rec == 15:
                Main.prints_int2(9)

                opciom = 0
                while opciom not in [1, 2]:
                    opciom = int(input())

                    if opciom == 1:
                        p_sede_p_espera = max(0, self.calc_produccion_sedes(fecha)[0][0] - 10 * self.modistasQueHay()[0])
                        p_sede_p = self.calc_produccion_sedes(fecha)[0][0] - p_sede_p_espera

                        c_sede_p_espera = max(0, self.calc_produccion_sedes(fecha)[0][1] - 10 * self.modistasQueHay()[0])
                        c_sede_p = self.calc_produccion_sedes(fecha)[0][1] - c_sede_p_espera

                        p_sede_2_espera = max(0, self.calc_produccion_sedes(fecha)[1][0] - 10 * self.modistasQueHay()[1])
                        p_sede_2 = self.calc_produccion_sedes(fecha)[1][0] - p_sede_2_espera

                        c_sede_2_espera = max(0, self.calc_produccion_sedes(fecha)[1][1] - 10 * self.modistasQueHay()[1])
                        c_sede_2 = self.calc_produccion_sedes(fecha)[1][1] - c_sede_2_espera

                        el_guarda_p_de_hoy = [p_sede_p, c_sede_p]
                        el_guarda_2_de_hoy = [p_sede_2, c_sede_2]
                        el_guarda_p_de_manana = [p_sede_p_espera, c_sede_p_espera]
                        el_guarda_2_de_manana = [p_sede_2_espera, c_sede_2_espera]

                        a_producir = [el_guarda_p_de_hoy, el_guarda_2_de_hoy]
                        lista_espera = [el_guarda_p_de_manana, el_guarda_2_de_manana]
                        a_producir_final = [a_producir, lista_espera]

                    elif opciom == 2:
                        a_producir = self.calc_produccion_sedes(fecha)
                        a_producir_final = [a_producir, []]

                    else:
                        Main.prints_int2(10)

            elif senal_rec == 0:
                a_producir = self.calc_produccion_sedes(fecha)
                a_producir_final = [a_producir, []]

        else:
            Main.prints_int2(11)

        return a_producir_final

    