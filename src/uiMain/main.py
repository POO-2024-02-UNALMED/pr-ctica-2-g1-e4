#region imports
import math
import random
from src.gestorAplicacion.administracion.banco import Banco
from src.gestorAplicacion.administracion.rol import Rol
from src.gestorAplicacion.bodega.bolsa import Bolsa
from src.gestorAplicacion.bodega.insumo import Insumo
from src.gestorAplicacion.bodega.prenda import Prenda
from src.gestorAplicacion.bodega.proveedor import Proveedor
from src.gestorAplicacion.fecha import Fecha
from src.gestorAplicacion.membresia import Membresia
from src.gestorAplicacion.venta import Venta
from src.gestorAplicacion.administracion.empleado import Empleado
from src.gestorAplicacion.administracion.deuda import Deuda
from ..gestorAplicacion.persona import Persona
from src.gestorAplicacion.sede import Sede
from src.gestorAplicacion.administracion.empleado import Empleado
from src.baseDatos.serializador import serializar
from src.baseDatos.deserializador import deserializar
import threading
#endregion

class Main:
    contadorBolsas=100
    fecha:Fecha=None
    proveedorBdelmain=None
    evento_ui = threading.Event()
    evento_ui2 = threading.Event()
    nuevoBalance=None
    diferenciaEstimado=0
    pesimismoPorSede = [2,2]
    listaErrores=[]
    def main():
        from src.gestorAplicacion.bodega.prenda import Prenda
        from src.gestorAplicacion.bodega.maquinaria import Maquinaria
        Main.fecha = Main.ingresarFechaConsola()
        print("Ecomoda a la orden")
        while True:
            print("\n¿Que operación desea realizar?")
            print("1. Despedir/Transferir/Contratar empleados")
            print("2. Adquirir insumos para la produccion")
            print("3, Ver el desglose economico de la empresa")
            print("4. Vender un producto")
            print("5. Producir prendas")
            print("6. Salir")
            
            opcion = Main.nextIntSeguro()
            if opcion == 1:
                pass
            elif opcion == 2:
                retorno = Main.planificarProduccion()
                lista_a = Main.coordinarBodegas(retorno)
                print(Main.comprarInsumos(lista_a))
            elif opcion == 3:
                balance_anterior = Main.calcularBalanceAnterior()
                diferencia_estimada = Main.calcularEstimado(balance_anterior)
                analisis_futuro = Main.planRecuperacion(diferencia_estimada)
                s1="\nSegún la evaluación del estado Financiero actual: " + "\n"+balance_anterior.Informe() 
                s2="\n\nSe realizó un análisis sobre la posibilidad de aplicar descuentos. \n"+ analisis_futuro
                s3="\n\nEste resultado se usó para estimar la diferencia entre ventas y deudas futuras, \nque fue de: $"+ diferencia_estimada
                s4=" y por tanto el nuevo porcentaje de pesimismo de la producción es:" + Venta.getPesimismo()+ "."
                retorna=s1+s2+s3+s4
                print(retorna)
            elif opcion == 4:
                venta = Main.vender()
                Main.realizarVenta(venta)
                Main.tarjetaRegalo(venta)
                sede = venta.getSede()
                Sede.getHistorialVentas().append(venta)
            elif opcion == 5:
                plan = Sede.planProduccion(Maquinaria.agruparMaquinasDisponibles(Main.fecha), Main.fecha)
                creadas = Prenda.producirPrendas(plan,Main.fecha)
                if (creadas):
                    print(Prenda.getCantidadUltimaProduccion()+" Prendas creadas con éxito")
                else:
                    print("No se pudo producir todo, los insumos no alcanzaron, producimos "+Prenda.getCantidadUltimaProduccion()+" prendas")
            #elif opcion == 6: #Serializador.serializar() #sys.exit(0)
            else:
                print("Esa opción no es valida.")
    
    @classmethod
    def ingresarFechaConsola(cls):
        dia = -1
        mes = -1
        while dia <= 0 or dia > 31:
            dia = int(input("Ingrese día: "))
            while mes <= 0 or mes > 12:
                mes = int(input("Ingrese mes: "))
        año = int(input("Ingrese año: "))
        fecha = Fecha(dia, mes, año)
        return fecha
    
    def  avisarFaltaDeInsumos(sede, fecha, tipo_prenda):
        from src.uiMain.F5Produccion import evento_senalizador
        from src.gestorAplicacion.bodega.prenda import Prenda
        print(f"No se pudo producir {tipo_prenda} en la sede {sede.getNombre()} por falta de insumos en la fecha {fecha}.")
        print(f"Hasta el momento se ha usado {Prenda.getCantidadTelaUltimaProduccion()} en tela.")
        #evento_senalizador.set()



    #region gestión humana
#------------------------------------------- Gestión Humana --------------------------------------------------------------------
    
    # Lo que siguen son para la versión grafica, o metodos puente para ella, y no usan print.-------------------------------

    despedidos=[] # Actualizado por la versión grafica de gestion humana
    porReemplazar=[]
    opcionesParaReemplazo=[] # Lista a elegir por cada rol


    # Metodos asistentes a la versión grafica de la interacción 1.
    @classmethod
    def listaInicialDespedirEmpleado(cls):
        return Empleado.listaInicialDespedirEmpleado(Main.fecha)

    @classmethod
    def despedirEmpleados(cls, nombres):
        empleados = []
        for nombre in nombres:
            encontrado=False
            for emp in Sede.getListaEmpleadosTotal():
                if emp.getNombre().lower() == nombre.lower():
                    empleados.append(emp)
                    encontrado=True
            if not encontrado:
                return (False,[])
                
        Empleado.despedirEmpleados(empleados, True, Main.fecha)
        cls.despedidos = empleados
        cls.porReemplazar = empleados.copy()
        return (True,empleados)

    @classmethod
    def verificarSedeExiste(cls, sede:str): # verifica que la sede exista
        return Sede.sedeExiste(sede)

    @classmethod
    def posiblesSedes(cls)->str:
        posiblesSedes="Posibles sedes:\n"
        for sede in Sede.getListaSedes():
            posiblesSedes+=sede.getNombre()+"\n"
        return posiblesSedes
    
    @classmethod    
    def sedePorNombre(cls,getNombre:str)->Sede:
        for sede in Sede.getListaSedes():
            if sede.getNombre().lower()==getNombre.lower():
                return sede
    
    # Usado para el recuadro de arriba de la interacción 1 grafica.
    @classmethod
    def mensajePromedioHumanas(cls):
        diferenciaSalarios = Persona.diferenciaSalarios()
        if diferenciaSalarios > 0:
            return f"Tus empleados estan {diferenciaSalarios:,} sobre el promedio de salarios"
        elif diferenciaSalarios < 0:
            return f"Tus empleados estan {-diferenciaSalarios:,} bajo el promedio de salarios"
        else:
            return "Tus empleados estan en el promedio de salarios"
    
    # Ejecutado al pasar a la interacción 2 grafica.
    @classmethod
    def prepararCambioSede(cls):
        nececidad = Sede.obtenerNecesidadTransferenciaEmpleados(Main.despedidos)
        cls.rolesAReemplazar = nececidad[0] if nececidad else []
        cls.transferirDe = nececidad[1] if nececidad else []
        cls.aContratar = nececidad[2] if nececidad else []
        cls.seleccion = []
        cls.idxRol = 0
        return cls.getTandaReemplazo()
    
    # Usado en interaccion 2 y 3 gráficas, pero cambia de donde se sacan las opciones.
    # Retorna una lista con : [Opciones para cambio, sede origen-> Solo aplica para cambio-sede, rol, cantidad a elegir]
    @classmethod
    def getTandaReemplazo(cls):
        cls.opcionesParaReemplazo = []
        if cls.idxRol < len(cls.rolesAReemplazar):
            sede=None
            cantidad=0
            rol = cls.rolesAReemplazar[cls.idxRol]
            if cls.estadoGestionHumana == "cambio-sede":
                sede = cls.transferirDe[cls.idxRol]
                for emp in sede.getListaEmpleados():
                    if emp.getRol() == rol:
                        cls.opcionesParaReemplazo.append(emp)
                cantidad = sum(1 for emp in Main.despedidos if emp.getRol() == rol)
                return cls.opcionesParaReemplazo, sede, rol, cantidad
            else:
                return cls.getTandaContratacion() # Hace lo mismo, pero no toma en cuenta la sede.
        else:
            return None
        
        
    # Avanza la interacción 2 y 3, cambiando de 2 a 3 cuando se han reemplazado todos los empleados posibles
    # Por cambio de sede.
    @classmethod
    def terminarTandaReemplazo(cls,reemplazos):
        empleadosReemplazadores = []
        for nombre in reemplazos:
            encontrado=False
            for emp in cls.opcionesParaReemplazo:
                if emp.getNombre().lower() == nombre.lower():
                    encontrado=True
                    empleadosReemplazadores.append(emp)
            if not encontrado:
                return False
        
        if cls.estadoGestionHumana == "cambio-sede":
            reemplazados=Sede.reemplazarPorCambioSede(Main.despedidos, empleadosReemplazadores)
            for emp in reemplazados:
                cls.porReemplazar.remove(emp)
        else:
            Persona.contratar(empleadosReemplazadores, cls.porReemplazar, Main.fecha)
            for emp in cls.porReemplazar:
                if emp.getRol() == cls.rolesAReemplazar[cls.idxRol]:
                    cls.porReemplazar.remove(emp)
        cls.idxRol+=1
        if cls.idxRol >= len(cls.rolesAReemplazar):
            cls.estadoGestionHumana="contratacion"
            cls.prepararContratacion()
        return True

    # Inicia interacción 3 grafica.
    @classmethod
    def prepararContratacion(cls):
        cls.aptosParaContratar, cls.rolesAReemplazar, cls.cantidadAContratar= Persona.entrevistar(cls.porReemplazar)
        cls.idxRol = 0

    # Usado antes de dibujar cada Tanda en interacción 3 grafica.
    
    @classmethod
    def getTandaContratacion(cls):
        cls.opcionesParaReemplazo=[]
        for apto in cls.aptosParaContratar:
            if apto.getRol()==cls.rolesAReemplazar[cls.idxRol]:
                cls.opcionesParaReemplazo.append(apto)
        return cls.opcionesParaReemplazo,None, cls.rolesAReemplazar[cls.idxRol], cls.cantidadAContratar[cls.idxRol]
#endregion

    #region financiera
#---------------------------------------------- Financiera ------------------------------------------------------------

    #Directivos disponibles
    def Directivos():
        from src.gestorAplicacion.administracion.area import Area
        from src.gestorAplicacion.sede import Sede
                
        elegible_empleados = []
        for empleado_actual in Sede.getListaEmpleadosTotal():
            if empleado_actual.getAreaActual() == Area.DIRECCION:
                elegible_empleados.append(empleado_actual.getNombre())
        return elegible_empleados
    
    #Interaccion 1    
    def calcularBalanceAnterior(empleado, eleccion):
        from src.gestorAplicacion.administracion.evaluacionFinanciera import EvaluacionFinanciera
        from src.gestorAplicacion.administracion.deuda import Deuda
        from src.gestorAplicacion.administracion.area import Area
        balanceCostosProduccion = Venta.calcularBalanceVentaProduccion(Main.fecha)
        deudaCalculada = Deuda.calcularDeudaMensual(Main.fecha, eleccion)
        balanceTotal = balanceCostosProduccion - deudaCalculada
        nuevoBalance = EvaluacionFinanciera(balanceTotal, empleado)
        Main.nuevoBalance=nuevoBalance
        return nuevoBalance
    
    # Interaccion 2 
    def calcularEstimado(porcentaje):
        from src.gestorAplicacion.administracion.evaluacionFinanciera import EvaluacionFinanciera
        diferenciaEstimado = EvaluacionFinanciera.estimadoVentasGastos(Main.fecha, porcentaje, Main.nuevoBalance)
        # Un mes se puede dar por salvado si el 80% de los gastos se pueden ver
        # cubiertos por las ventas predichas
        Main.diferenciaEstimado=diferenciaEstimado
        return diferenciaEstimado
    
    # Interacción 3
    def planRecuperacion(diferenciaEstimada, banco):
        from src.gestorAplicacion.bodega.prenda import Prenda
        from src.gestorAplicacion.administracion.deuda import Deuda
        bancos=Banco.getListaBancos()
        if diferenciaEstimada > 0:
            deudaPagada= Deuda.compararDeudas(Main.fecha)
            return deudaPagada
        else:
            cuotas = 0
            while cuotas <= 0 or cuotas > 18:
                Deuda.calcularCuotas(diferenciaEstimada)
            deudaAdquirir = Deuda(Main.fecha, diferenciaEstimada, banco, "Banco", cuotas)
            return deudaAdquirir
            
    def descuentosBlackFriday(descuento, nuevoDescuento):
        bfString = None
        if descuento <= 0.0:
            bfString = ("El análisis de ventas realizado sobre el Black Friday arrojó que la audiencia no reacciona tan bien a los descuentos, ""propusimos no hacer descuentos")
        else:
            bfString = ("El análisis de ventas realizado sobre el Black Friday arrojó que la audiencia reacciona bien a los descuentos, "f"propusimos un descuento del {descuento * 100}%")
        Prenda.prevenciones(descuento, nuevoDescuento, Main.fecha)
        analisisFuturo = (f"{bfString}, sin embargo su desición fue aplicar un descuento de: {nuevoDescuento * 100}%.")
        return analisisFuturo
#endregion

#region insumos
#-----------------------------------------------------------------Insumos------------------------------------------------------------------------------------
   
    insumosAConseguir = []# Modificado por planificarProduccion

    @classmethod
    def datosParaFieldPesimismo(cls):
        criterios=[]
        valores=[]
        for sede in Sede.getListaSedes():
            #prediccionC = None
            criterios.append(sede)
            valores.append(round(Venta.getPesimismo()*100))
        return (criterios,valores)


    # Interacción 1 
    @classmethod
    def planificarProduccion(cls,ventanaPrincipal,pesimismos): # pesimismos van de 0 a 100,y cambia la predicción en ese porcentaje
        from src.gestorAplicacion.bodega.pantalon import Pantalon
        from src.gestorAplicacion.bodega.camisa import Camisa
        fecha=Main.fecha
        criterios = []
        valores = []        
        retorno = []
        Main.texto = []
        cls.pesimismoPorSede = []
        for i in range(len(Sede.getListaSedes())):
            cls.pesimismoPorSede.append(float(pesimismos[i])/100)

        for idxSede,sede in enumerate(Sede.getListaSedes()):
            pantalonesPredichos = False
            camisasPredichas = False
            insumoXSede = []
            cantidadAPedir = []
            listaSede = [insumoXSede, cantidadAPedir]

            for prenda in Sede.getPrendasInventadas(sede):

                if isinstance(prenda, Pantalon) and not pantalonesPredichos:
                    proyeccion = Venta.predecirVentas(fecha, sede, prenda.getNombre())
                    prediccionP = proyeccion * (1 - cls.pesimismoPorSede[idxSede])
                    Main.texto.append(f"La predicción de ventas para {prenda} es de {math.ceil(prediccionP)} para la sede {sede}")
                    #startFrame.prediccion(self, texto)
                    for insumo in prenda.getInsumo():
                        insumoXSede.append(insumo)
                    for cantidad in Pantalon.getCantidadInsumo():
                        cantidadAPedir.append(math.ceil(cantidad * prediccionP))
                    pantalonesPredichos = True

                if isinstance(prenda, Camisa) and not camisasPredichas:
                    proyeccion = Venta.predecirVentas(fecha, sede, prenda.getNombre())
                    prediccionC = proyeccion * (1 - cls.pesimismoPorSede[idxSede])
                    Main.texto.append(f"La predicción de ventas para {prenda} es de {math.ceil(prediccionC)} para la sede {sede}")
                    #startFrame.prediccion(self, texto)
                    print(Main.texto)
                    for i, insumo in enumerate(prenda.getInsumo()):
                        cantidad = math.ceil(Camisa.getCantidadInsumo()[i] * prediccionC)
                        if insumo in insumoXSede:
                            index = insumoXSede.index(insumo)
                            cantidadAPedir[index] += cantidad
                        else:
                            insumoXSede.append(insumo)
                            cantidadAPedir.append(cantidad)
                    camisasPredichas = True

            retorno.append(listaSede)

        #startFrame.prediccion(self, Main.texto, Main.retorno)
        cls.planificarProduccion = retorno
        return retorno

    indexSedeCoordinarBodegas=0

    @classmethod
    def prepararCoordinacionBodegas(cls,ventanaPrincipal)->None:
        cls.infoTablaInsumos=[]
        cls.indexSedeCoordinarBodegas=0
        cls.planDeCompra=[]
        cls.productosOpcionTransferencia=[]
        
    productosOpcionTransferencia=[] # Generado en coordinarBodega
    # contine listas con indice 0 el insumo, indice 1 indice del insumo en la bodega, indice 2 sede donadora, indice 3 precio indice 4 cantidad faltante
    planDeCompra=[] # Generado en coordinarBodega
    infoTablaInsumos=[] # Lista de filas, cada una con insumo, cantidad en bodega,cantidad requerida, cantidad a conseguir y medio para conseguirlo.

    @classmethod
    def getSedeActualCoordinarBodegas(cls)->Sede:
        return Sede.getListaSedes()[cls.indexSedeCoordinarBodegas]

    @classmethod
    def getNombreSedeActualCoordinacion(cls)->str:
        return cls.getSedeActualCoordinarBodegas().getNombre()

    # Interacción 2 
    @classmethod
    def coordinarBodega(cls): # Antes coordinarBodegas
        insumoFieldFrame = []
        
        insumoFieldFrame.clear()
        insumosNecesarios = cls.planificarProduccion[cls.indexSedeCoordinarBodegas][0]
        cantidadesNecesarias = cls.planificarProduccion[cls.indexSedeCoordinarBodegas][1]

        s=Sede.getListaSedes()[cls.indexSedeCoordinarBodegas]

        cls.productosOpcionTransferencia.clear()

        productosAComprar = []
        cantidadesAComprar = []
        for i in insumosNecesarios:
            insumoFieldFrame.append(str(i) + f" ${Insumo.getPrecioIndividual(i)}")
            (hayEnBodega,indiceEnBodega) = Sede.verificarProductoBodega(i, s)
            idxInsumo = insumosNecesarios.index(i)
            filaTabla=[i.getNombre(),0,cantidadesNecesarias[idxInsumo],0]
            cantidadAConseguir=cantidadesNecesarias[idxInsumo]
            if hayEnBodega:
                cantidadEnBodega= Sede.getCantidadInsumosBodega(s)[indiceEnBodega]
                cantidadAConseguir= max(cantidadesNecesarias[idxInsumo] -cantidadEnBodega, 0)
                filaTabla[3]=cantidadAConseguir
                filaTabla[1]=cantidadEnBodega
            if cantidadAConseguir>0:
                productoEnOtraSede = Sede.verificarProductoOtraSede(i,cls.getSedeActualCoordinarBodegas())

                if productoEnOtraSede[0]:
                    cls.productosOpcionTransferencia.append([i, productoEnOtraSede[1], productoEnOtraSede[2], productoEnOtraSede[3],cantidadAConseguir])
                    filaTabla.append("Comprar o transferir")
                else:
                    productosAComprar.append(i)
                    cantidadesAComprar.append(cantidadAConseguir)
                    filaTabla.append("Comprar")
            else:
                filaTabla.append("¡Lo hay!")
            cls.infoTablaInsumos.append(filaTabla)
        cls.planDeCompra.append([productosAComprar, cantidadesAComprar])
        
    @classmethod
    def getCriteriosCoordinarBodegas(cls):
            criterios=[]
            for producto in cls.productosOpcionTransferencia:
                criterios.append(f"Transferir {producto[4]} {producto[0].getNombre()} de {Sede.getNombre(producto[2])}, o comprar por ${producto[3]}")
            return criterios

    @classmethod
    def siguienteSedeCoordinarBodegas(cls,respuestas)->bool:
        for idxRespuesta,respuesta in enumerate(respuestas):
            insumoTransferible:Insumo=cls.productosOpcionTransferencia[idxRespuesta][0]
            cantidad=cls.productosOpcionTransferencia[idxRespuesta][4]
            if respuesta.lower()=="c":
                cls.planDeCompra[cls.indexSedeCoordinarBodegas][0].append(insumoTransferible)
                cls.planDeCompra[cls.indexSedeCoordinarBodegas][1].append(cantidad)
            elif respuesta.lower()=="t":
                restante=Sede.transferirInsumo(insumoTransferible,cls.productosOpcionTransferencia[idxRespuesta][2],Sede.getListaSedes()[cls.indexSedeCoordinarBodegas],cantidad)
                if restante>0:
                    cls.planDeCompra[cls.indexSedeCoordinarBodegas][0].append(insumoTransferible)
                    cls.planDeCompra[cls.indexSedeCoordinarBodegas][1].append(restante)
        cls.infoTablaInsumos.clear()
        cls.productosOpcionTransferencia.clear()
        if cls.indexSedeCoordinarBodegas>=len(Sede.getListaSedes())-1:
            return False
        else:
            cls.indexSedeCoordinarBodegas+=1
            return True

    opcionesCompraExtra=[] # Generado en comprarInsumos. 1 lista por insumo
    # Cada 1 con indice 0 el insumo, indice 1 proveedor, indice 2 diferencial de precio, indice 3 sede compradora.
    deudas=[] # Generado en comprarInsumo

    extraPorComprar=[]

    # Interacción 3
    @classmethod
    def comprarInsumos(cls):
        from src.gestorAplicacion.bodega.proveedor import Proveedor
        from src.gestorAplicacion.administracion.deuda import Deuda
        cls.extraPorComprar = []
        for idxSede,sede in enumerate(cls.planDeCompra):
            insumos = sede[0]
            cantidad = sede[1]
            insumosPorComprarExtra=[]
            cantidadPorComprarExtra=[]
            quedanPorComprarSede=[insumosPorComprarExtra,cantidadPorComprarExtra]
            for idxInsumo in range(len(insumos)):
                mejorProveedor = None
                mejorPrecio = 0
                insumo:Insumo=insumos[idxInsumo]
                instanciaSede:Sede=Sede.getListaSedes()[idxSede]
                for proveedor in Proveedor.getListaProveedores():
                    if Proveedor.getInsumo(proveedor).getNombre() == insumos[idxInsumo].getNombre():
                        if proveedor.getPrecio() < mejorPrecio or mejorPrecio==0:
                            mejorProveedor = proveedor
                            mejorPrecio = proveedor.getPrecio()
                insumo.setProveedor(mejorProveedor)
                
                insumoEnBodega=instanciaSede.getListaInsumosBodega()[instanciaSede.encontrarInsumoEnBodega(insumo)]

                ultimoPrecio=insumoEnBodega.getUltimoPrecio()
                if mejorPrecio < ultimoPrecio:
                    diferencial =ultimoPrecio-mejorPrecio
                    cls.opcionesCompraExtra.append([insumos[idxInsumo], mejorProveedor.getNombre(), diferencial, instanciaSede.getNombre()])
                    insumosPorComprarExtra.append(insumos[idxInsumo])
                    cantidadPorComprarExtra.append(cantidad[idxInsumo])
                else:
                    cls.comprarInsumo(cantidad[idxInsumo], insumos[idxInsumo], mejorProveedor, Sede.getListaSedes()[idxSede])
            cls.extraPorComprar.append(quedanPorComprarSede)
        return cls.opcionesCompraExtra

    @classmethod
    def getNombresCompraExtra(cls):
        nombres=[]
        for opcion in cls.opcionesCompraExtra:
            nombres.append(opcion[0].getNombre())
        return nombres
    
    @classmethod
    def comprarInsumo(cls,cantidad:int,insumo:Insumo,proveedor:Proveedor,sede:Sede)->None:
        Sede.anadirInsumo(insumo, sede, cantidad)
        aEndeudarse=proveedor.costoPorCantidadInsumo(cantidad)
        if proveedor.getDeuda() is None:
            deuda = Deuda(cls.fecha, aEndeudarse, proveedor.getNombre, "Proveedor", Deuda.calcularCuotas(aEndeudarse))
        elif not proveedor.getDeuda().getEstadoDePago():
            proveedor.unificarDeudasXProveedor(cls.fecha, aEndeudarse)
            deuda = proveedor.getDeuda()
        insumoEnBodega:Insumo=sede.getListaInsumosBodega()[sede.encontrarInsumoEnBodega(insumo)]
        insumoEnBodega.setUltimoPrecio(Insumo.getPrecioIndividual(insumo))
        insumoEnBodega.setProveedor(proveedor)
        cls.deudas.append(deuda)
    #endregion

    def nextIntSeguro():
        while True:
            respuesta = input()
            if respuesta.isdigit():
                return int(respuesta)
            else:
                print("Por favor ingrese un número entero")

    @classmethod
    def dondeRetirar(cls):
        print("\n*Seleccione la sede desde donde comprara el Repuesto:\n")
        if Banco.getAhorroBanco(Sede.getCuentaSede(Sede.getListaSedes()[0])) >= Proveedor.getPrecio(Main.proveedorBdelmain):
            print(f"1. {Sede.getNombre(Sede.getListaSedes()[0])} tiene disponible: {Banco.getAhorroBanco(Sede.getCuentaSede(Sede.getListaSedes()[0]))}")
        if Banco.getAhorroBanco(Sede.getCuentaSede(Sede.getListaSedes()[1])) >= Proveedor.getPrecio(Main.proveedorBdelmain):
            print(f"2. {Sede.getNombre(Sede.getListaSedes()[1])} tiene disponible: {Banco.getAhorroBanco(Sede.getCuentaSede(Sede.getListaSedes()[1]))}")

        opcion = 0
        while opcion != 1 and opcion != 2:
            opcion = int(input())
            if opcion == 1:
                nuevoDineroSede = Banco.getAhorroBanco(Sede.getCuentaSede(Sede.getListaSedes()[1])) - Insumo.getPrecioIndividual(Proveedor.getInsumo(Main.proveedorBdelmain))
                Banco.getAhorroBanco(Sede.getCuentaSede(Sede.getListaSedes()[0]),nuevoDineroSede)
                print(f"El repuesto se compro exitosamente desde la {Sede.getNombre(Sede.getListaSedes()[0])}, saldo disponible:")
                print(f"{Sede.getNombre(Sede.getListaSedes()[0])} = {Banco.getAhorroBanco(Sede.getCuentaSede(Sede.getListaSedes()[0]))}")
                print(f"{Sede.getNombre(Sede.getListaSedes()[1])} = {Banco.getAhorroBanco(Sede.getCuentaSede(Sede.getListaSedes()[1]))}")
            elif opcion == 2:
                nuevoDineroSede = Banco.getAhorroBanco(Sede.getCuentaSede(Sede.getListaSedes()[1])) - Insumo.getPrecioIndividual(Proveedor.getInsumo(Main.proveedorBdelmain))
                Banco.setAhorroBanco(Sede.getCuentaSede(Sede.getListaSedes()[1]),nuevoDineroSede)
                print(f"El repuesto se compro exitosamente desde la sede {Sede.getNombre(Sede.getListaSedes()[1])}, saldo disponible:")
                print(f"{Sede.getNombre(Sede.getListaSedes()[0])} = {Banco.getAhorroBanco(Sede.getCuentaSede(Sede.getListaSedes()[0]))}")
                print(f"{Sede.getNombre(Sede.getListaSedes()[1])} = {Banco.getAhorroBanco(Sede.getCuentaSede(Sede.getListaSedes()[1]))}")
            else:
                print("Opcion incorrecta, marque 1 o 2 segun desee")

    @staticmethod
    def recibeProveedorB(proveedorB):
        Main.proveedorBdelmain = proveedorB

    @classmethod
    def retornaProveedorB(cls):
        return cls.proveedorBdelmain
    
    @classmethod
    def terminarCompraDeInsumos(cls,extra=None): # Extra es una lista de enteros con la cantidad extra de insumos a comprar
        if extra is not None:
            for idx ,  cantidad in enumerate(extra):
                sede = cls.sedePorNombre(cls.planDeCompra[idx][3])
                insumo = cls.planDeCompra[idx][0]
                proveedor = insumo.getProveedor()
                cls.extraPorComprar[Sede.getListaSedes().index(sede)][1]+=cantidad
        
        for idxSede, sede in enumerate(cls.extraPorComprar):
            for idx, insumo in enumerate(sede[0]):
                cls.comprarInsumo(sede[1][idx], insumo, insumo.getProveedor(), Sede.getListaSedes()[idxSede])

#region facturacion

    def listaVendedores(sede):
        from src.gestorAplicacion.administracion.area import Area
        listaEmpleado=[]
        for i, empleado in enumerate(sede.getListaEmpleados()):
            if Empleado.getAreaActual(empleado) == Area.OFICINA:
                listaEmpleado.append(empleado)
        return listaEmpleado

    def listaEncargados(sede):
        from src.gestorAplicacion.administracion.area import Area
        listaEmpleado=[]
        for i, empleado in enumerate(sede.getListaEmpleados()):
            if Empleado.getAreaActual(empleado) == Area.VENTAS:
                listaEmpleado.append(empleado)
        return listaEmpleado
#-----------------------------------------------------------------Facturación-----------------------------------------------------------------------------------

    def vender(cliente, sede, encargado, vendedor, productosSeleccionados, cantidadProductos):
        from ..gestorAplicacion.administracion.empleado import Empleado
        from src.gestorAplicacion.bodega.pantalon import Pantalon
        from src.gestorAplicacion.bodega.camisa import Camisa
        from src.gestorAplicacion.administracion.area import Area
        venta = None
        fechaVenta = Main.fecha
        costosEnvio = 0
        for i in range(len(productosSeleccionados)):
            cantidadPrenda= cantidadProductos[i]
            prendaSeleccionada = productosSeleccionados[i]
            cantidadDisponible = 0
            for prenda in Sede.getPrendasInventadasTotal():
                if(Prenda.getNombre(prenda)==Prenda.getNombre(prendaSeleccionada)):
                    cantidadDisponible+=1
            Main.manejarFaltantes(sede, cantidadPrenda, cantidadDisponible, prendaSeleccionada.getNombre(), costosEnvio)
            if 0 < cantidadPrenda < len(Sede.getPrendasInventadasTotal()):
                eliminadas = 0
                idxPrenda=0
                while idxPrenda<len(Sede.getPrendasInventadasTotal()):
                    if eliminadas >= cantidadPrenda:
                        break
                    if Sede.getPrendasInventadasTotal()[idxPrenda] == prendaSeleccionada:
                        eliminada = Sede.getPrendasInventadasTotal().pop(idxPrenda)
                        eliminadas += 1
                        i -= 1
                    idxPrenda += 1
        sumaPreciosPrendas = 0
        cantidadCamisas = 0
        cantidadPantalon = 0
        for prenda in productosSeleccionados:
            if isinstance(prenda, Camisa):
                sumaPreciosPrendas += Camisa.precioVenta()*cantidadProductos[productosSeleccionados.index(prenda)]
                cantidadCamisas += 1
                if cantidadCamisas >= 10:
                    descuento = int(sumaPreciosPrendas * 0.05)
                    sumaPreciosPrendas -= descuento
            elif isinstance(prenda, Pantalon):
                sumaPreciosPrendas += Pantalon.precioVenta()*cantidadProductos[productosSeleccionados.index(prenda)]
                cantidadPantalon += 1
                if cantidadPantalon >= 10:
                    descuento = int(sumaPreciosPrendas * 0.05)
                    sumaPreciosPrendas -= descuento
        IVA = int((costosEnvio + sumaPreciosPrendas) * 0.19)
        venta = Venta(sede, fechaVenta, cliente, vendedor, encargado, productosSeleccionados)
        venta.setCostoEnvio(costosEnvio)
        sumaPreciosPrendas += costosEnvio
        monto = sumaPreciosPrendas + IVA + costosEnvio
        montoPagar = int(monto - (monto * Membresia.getPorcentajeDescuento(Persona.getMembresia(cliente))))
        venta.setMontoPagado(montoPagar)
        venta.setSubtotal(sumaPreciosPrendas)
        comision = int(montoPagar * 0.05)
        Empleado.setRendimientoBonificacion(vendedor,comision)
        
        return venta 

    def imprimirNoEmpleados():
        from ..gestorAplicacion.administracion.empleado import Empleado
        noEmpleados = []
        for persona in Persona.getListaPersonas():
            if not isinstance(persona, Empleado):
                noEmpleados.append(persona)
        return noEmpleados

    def verificarBolsas(venta):
        from src.gestorAplicacion.bodega.proveedor import Proveedor
        productosSeleccionados = venta.getArticulos()
        sede = venta.getSede()
        totalPrendas = len(productosSeleccionados)
        insumosBodega = sede.getListaInsumosBodega()
        i=1
        bp, bm, bg = 0,0,0
        for i in range(len(insumosBodega)):
            bolsa = insumosBodega[i]
            if isinstance(bolsa, Bolsa):
                capacidad = bolsa.getCapacidadMaxima()
                cantidad = sede.getCantidadInsumosBodega()[i]
                if capacidad == 1 and cantidad > 0:
                    bp += cantidad
                if capacidad == 3 and cantidad > 0:
                    bm += cantidad
                if capacidad == 8 and cantidad > 0:
                    bg += cantidad
        return bp, bm, bg
        

    def cantidadActualBolsas(venta, cantidadBolsaGrande,cantidadBolsaMediana,cantidadBolsaPequeña):
        productosSeleccionados = venta.getArticulos()
        sede = venta.getSede()
        totalPrendas = len(productosSeleccionados)
        insumosBodega = sede.getListaInsumosBodega()
        tamañoListaInsumos = sede.getCantidadInsumosBodega()
        bolsasSeleccionadas = []
        capacidadTotal = 0
        bolsasAPedir=cantidadBolsaGrande+cantidadBolsaMediana+cantidadBolsaPequeña
        debeBolsas=0
        for i in range(bolsasAPedir):
            capacidadBolsa = 0
            if cantidadBolsaGrande > 0:
                capacidadBolsa = 8
                cantidadBolsaGrande -= 1
            elif cantidadBolsaMediana > 0:
                cantidadBolsaMediana -= 1
                capacidadBolsa = 3
            elif cantidadBolsaPequeña >0:
                capacidadBolsa = 1
                cantidadBolsaPequeña -= 1

            cantidadDisponible = 0
            capacidadTotal += capacidadBolsa
            tamañoListaInsumos=len(sede.getListaInsumosBodega())
            for i in range(tamañoListaInsumos):
                insumo = sede.getListaInsumosBodega()[i]
                if isinstance(insumo, Bolsa):
                    if insumo.getCapacidadMaxima() == capacidadBolsa:
                        cantidadInsumosBodega=sede.getCantidadInsumosBodega()
                        cantidadDisponible += cantidadInsumosBodega[i]
                        if cantidadDisponible > 0:
                            cantidadInsumosBodega[i] -= 1
                            break
    
        debeBolsas=max(totalPrendas-capacidadTotal,0)
        venta.getBolsas().append(bolsasSeleccionadas)
        totalVenta = venta.getMontoPagado() + len(bolsasSeleccionadas) * 2000
        venta.setMontoPagado(totalVenta)
        return debeBolsas        

    def surtirBolsas(ventana, venta,intento):
        from src.gestorAplicacion.bodega.proveedor import Proveedor
        nombreBolsa = "Bolsa"
        bolsaMenor=0
        revisarSede=venta.getSede()
        for i in range(len(revisarSede.getListaInsumosBodega())):
            insumo=revisarSede.getListaInsumosBodega()[i]
            if isinstance(insumo, Bolsa):
                if bolsaMenor==0:
                    bolsaMenor=revisarSede.getCantidadInsumosBodega()[i]
                elif  revisarSede.getCantidadInsumosBodega()[i]<=bolsaMenor:
                    bolsaMenor=revisarSede.getCantidadInsumosBodega()[i]
                    break
        listaInsumos = Sede.getListaInsumosBodega(insumo.getSede())
        if bolsaMenor < 10:
            mensaje=f"La sede {revisarSede.getNombre()} tiene menos de 10 bolsas en stock (Cantidad: {bolsaMenor})."
            for e in range(len(listaInsumos)):
                insumo = listaInsumos[e]
                if isinstance(insumo, Bolsa) and insumo.getNombre() == nombreBolsa:                   
                    ventana.modifInteraccion3Facturacion(insumo, mensaje)
        else:
            ventana.modifInteraccion3Facturacion(insumo, "No hay necesidad de comprar")
                            
    def comprarBolsas(ventana, venta, insumo, cantidadComprar):                      
        listaBolsas=[]
        mensaje=""
        nombreBolsa=insumo.getNombre()
        sede = venta.getSede()   
        cantidadInsumosBodega = sede.getCantidadInsumosBodega()     
        banco = sede.getCuentaSede()
        for revisarSede in Sede.getListaSedes():
            listaInsumos = Sede.getListaInsumosBodega(insumo.getSede())
            for e in range(len(listaInsumos)):
                    insumo = listaInsumos[e]    
                    if isinstance(insumo, Bolsa) and insumo.getNombre() == nombreBolsa:
                        costoCompra = Proveedor.costoDeLaCantidad(insumo, cantidadComprar)
                        banco.setAhorroBanco(Banco.getAhorroBanco(banco) - costoCompra)
                        cantidadInsumosBodega[e] += cantidadComprar
                        insumo.setPrecioCompra(costoCompra)
                        insumo.setPrecioCompra(costoCompra)
                        mensaje= (f"Se compraron {cantidadComprar} {nombreBolsa} por un costo total de {costoCompra}")
        return mensaje


    def manejarFaltantes(sede, cantidadPrenda, disponibles, tipoPrenda, costosEnvio):
        faltantes = cantidadPrenda - disponibles

        if faltantes > 0:
            costosEnvio += 3000 + (faltantes * 1000)
            prendasTransferidas = 0
            for otraSede in Sede.getListaSedes():
                if otraSede != sede:
                    for prenda in Sede.getPrendasInventadas(otraSede):
                        if Prenda.getNombre(prenda) == tipoPrenda and prendasTransferidas < faltantes:
                            Sede.getPrendasInventadas(otraSede).remove(prenda)
                            Sede.getPrendasInventadas(sede).append(prenda)
                            prendasTransferidas += 1

                    if prendasTransferidas == faltantes:
                        break

    def tarjetaRegalo(venta,codigoIngresado,respuesta,compraTarjeta,montoTarjeta):
        sede = Venta.getSede(venta)
        banco = Sede.getCuentaSede(sede)
        nuevoIntento = 1
        retorno=""
        while nuevoIntento == 1:
            if respuesta.lower() == "si":
                if codigoIngresado in Venta.getCodigosRegalo():
                    retorno+="Código válido. Procesando tarjeta de regalo..."
                    indice = Venta.getCodigosRegalo().index(codigoIngresado)
                    montoTarjeta = Venta.getMontosRegalo()[indice]
                    montoVenta = Venta.getMontoPagado(venta)

                    if montoTarjeta >= montoVenta:
                        retorno+="\nEl monto de la tarjeta cubre la totalidad de la venta."
                        saldoRestante = montoTarjeta - montoVenta
                        Venta.getMontosRegalo()[indice] = saldoRestante
                        Venta.setMontoPagado(venta,0)
                        retorno+="\nSaldo restante en la tarjeta de regalo: $" + str(saldoRestante)
                    else:
                        montoFaltante = montoVenta - montoTarjeta
                        Venta.getMontosRegalo()[indice] = 0
                        venta.setMontoPagado(montoFaltante)
                        retorno+="\nEl monto de la tarjeta no es suficiente para cubrir la venta."
                        retorno+="\nMonto restante a pagar: $" + str(montoFaltante)

                    if Venta.getMontosRegalo()[indice] == 0:
                        Venta.getCodigosRegalo().pop(indice)
                        Venta.getMontosRegalo().pop(indice)
                        retorno+="\nLa tarjeta de regalo se ha agotado y ha sido desactivada."

                    nuevoIntento = 2
                else:
                    retorno+="\nEl código ingresado no es válido. Por favor, intentar de nuevo o pagar el monto total"
                    #print("Ingresa 1 para intentar de nuevo.")
                    #print("Ingresa 2 para salir del intento")
                    #nuevoIntento = Main.nextIntSeguro()
                    
            elif respuesta.lower() == "no":
                nuevoIntento -= 1
                break

        if compraTarjeta.lower() == "si":
            codigoGenerado = Main.generarCodigoAleatorio()
            Venta.getCodigosRegalo().append(codigoGenerado)
            Venta.getMontosRegalo().append(montoTarjeta)
            Banco.setAhorroBanco(banco,Banco.getAhorroBanco(banco) + montoTarjeta)

            retorno+="\nTarjeta de regalo generada exitosamente."
            retorno+="\nCódigo: " + codigoGenerado
            retorno+="\nMonto: $" + str(montoTarjeta)
        return retorno
            
    def ingresoEmpresa(venta,transferirFondos,porcentaje):
        from src.gestorAplicacion.bodega.pantalon import Pantalon
        from src.gestorAplicacion.bodega.camisa import Camisa        
        sede = Venta.getSede(venta)
        banco = Sede.getCuentaSede(sede)
        ingreso = Venta.getMontoPagado(venta)
        mensaje="Ingreso calculado: $" + str(ingreso)
        mensajeFinal=""
        Banco.setAhorroBanco(banco, Banco.getAhorroBanco(banco) + ingreso)

        mensaje+="\nMonto total en la cuenta de la sede: $" + str(Banco.getAhorroBanco(banco))
        bancoRecibir = Banco.getCuentaPrincipal()
        bancoTransferir = Sede.getCuentaSede(sede)
        if bancoTransferir != bancoRecibir:
            if transferirFondos == "si":
                if porcentaje >= 20 or porcentaje <= 60:
                    montoTransferencia = (Banco.getAhorroBanco(bancoTransferir) * porcentaje / 100) - 50000
                    if montoTransferencia > 0:
                        if bancoRecibir.getNombreCuenta() == "principal":
                            bancoRecibir.setAhorroBanco(Banco.getAhorroBanco(bancoTransferir) - (montoTransferencia + 50000))
                            bancoRecibir.setAhorroBanco(bancoRecibir.getAhorroBanco() + montoTransferencia)
                            mensaje+="\nTransferencia exitosa. "
                            mensaje+="Monto transferido: $" + str(montoTransferencia)
                            mensaje+="\n Costo de transferencia: $50000"
                    else:
                        mensaje+="\nFondos insuficientes para cubrir la transferencia y el costo."
                else:
                    mensaje+="\nPorcentaje no válido. No se realizará la transferencia."
            else:
                mensaje+="\nNo se realizará la transferencia de fondos."
        if bancoTransferir is not None:
            mensaje+="\nEstado final de la cuenta de la sede: $" + str(Banco.getAhorroBanco(bancoTransferir))
        if bancoRecibir is not None:
            mensaje+="\nEstado final de la cuenta principal: $" + str(bancoRecibir.getAhorroBanco())
        productosSeleccionados = Venta.getArticulos(venta)
        montoPagar = Venta.getMontoPagado(venta)
        tasaIva = 0.19
        valorBase = int(montoPagar / (1 + tasaIva))
        iva = montoPagar - valorBase
        mensajeFinal+="\n---- FACTURA ----"
        mensajeFinal+="\nPrendas compradas:"
        cantidadCamisas = 0
        cantidadPantalon = 0
        subtotalCamisas = 0
        subtotalPantalon = 0

        for prenda in productosSeleccionados:
            if isinstance(prenda, Camisa):
                cantidadCamisas += 1
                subtotalCamisas += Camisa.precioVenta()
            if isinstance(prenda, Pantalon):
                cantidadPantalon += 1
                subtotalPantalon += Pantalon.precioVenta()

        camisaEncontrada = False
        pantalonEncontrado = False
        for prenda in productosSeleccionados:
            if isinstance(prenda, Camisa) and not camisaEncontrada:
                mensajeFinal+="\n"+prenda.getNombre() + " - Cantidad: " + str(cantidadCamisas) + " - Subtotal: $" + str(subtotalCamisas)
                camisaEncontrada = True
            if isinstance(prenda, Pantalon) and not pantalonEncontrado:
                mensajeFinal+="\n"+prenda.getNombre() + " - Cantidad: " + str(cantidadPantalon) + " - Subtotal: $" + str(subtotalPantalon)
                pantalonEncontrado = True

        mensajeFinal+="\n"+"Valor total a pagar: $" + str(montoPagar)
        mensajeFinal+="\n"+"Subtotal prendas: $" + str(Venta.getSubtotal(venta))
        mensajeFinal+="\n"+"IVA: $" + str(iva)
        mensajeFinal+="\n"+"Venta registrada por: " + Venta.getEncargado(venta).getNombre()
        mensajeFinal+="\n"+"Asesor de la compra: " + Venta.getAsesor(venta).getNombre()

        mensajeFinal+="\n""El monto total a pagar por parte del cliente es " + str(montoPagar) + " y el estado final de la cuenta de la sede es $" + str(Banco.getAhorroBanco(bancoTransferir))
        return mensajeFinal, mensaje
    
    def generarCodigoAleatorio():
        caracteres = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        while True:
            codigo = ''.join(random.choice(caracteres) for _ in range(8))
            if codigo not in Venta.getCodigosRegalo():
                return codigo

    def actualizarProveedores():
        from src.gestorAplicacion.bodega.proveedor import Proveedor
        sedeP = next((sede for sede in Sede.getListaSedes() if sede.getNombre() == "Sede Principal"), None)
        if sedeP:
            for insumo in sedeP.getListaInsumosBodega():
                compatibles = [prov for prov in Proveedor.getListaProveedores() if prov.getInsumo().getNombre() == insumo.getNombre()]
                nuevos = compatibles[:]
                random.shuffle(nuevos)
                for i, prov in enumerate(compatibles):
                    prov.setPrecio(nuevos[i].getPrecio())
    #endregion
    def pedirModista(cantidadPrendas, sede, idxTanda):
        from src.uiMain.F5Produccion import recibePrintModista, getIndexx
        printModista = None
        printModista = f"Seleccione el modista que se encargará de la tanda #{idxTanda} de producción de {cantidadPrendas} prendas en {sede.getNombre()}:"
        print(printModista)
        modistas = [empleado for empleado in sede.getListaEmpleados() if empleado.getRol() == Rol.MODISTA]
        recibePrintModista(printModista, modistas)
        Main.evento_ui.wait()
        print("\nestoy esperando a que me dejen pasar...\n")
        Main.evento_ui.clear()
        for i, modista in enumerate(modistas):
            print(f"{i}. {modista.getNombre()}")
        Main.evento_ui2.clear()
        print("\nesperando respuesta con el boton.....\n")
        Main.evento_ui2.wait()
        while True:
            seleccion = getIndexx() #metodo para traer de F5Produccion la senal, puede ser un getSenal(), definirlo en F5Produccion
            if 0 <= seleccion < len(modistas):
                return modistas[seleccion]
            else:
                print("Opción inválida. Intente nuevamente.")

    @classmethod
    def printsInt2(cls, senall):
        mensajes = {
            1: "Sede Principal disponible\nLa Sede 2 no puede trabajar por falta de maquinaria...",
            #2: "\n Marque una opcion correcta entre 1 o 2...\n",
            3: "Sede 2 disponible\nLa Sede Principal no puede trabajar por falta de maquinaria...",
            4: "\n Marque una opcion correcta entre 1 o 2...\n",
            5: "La Sede Principal esta sobrecargada, ¿Que desea hacer? \n1. Enviar parte de la produccion a la Sede 2, para producir por partes iguales.\n2. Ejecutar produccion, asumiendo todo el costo por sobrecarga en la Sede Principal.",
            #6: "Coloca una opcion indicada entre 1 o 2...",
            7: "La Sede 2 esta sobrecargada, ¿Que desea hacer? \n1. Enviar parte de la produccion a la Sede Principal, para producir por partes iguales.\n2. Ejecutar produccion, asumiendo todo el costo por sobrecarga en la Sede 2.",
            #8: "Coloca una opcion indicada entre 1 o 2...",
            #9: "Las dos sedes estan sobrecargadas, ¿Que quieres hacer?...\n1. Producir mañana las prendas que generan sobrecarga.\n2. Producir todo hoy, asumiendo el costo por sobrecarga.",
            10: "Seleccione una opcion indicada entre 1 o 2...",
            11: "\n Lo sentimos, se debe arreglar la maquinaria en alguna de las dos sedes para comenzar a producir...\n",
            
            12: "Las dos sedes están disponibles"
        }
        print(mensajes.get(senall, ""))
        return mensajes.get(senall)

    @classmethod
    def printsInt1(cls, signal, rep, maq, sede):
        if signal == 1:
            return f"{rep.getNombre()} se debe cambiar.\nMaquina afectada: {maq.getNombre()}  -  Sede afectada: {sede.getNombre()}"
        elif signal == 2:
            print(f"*El proveedor mas barato se llama '{cls.proveedorBdelmain.getNombre()}', y lo vende a: {cls.proveedorBdelmain.getPrecio()}\n")

    @classmethod
    def printsInt11(cls, rep, maq, sede, senal):
        if senal == 1:
            print(f"Repuesto: '{rep.getNombre()}' añadido correctamente a la {maq.getNombre()}, de la: {sede.getNombre()}")
        elif senal == 2:
            print("Ninguna de las sedes cuenta con dinero suficiente, considere pedir un prestamo.")
        elif senal == 3:
            print(f"\n--> Por ende, la {maq.getNombre()} de la {maq.getSede().getNombre()}, se encuentra inhabilitada.")
    
    @classmethod
    def printsInt111(cls, maq, senal):
        if senal == 4:
            print(f"\n--> La {maq.getNombre()} de la {maq.getSede().getNombre()} requiere mantenimiento.\n")

    def crearVentaAleatoria(deTantosProductos, aTantosProductos, fecha, asesor, encargado, cantidad, sede):
        from src.gestorAplicacion.bodega.pantalon import Pantalon
        from src.gestorAplicacion.bodega.camisa import Camisa
        for _ in range(cantidad):
            precio = 0
            costoEnvio = 0
            cantidadProductos = random.randint(deTantosProductos, aTantosProductos)
            articulos = []
            for _ in range(cantidadProductos):
                tipoProducto = random.randint(0, 1)
                if tipoProducto == 0:
                    producto = Camisa(fecha, asesor, False, True, sede, sede.insumosPorNombre(Camisa.getTipoInsumo()))
                    precio += 200_000
                    costoEnvio += 1_000
                    articulos.append(producto)
                elif tipoProducto == 1:
                    producto = Pantalon(fecha, asesor, False, True, sede, sede.insumosPorNombre(Pantalon.getTipoInsumo()))
                    precio += 200_000
                    costoEnvio += 1_000
                    articulos.append(producto)
            cliente = random.choice(Persona.getListaPersonas())
            venta = Venta(sede, fecha, cliente, asesor, encargado, articulos, precio, precio + costoEnvio)
            asesor.setRendimientoBonificacion(int(precio * 0.05))
            venta.setCostoEnvio(costoEnvio)

    @classmethod
    def crearSedesMaquinasRepuestos(cls):
        from ..gestorAplicacion.administracion.empleado import Empleado
        from src.gestorAplicacion.bodega.repuesto import Repuesto
        from src.gestorAplicacion.bodega.proveedor import Proveedor
        from src.gestorAplicacion.bodega.pantalon import Pantalon 
        from src.gestorAplicacion.bodega.maquinaria import Maquinaria
        from src.gestorAplicacion.bodega.camisa import Camisa
        from src.gestorAplicacion.administracion.evaluacionFinanciera import EvaluacionFinanciera
        from src.gestorAplicacion.administracion.deuda import Deuda    
        from src.gestorAplicacion.administracion.area import Area
        #Episodio 43
        p1 = Proveedor(600, "Rag Tela")
        p1.setInsumo(Insumo("Tela", p1))
        p2 = Proveedor(250, "Macro Telas")
        p2.setInsumo(Insumo("Hilo", p2))
        p4 = Proveedor(15000, "Insumos textileros")
        p4.setInsumo(Insumo("Cremallera", p4))
        p3 = Proveedor(200, "San Remo")
        p3.setInsumo(Insumo("Boton", p3))
        p5 = Proveedor(500, "Fatelares")
        p5.setInsumo(Insumo("Tela", p5))
        p6 = Proveedor(500, "Macro Textil")
        p6.setInsumo(Insumo("Tela", p6))
        p9 = Proveedor(300, "Hilos Venus")
        p9.setInsumo(Insumo("Hilo", p9))
        p7 = Proveedor(10000, "Insumos para Confección")
        p7.setInsumo(Insumo("Cremallera", p7))
        p8 = Proveedor(170, "InduBoton")
        p8.setInsumo(Insumo("Boton", p8))
        p10 = Proveedor(5000, "Primavera")
        p10.setDescuento(0.06)
        p10.setInsumo(Bolsa("Bolsa", p10))
        p11 = Proveedor(8000, "Empaques y Cartones")
        p11.setInsumo(Bolsa("Bolsa", p11))
        p11.setDescuento(0.1)
        p12 = Proveedor(6000, "Plastienda")
        p10.setDescuento(0.05)
        p12.setInsumo(Bolsa("Bolsa", p12))
        #PROVEEDORES QUE VENDEN AGUJAS DE LA MAQUINA DE COSER:
        p13 = Proveedor(80500, "Solo Agujas")
        p13.setInsumo(Insumo("Agujas de la Maquina de Coser", p13))
        p14 = Proveedor(92000, "Agujas y mas")
        p14.setInsumo(Insumo("Agujas de la Maquina de Coser", p14))
        p15 = Proveedor(70000, "Las propias agujas")
        p15.setInsumo(Insumo("Agujas de la Maquina de Coser", p15))
        p1.setDeuda(Deuda(Fecha(15, 1, 24), 500_000, p1.getNombre(), "Proveedor", 5))
        p2.setDeuda(Deuda(Fecha(15, 1, 24), 1_000_000, p2.getNombre(), "Proveedor", 10))
        # PROVEEDORES QUE VENDEN ACEITE:
        p16 = Proveedor(24000, "Aceites y mas")
        p16.setInsumo(Insumo("Aceite", p16))
        p17 = Proveedor(30000, "Aceitunas")
        p17.setInsumo(Insumo("Aceite", p17))
        p18 = Proveedor(20000, "El barato del Aceite")
        p18.setInsumo(Insumo("Aceite", p18))
        # PROVEEDORES QUE VENDEN CUCHILLAS
        p19 = Proveedor(32000, "El de las Cuchillas")
        p19.setInsumo(Insumo("Cuchillas", p19))
        p20 = Proveedor(28000, "El barato de las cuchillas")
        p20.setInsumo(Insumo("Cuchillas", p20))
        p21 = Proveedor(37000, "El carero de las cuchillas")
        p21.setInsumo(Insumo("Cuchillas", p21))
        # PROVEEDORES QUE VENDEN AFILADORES
        p22 = Proveedor(72000, "El afilador")
        p22.setInsumo(Insumo("Afiladores", p22))
        p23 = Proveedor(60000, "La bodega del afilador")
        p23.setInsumo(Insumo("Afiladores", p23))
        p24 = Proveedor(80000, "Afilamos caro")
        p24.setInsumo(Insumo("Afiladores", p24))
        # PROVEEDORES QUE VENDEN RESISTENCIAS ELECTRICAS:
        p25 = Proveedor(160000, "Resistencias y mas")
        p25.setInsumo(Insumo("Resistencia electrica", p25))
        p26 = Proveedor(140000, "Electricos")
        p26.setInsumo(Insumo("Resistencia electrica", p26))
        # PROVEEDORES QUE VENDEN MANGUERAS DE VAPOR:
        p27 = Proveedor(120000, "Mangueras y mas")
        p27.setInsumo(Insumo("Manguera de vapor", p27))
        p28 = Proveedor(140000, "Mangueras Don Diego")
        p28.setInsumo(Insumo("Manguera de vapor", p28))
        # PROVEEDORES QUE VENDEN AGUJAS DE LA BORDADORA INDUSTRIAL:
        p29 = Proveedor(55000, "El Agujero")
        p29.setInsumo(Insumo("Agujas de la Bordadora industrial", p29))
        p30 = Proveedor(45000, "La bodega del Agujero")
        p30.setInsumo(Insumo("Agujas de la Bordadora industrial", p30))
        # PROVEEDORES QUE VENDEN BANDAS DE TRANSMISION:
        p31 = Proveedor(200000, "El de las Bandas")
        p31.setInsumo(Insumo("Bandas de transmision", p31))
        p32 = Proveedor(250000, "El carero de las Bandas")
        p32.setInsumo(Insumo("Bandas de transmision", p32))
        # PROVEEDORES QUE VENDEN TINTA NEGRA PARA IMPRESORA:
        p33 = Proveedor(50000, "Tinta por aqui")
        p33.setInsumo(Insumo("Tinta Negra Impresora", p33))
        p34 = Proveedor(44000, "El tintoso")
        p34.setInsumo(Insumo("Tinta Negra Impresora", p34))
        # PROVEEDORES QUE VENDEN LECTORES DE BARRAS:
        p35 = Proveedor(120000, "Mega tecnologies")
        p35.setInsumo(Insumo("Lector de barras", p35))
        p36 = Proveedor(160000, "HP")
        p36.setInsumo(Insumo("Lector de barras", p36))
        # PROVEEDORES QUE VENDEN PAPEL QUIMICO:
        p37 = Proveedor(40000, "Panamericana")
        p37.setInsumo(Insumo("Papel quimico", p37))
        p38 = Proveedor(50000, "SSKaisen")
        p38.setInsumo(Insumo("Papel quimico", p38))
        # PROVEEDORES QUE VENDEN CARGADORES PARA PORTATILES:
        p39 = Proveedor(150000, "Homecenter")
        p39.setInsumo(Insumo("Cargador Computador", p39))
        p40 = Proveedor(180000, "Todo en cargadores")
        p40.setInsumo(Insumo("Cargador Computador", p40))
        # PROVEEDORES QUE VENDER MOUSE PARA PORTATILES:
        p41 = Proveedor(20000, "Mecado Libre")
        p41.setInsumo(Insumo("Mouse Computador", p41))
        p42 = Proveedor(30000, "Asus")
        p42.setInsumo(Insumo("Mouse Computador", p42))
        # CREACION DE TODOS LOS REPUESTOS QUE MANEJAREMOS PARA LA FUNCIONALIDAD
        # PRODUCCION
        AgujasMC = Repuesto("Agujas de la Maquina de coser", p13, 12)
        Aceite = Repuesto("Aceite", p16, 60, 1, None, 70)

        Cuchillas = Repuesto("Cuchillas", p19, 60)
        Afiladores = Repuesto("Afiladores", p22, 750)
        ResistenciaElectrica = Repuesto("Resistencia Electrica", p25, 1500)
        MangueraDeVapor = Repuesto("Manguera de Vapor", p27, 750, 1, None)
        AgujasBI = Repuesto("Agujas de la Bordadora Industrial", p29, 25)
        BandasDeTransmision = Repuesto("Bandas de Transmision", p31, 2500)
        TintaN = Repuesto("Tinta Negra Impresora", p33, 3000, 1, None, 3100)
        Lector = Repuesto("Lector de barras", p35, 3000)
        PapelQuimico = Repuesto("Papel quimico", p37, 72)
        Cargador = Repuesto("Cargador Computador", p39, 6000)
        Mouse = Repuesto("Mouse Computador", p41, 900, 1, None, 1000)

        # CREACION DE LAS SEDES QUE MANEJAREMOS, CON SUS RESPECTIVAS MAQUINAS EN CADA
        # UNA DE ELLAS
        sedeP = Sede("Sede Principal")
        sede2 = Sede("Sede 2")
        # AGRUPACION DE LOS REPUESTOS EN LISTAS PARA ENVIARLOS A LAS MAQUINAS
        # CORRESPONDIENTES
        repuestosMC = []; repuestosMCorte = []; repuestosPI = []; repuestosBI = []; repuestosMTermofijado = []; repuestosMTijereado = []; repuestosImp = []; repuestosRe = []; repuestosComp = []; repuestosMC2 = []; repuestosMCorte2 = []; repuestosPI2 = []; repuestosBI2 = []; repuestosMTermofijado2 = []; repuestosMTijereado2 = []; repuestosImp2 = []; repuestosRe2 = []; repuestosComp2 = []
        repuestosImp.append(TintaN)
        repuestosRe.append(PapelQuimico)
        repuestosRe.append(Lector)
        repuestosComp.append(Mouse)
        repuestosComp.append(Cargador)
        repuestosMC.append(AgujasMC)
        repuestosMC.append(Aceite)
        repuestosMCorte.append(Cuchillas)
        repuestosMCorte.append(Afiladores)
        repuestosPI.append(ResistenciaElectrica)
        repuestosPI.append(MangueraDeVapor)
        repuestosBI.append(AgujasBI)
        repuestosBI.append(Aceite.copiar())
        repuestosMTermofijado.append(BandasDeTransmision)
        repuestosMTermofijado.append(ResistenciaElectrica.copiar())
        repuestosMTijereado.append(Cuchillas.copiar())
        repuestosMTijereado.append(Aceite.copiar())
        # respuestos para las maquinas de la sede2
        repuestosImp2.append(TintaN.copiar())
        repuestosRe2.append(PapelQuimico.copiar())
        repuestosRe2.append(Lector.copiar())
        repuestosComp2.append(Mouse.copiar())
        repuestosComp2.append(Cargador.copiar())
        repuestosMC2.append(AgujasMC.copiar())
        repuestosMC2.append(Aceite.copiar())
        repuestosMCorte2.append(Cuchillas.copiar())
        repuestosMCorte2.append(Afiladores.copiar())
        repuestosPI2.append(ResistenciaElectrica.copiar())
        repuestosPI2.append(MangueraDeVapor.copiar())
        repuestosBI2.append(AgujasBI.copiar())
        repuestosBI2.append(Aceite.copiar())
        repuestosMTermofijado2.append(BandasDeTransmision.copiar())
        repuestosMTermofijado2.append(ResistenciaElectrica.copiar())
        repuestosMTijereado2.append(Cuchillas.copiar())
        repuestosMTijereado2.append(Aceite.copiar())

        # CREACION DE LAS MAQUINAS QUE MANEJAREMOS CON SUS RESPECTIVOS RESPUESTOS
        # sedeP
        MaquinaDeCoser = Maquinaria("Maquina de Coser Industrial", 4250000, 600, repuestosMC, sedeP)
        MaquinaDeCorte = Maquinaria("Maquina de Corte", 6000000, 700, repuestosMCorte, sedeP)
        PlanchaIndustrial = Maquinaria("Plancha Industrial", 2000000, 900, repuestosPI, sedeP)
        BordadoraIndustrial = Maquinaria("Bordadora Industrial", 31000000, 500, repuestosBI, sedeP, 501)
        #BordadoraIndustrial = Maquinaria("Bordadora Industrial", 31000000, 500, repuestosBI, sedeP)
        #BordadoraIndustrial.setHorasUso(501)
        
        MaquinaDeTermofijado = Maquinaria("Maquina de Termofijado", 20000000, 1000,repuestosMTermofijado, sedeP, 1001)
        #MaquinaDeTermofijado = Maquinaria("Maquina de Termofijado", 20000000, 1000,repuestosMTermofijado, sedeP)
        #MaquinaDeTermofijado.setHorasUso(101)
        MaquinaDeTijereado = Maquinaria("Maquina de Tijereado", 5000000, 600, repuestosMTijereado,sedeP)
        Impresora = Maquinaria("Impresora", 800000, 2000, repuestosImp, sedeP)
        Registradora = Maquinaria("Caja Registradora", 700000, 17000, repuestosRe, sedeP)
        Computador = Maquinaria("Computador", 2_000_000, 10000, repuestosComp, sedeP)

        # sede2
        MaquinaDeCoser2 = Maquinaria("Maquina de Coser Industrial", 4250000, 600, repuestosMC2, sede2)
        MaquinaDeCorte2 = Maquinaria("Maquina de Corte", 6000000, 700, repuestosMCorte2, sede2)
        PlanchaIndustrial2 = Maquinaria("Plancha Industrial", 2000000, 900, repuestosPI2, sede2, 901)
        #PlanchaIndustrial2 = Maquinaria("Plancha Industrial", 2000000, 900, repuestosPI2, sede2)
        #PlanchaIndustrial2.setHorasUso(901)
        BordadoraIndustrial2 = Maquinaria("Bordadora Industrial", 31000000, 500, repuestosBI2, sede2)
        MaquinaDeTermofijado2 = Maquinaria("Maquina de Termofijado", 20000000, 1000,repuestosMTermofijado2, sede2)
        MaquinaDeTijereado2 = Maquinaria("Maquina de Tijereado", 5000000, 600, repuestosMTijereado2,sede2)
        Impresora2 = Maquinaria("Impresora", 800000, 2000, repuestosImp2, sede2)
        Registradora2 = Maquinaria("Caja Registradora", 700000, 17000, repuestosRe2, sede2)
        Computador2 = Maquinaria("Computador", 2_000_000, 10000, repuestosComp2, sede2)

        bp = Banco("principal", "Banco Montreal",  4_000_000_000, 0.05)
        b1 = Banco("secundaria", "Banco Montreal", 5_000_000, 0.05)
        b3 = Banco("principal", "Bancolombia", 140_000_000, 0.09)
        b4 = Banco("principal", "Banco Davivienda", 80_000_000, 0.1)
        b2 = Banco("principal", "Banco de Bogotá", 125_000_000, 0.07)
        tm = Banco("principal", "Inversiones Terramoda", 160_000_000, 0.0)
        Banco.setCuentaPrincipal(bp)
        sede2.setCuentaSede(b1)
        sedeP.setCuentaSede(b4)

        d1 = Deuda(Fecha(15, 1, 20), 20_000_000, "Bancolombia", "Banco", 1)
        b3.actualizarDeuda(d1)
        d1.setEstadoDePago(True)
        d1.setCapitalPagado(20_000_000)
        d2 = Deuda(Fecha(15, 1, 20), 100_000_000, "Banco Montreal", "Banco", 18)
        d2.setCapitalPagado(100_000_000 / 2)
        b1.actualizarDeuda(d2)
        b2.actualizarDeuda(Deuda(Fecha(10, 1, 24), 5_000_000, "Banco de Bogotá", "Banco", 10))
        tm.actualizarDeuda(Deuda(Fecha(30, 9, 22), 150_000_000, "Inversiones Terramoda", "Banco", 18))
        tm.actualizarDeuda(Deuda(Fecha(20, 2, 23), 800_000, "Inversiones Terramoda", "Banco", 18))

        # Insumos de sede
        i1 = Insumo(nombre="Tela", proveedor=p5, cantidad=1 * 2_000, sede= sedeP)
        i2 = Insumo(nombre="Tela", proveedor=p5, cantidad=1 * 20_000,  sede=sede2)
        i3 = Insumo(nombre="Boton", proveedor=p3, cantidad=4 * 20_000, sede=sedeP)
        i4 = Insumo(nombre="Boton", proveedor=p3, cantidad=4 * 100, sede=sede2)
        i5 = Insumo(nombre="Cremallera", proveedor=p4, cantidad=1 * 20, sede=sedeP)
        i6 = Insumo(nombre="Cremallera", proveedor=p4, cantidad=1 * 20_000, sede=sede2)
        i7 = Insumo(nombre="Hilo", proveedor=p2, cantidad=100 * 20_000, sede=sedeP)
        i8 = Insumo(nombre="Hilo", proveedor=p2, cantidad=100 * 20_000, sede=sede2)
        i9 = Bolsa(nombre="Bolsa", proveedor=p10, cantidad=1 * 20, sede=sedeP, capacidadMaxima=8)
        i10 = Bolsa(nombre="Bolsa", proveedor=p10, cantidad=1 * 20, sede=sede2, capacidadMaxima=8)
        i11 = Bolsa(nombre="Bolsa", proveedor=p10, cantidad=1 * 20, sede=sedeP, capacidadMaxima=3)
        i12 = Bolsa(nombre="Bolsa", proveedor=p10, cantidad=1 * 20, sede=sede2, capacidadMaxima=3)
        i13 = Bolsa(nombre="Bolsa", proveedor=p10, cantidad=1 * 20, sede=sedeP, capacidadMaxima=1)
        i14 = Bolsa(nombre="Bolsa", proveedor=p10, cantidad=1 * 20, sede=sede2, capacidadMaxima=1)

        betty = Empleado(Area.DIRECCION, Fecha(1, 1, 23), sedeP, "Beatriz Pinzón", 4269292,Rol.PRESIDENTE, 10, Membresia.NULA, Computador)
        Armando = Empleado(Area.DIRECCION, Fecha(30, 11, 20), sedeP, "Armando Mendoza", 19121311,Rol.PRESIDENTE, 15, Membresia.PLATA, Computador.copiar())
        Cata = Empleado(Area.OFICINA, Fecha(1, 6, 16), sedeP, "Catalina Ángel", 7296957, Rol.ASISTENTE,20, Membresia.ORO, Impresora)
        Mario = (Empleado(Area.OFICINA, Fecha(30, 11, 20), sedeP, "Mario Calderón", 19256002,Rol.EJECUTIVO, 4, Membresia.PLATA, Impresora.copiar()))
        Hugo = (Empleado(Area.CORTE, Fecha(1, 5, 14), sedeP, "Hugo Lombardi", 7980705, Rol.DISEÑADOR,20, Membresia.ORO, MaquinaDeCorte))
        Inez = (Empleado(Area.CORTE, Fecha(1, 5, 14), sedeP, "Inez Ramirez", 23103023, Rol.MODISTA, 2,Membresia.NULA, MaquinaDeCoser))
        Aura = (Empleado(Area.VENTAS, Fecha(1, 2, 23), sedeP, "Aura Maria", 4146118, Rol.SECRETARIA, 2,Membresia.NULA, Registradora))
        Sandra = (Empleado(Area.CORTE, Fecha(15, 9, 23), sedeP, "Sandra Patiño", 5941859, Rol.MODISTA,5, Membresia.NULA, PlanchaIndustrial))
        Sofia = (Empleado(Area.CORTE, Fecha(30, 9, 22), sedeP, "Sofía Lopez", 5079239, Rol.MODISTA, 6,Membresia.NULA, MaquinaDeTermofijado))
        Mariana = (Empleado(Area.CORTE, Fecha(1, 5, 23), sedeP, "Mariana Valdéz", 4051807, Rol.MODISTA,10, Membresia.BRONCE, MaquinaDeTijereado))
        Bertha = (Empleado(Area.CORTE, Fecha(25, 2, 20), sedeP, "Bertha Muñoz", 7137741, Rol.MODISTA,15, Membresia.BRONCE, BordadoraIndustrial))
        Wilson = (Empleado(Area.VENTAS, Fecha(4, 4, 22), sedeP, "Wilson Sastoque", 9634927, Rol.PLANTA,5, Membresia.NULA, Registradora.copiar()))
        Gutierrez = (Empleado(Area.DIRECCION, Fecha(5, 8, 19), sede2, "Saul Gutierrez", 9557933,Rol.EJECUTIVO, 11, Membresia.NULA, Computador2))
        Marcela = (Empleado(Area.DIRECCION, Fecha(30, 11, 20), sede2, "Marcela Valencia", 8519803,Rol.EJECUTIVO, 10, Membresia.ORO, Computador2.copiar()))
        Gabriela = (Empleado(Area.VENTAS, Fecha(1, 1, 24), sede2, "Gabriela Garza", 5287925,Rol.VENDEDOR, 9, Membresia.PLATA, Registradora2))
        Patricia = (Empleado(Area.OFICINA, Fecha(5, 2, 23), sede2, "Patricia Fernandez", 4595311,Rol.SECRETARIA, 6, Membresia.BRONCE, Impresora2))
        Kenneth = (Empleado(Area.CORTE, Fecha(1, 1, 24), sede2, "Kenneth Johnson", 7494184,Rol.MODISTA, 8, Membresia.ORO, PlanchaIndustrial2))
        Robles = (Empleado(Area.OFICINA, Fecha(12, 10, 24), sede2, "Miguel Robles", 7518004,Rol.VENDEDOR, 7, Membresia.BRONCE, Impresora2.copiar()))
        Alejandra = (Empleado(Area.CORTE, Fecha(1, 2, 24), sede2, "Alejandra Zingg", 6840296,Rol.MODISTA, 2, Membresia.BRONCE, BordadoraIndustrial2))
        Cecilia = (Empleado(Area.CORTE, Fecha(1, 2, 23), sede2, "Cecilia Bolocco", 7443886,Rol.MODISTA, 10, Membresia.PLATA, MaquinaDeCoser2))
        Freddy = (Empleado(Area.VENTAS, Fecha(31, 1, 22), sede2, "Freddy Contreras", 6740561,Rol.PLANTA, 5, Membresia.NULA, Registradora2.copiar()))
        Adriana = (Empleado(Area.CORTE, Fecha(18, 6, 25), sede2, "Adriana arboleda", 5927947,Rol.MODISTA, 20, Membresia.ORO, MaquinaDeCorte2))
        Karina = (Empleado(Area.CORTE, Fecha(9, 3, 25), sede2, "Karina Larson", 5229381, Rol.MODISTA,2, Membresia.PLATA, MaquinaDeTermofijado2))
        Jenny = (Empleado(Area.CORTE, Fecha(1, 8, 24), sede2, "Jenny Garcia", 4264643, Rol.MODISTA, 1,Membresia.ORO, MaquinaDeTijereado2))
        ol = Empleado(Area.DIRECCION, Fecha(1, 2, 20), sede2, "Gustavo Olarte", 7470922, Rol.EJECUTIVO,3, Membresia.NULA, Computador2.copiar())
        ol.setTraslados(3)
        a = []
        a.append(Area.VENTAS)
        a.append(Area.OFICINA)
        ol.setAreas(a)
        EvaluacionFinanciera(-200_000, ol)
        EvaluacionFinanciera(-120_000, ol)
        EvaluacionFinanciera(-50_000, ol)
        EvaluacionFinanciera(1_000, ol)
        EvaluacionFinanciera(-70_000, ol)
        EvaluacionFinanciera(50_000_000, betty)
        EvaluacionFinanciera(1_000_000, betty)
        EvaluacionFinanciera(500_000, Armando)
        EvaluacionFinanciera(-10_000, Armando)
        EvaluacionFinanciera(100_000, Armando)
        c1 = Persona("Claudia Elena Vásquez", 5162307, Rol.MODISTA, 2, False, Membresia.BRONCE)
        c2 = Persona("Michel Doniel", 9458074, Rol.ASISTENTE, 4, False, Membresia.BRONCE)
        c3 = Persona("Claudia Bosch", 5975399, Rol.MODISTA, 4, False, Membresia.ORO)
        c4 = Persona("Mónica Agudelo", 8748155, Rol.MODISTA, 8, False, Membresia.ORO)
        c5 = Persona("Daniel Valencia", 9818534, Rol.EJECUTIVO, 10, False, Membresia.BRONCE)
        c6 = Persona("Efraín Rodriguez", 8256519, Rol.VENDEDOR, 10, False, Membresia.NULA)
        c7 = Persona("Mauricio Brightman", 8823954, Rol.PLANTA, 10, False, Membresia.ORO)
        c8 = Persona("Nicolás Mora", 4365567, Rol.EJECUTIVO, 8, False, Membresia.NULA)
        c9 = Persona("Roberto Mendoza", 28096740, Rol.PRESIDENTE, 2, False, Membresia.ORO)
        c10 = Persona("Hermes Pinzón", 21077781, Rol.ASISTENTE, 2, False, Membresia.NULA)
        c11 = Persona("Julia Solano", 28943158, Rol.SECRETARIA, 10, False, Membresia.BRONCE)
        c12 = Persona("Maria Beatriz Valencia", 6472799, Rol.ASISTENTE, 2, False, Membresia.BRONCE)
        c13 = Persona("Antonio Sanchéz", 8922998, Rol.VENDEDOR, 12, False, Membresia.NULA)
        c15 = Persona("Armando Paredes", 1212312, Rol.PLANTA, 1, False, Membresia.NULA)
        C16= Persona("Nuria Rendón", 1212312, Rol.PLANTA, 1, False, Membresia.NULA)
        tiposp = []; cantidadesp = [];tiposc = []; cantidadesc = []
        tiposp.append("Tela")
        tiposp.append("Boton")
        tiposp.append("Cremallera")
        tiposp.append("Hilo")
        cantidadesp.append(200)
        cantidadesp.append(1)
        cantidadesp.append(1)
        cantidadesp.append(300)
        tiposc.append("Tela")
        tiposc.append("Boton")
        tiposc.append("Hilo")
        cantidadesc.append(100)
        cantidadesc.append(3)
        cantidadesc.append(90)
        tiposca = []
        tiposca.append(i1)
        tiposca.append(i3)
        tiposca.append(i7)
        tiposcb = []
        tiposcb.append(i2)
        tiposcb.append(i4)
        tiposcb.append(i8)
        tipospa = []
        tipospa.append(i1)
        tipospa.append(i3)
        tipospa.append(i5)
        tipospa.append(i7)
        tipospb = []
        tipospb.append(i2)
        tipospb.append(i4)
        tipospb.append(i6)
        tipospb.append(i8)
        r1 = Pantalon(Fecha(1, 1, 23), Hugo, False, True, sedeP,tipospa)
        r2 = Pantalon(Fecha(1, 1, 23), Inez, False, True, sedeP,tipospa)
        r3 = Pantalon(Fecha(1, 1, 23), Sandra, False, True, sedeP,tipospa)
        r4 = Pantalon(Fecha(1, 1, 23), Sofia, False, True, sedeP,tipospa)
        r5 = Pantalon(Fecha(1, 1, 23), Mariana, False, True, sedeP,tipospa)
        r6 = Pantalon(Fecha(1, 1, 23), Bertha, False, True, sedeP,tipospa)
        r7 = Camisa(Fecha(1, 1, 23), Hugo, False, True, sedeP,tiposca)
        r8 = Camisa(Fecha(1, 1, 23), Inez, False, True, sedeP,tiposca)
        r9 = Camisa(Fecha(1, 1, 23), Sandra, False, True, sedeP,tiposca)
        r10 = Camisa(Fecha(1, 1, 23), Sofia, False, True, sedeP,tiposca)
        r11 = Camisa(Fecha(1, 1, 23), Mariana, False, True, sedeP,tiposca)
        r12 = Camisa(Fecha(1, 1, 23), Bertha, False, True, sedeP,tiposca)
        r13 = Pantalon(Fecha(1, 1, 23), Jenny, False, True, sede2,tipospb)
        r14 = Pantalon(Fecha(1, 1, 23), Karina, True, True, sede2,tipospb)
        r15 = Pantalon(Fecha(1, 1, 23), Adriana, False, True, sede2,tipospb)
        r16 = Pantalon(Fecha(1, 1, 23), Cecilia, False, True, sede2,tipospb)
        r17 = Pantalon(Fecha(1, 1, 23), Alejandra, False, True, sede2,tipospb)
        r18 = Pantalon(Fecha(1, 1, 23), Kenneth, False, True, sede2,tipospb)
        r19 = Camisa(Fecha(1, 1, 23), Jenny, False, True, sede2,tiposcb)
        r20 = Camisa(Fecha(1, 1, 23), Karina, True, True, sede2,tiposcb)
        r21 = Camisa(Fecha(1, 1, 23), Adriana, False, True, sede2,tiposcb)
        r22 = Camisa(Fecha(1, 1, 23), Cecilia, False, True, sede2,tiposcb)
        r23 = Camisa(Fecha(1, 1, 23), Alejandra, False, True, sede2,tiposcb)
        r24 = Camisa(Fecha(1, 1, 23), Kenneth, False, True, sede2,tiposcb)
        Karina.setPericia(0.1)
        ps1 = []
        ps1.append(r13)
        v1 = Venta(sede2, Fecha(28, 11, 24), c8, Gabriela, Patricia, ps1, 200000, 250000)
        v1.setCostoEnvio(20000)
        b1.setAhorroBanco(b1.getAhorroBanco() + 250000)
        com1 = round(250000 * 0.05)
        Gabriela.setRendimientoBonificacion(com1)
        ps2 = []
        ps2.append(r16)
        v2 = Venta(sede2, Fecha(29, 11, 24), c13, Freddy, Patricia, ps2, 300000, 350000)
        v2.setCostoEnvio(100000)
        b2.setAhorroBanco(b2.getAhorroBanco() + 350000)
        com2 = round(350000 * 0.05)
        Freddy.setRendimientoBonificacion(com2)
        ps3 = []
        ps3.append(r15)
        v3 = Venta(sede2, Fecha(29, 1, 25), c13, Freddy, Patricia, ps3, 300000, 350_000)
        v3.setCostoEnvio(100000)
        b3.setAhorroBanco(b2.getAhorroBanco() + 350000)
        com3 = round(350_000 * 0.05)
        Freddy.setRendimientoBonificacion(com3)
        ps4 = []
        ps4.append(r1)
        ps4.append(r2)
        v4 = Venta(sedeP, Fecha(30, 11, 24), c6, Aura, Cata, ps4, 300000, 350_000)
        v4.setCostoEnvio(100_000)
        b1.setAhorroBanco(b1.getAhorroBanco() + 350000)
        com4 = round(350000 * 0.05)
        Aura.setRendimientoBonificacion(com3)
        ps5 = []
        ps5.append(r7)
        v5 = Venta(sedeP, Fecha(30, 1, 25), c6, Aura, Cata, ps5, 300000, 350_000)
        v5.setCostoEnvio(100_000)
        b1.setAhorroBanco(b1.getAhorroBanco() + 350000)
        com5 = round(350000 * 0.05)
        Aura.setRendimientoBonificacion(com3)
        ps6 = []
        ps6.append(r15)
        ps6.append(r16)
        v6 = Venta(sedeP, Fecha(20, 2, 25), c4, Wilson, Mario, ps6, 400000, 600_000)
        v6.setCostoEnvio(100000)
        b3.setAhorroBanco(b3.getAhorroBanco() + 600000)
        com6 = round(600_000 * 0.05)
        Wilson.setRendimientoBonificacion(com6)
        maxProductos = 5
        minProductos = 1
        Main.crearVentaAleatoria(minProductos,maxProductos, Fecha(29,11,24), Aura, Cata, 300, sedeP)
        Main.crearVentaAleatoria(minProductos,1, Fecha(24,11,24), Aura, Mario, 300, sedeP)
        Main.crearVentaAleatoria(minProductos,maxProductos, Fecha(20,2,24), Aura, Cata, 600, sedeP)
        Main.crearVentaAleatoria(minProductos,maxProductos, Fecha(20,2,25), Aura, Mario, 600, sedeP)
        Main.crearVentaAleatoria(minProductos,maxProductos, Fecha(20,12,24), Aura, Cata, 700, sedeP)
        Main.crearVentaAleatoria(minProductos,maxProductos, Fecha(20,12,24), Aura, Mario, 700, sede2)
        Main.crearVentaAleatoria(minProductos,maxProductos, Fecha(20,1,25), Aura, Cata, 700, sede2)
        Main.crearVentaAleatoria(minProductos,maxProductos, Fecha(20,1,25), Aura, Mario, 700, sede2)
        Main.crearVentaAleatoria(minProductos,maxProductos, Fecha(20,1,25), Freddy,Patricia , 300, sede2)
        
        Main.fijarUltimoPrecioInicial()

    @classmethod
    def fijarUltimoPrecioInicial(cls):
        for sede in Sede.getListaSedes():
            for insumo in sede.getListaInsumosBodega():
                insumo.setUltimoPrecio(Proveedor.buscarPorNombreInsumo(insumo.getNombre()).getPrecio())
    
    @classmethod # Wrapper para uso de StartFrame
    def guardar(cls):
        serializar()

if __name__ == "__main__":
    print("Para usar la interfaz grafica, 1. Para usar la consola, 2. Para reiniciar los datos, 3")
    opcion="3"
    deserializarAlIniciar=True
    while opcion=="3":
        opcion = input()
        match opcion:
            case "1":
                from src.uiMain.bienvenida.bienvenida import Bienvenida
                if deserializarAlIniciar:
                    deserializar()
                Bienvenida.bienvenida()
            case "2":
                if deserializarAlIniciar:
                    deserializar()
                Main.main()
            case "3":
                Main.crearSedesMaquinasRepuestos()
                serializar()
                deserializarAlIniciar=False