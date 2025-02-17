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
from src.uiMain.F2Insumos import F2Insumos
from ..gestorAplicacion.persona import Persona
from src.gestorAplicacion.sede import Sede
from typing import List
from src.gestorAplicacion.administracion.empleado import Empleado
import threading

class Main:
    fecha:Fecha=None
    proveedorBdelmain=None
    evento_ui = threading.Event()

    def main():
        from src.gestorAplicacion.bodega.prenda import Prenda
        from src.gestorAplicacion.bodega.maquinaria import Maquinaria
        Main.fecha = Main.ingresarFechaConsola()
        print("Ecomoda a la orden, presiona enter para continuar")
        respuesta=input()
        if respuesta!="moscorrofio":
            Main.crearSedesMaquinasRepuestos()
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
                despedidos = Main.despedirEmpleadosConsola(Main.fecha)
                a_contratar = Main.reorganizarEmpleados(despedidos)
                Main.contratarEmpleadosConsola(a_contratar,Main.fecha)
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
                maquina = Maquinaria()
                sedePrueba = Sede() 
                plan = sedePrueba.planProduccion(maquina.agruparMaquinasDisponibles(Main.fecha), Main.fecha)
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
        from src.gestorAplicacion.bodega.prenda import Prenda
        print(f"No se pudo producir {tipo_prenda} en la sede {sede.getNombre()} por falta de insumos en la fecha {fecha}.")
        print(f"Hasta el momento se ha usado {Prenda.getCantidadTelaUltimaProduccion()} en tela.")
    
    #----------------------------gestion humana-----------------------------------

    def despedirEmpleadosConsola(fecha):
        from ..gestorAplicacion.administracion.empleado import Empleado
        print("Obteniendo lista sugerida de empleados")
        info_despidos= Empleado.listaInicialDespedirEmpleado(fecha)
        a_despedir = info_despidos[0]
        mensajes = info_despidos[1]

        for mensaje in mensajes:
            print(mensaje)

        print("\nEsta es una lista de empleados que no estan rindiendo correctamente, ¿que deseas hacer?")

        diferenciaSalarios = Persona.diferenciaSalarios()
        if diferenciaSalarios > 0:
            print(f"Tus empleados estan {diferenciaSalarios:,} sobre el promedio de salarios")
        elif diferenciaSalarios < 0:
            print(f"Tus empleados estan {diferenciaSalarios:,} bajo el promedio de salarios")
        else:
            print("Tus empleados estan en el promedio de salarios")

        for emp in a_despedir:
            print(f"Nombre: {emp.getNombre()}, Área: {emp.getAreaActual()}, Documento: {emp.getDocumento()}")

        opcion = 2
        while opcion == 2:
            print("1. Elegir a los despedidos")
            print("2. Añadir a alguien más")
            opcion = Main.nextIntSeguro()
            if opcion == 2:
                print("¿De que sede quieres añadir al empleado?")
                for i , sede in Sede.getlistaSedes():
                    print(f"{i}. {sede.getNombre()}")
                sede = Main.nextIntSeguro()
                print("¿Que empleado quieres despedir? Pon su nombre completo o documento, esto lo añadirá a la lista de despedibles.")
                for emp in Sede.getlistaSedes().get(sede).getlistaEmpleados():
                    print(f"{emp.getNombre()} {emp.getAreaActual()} {emp.getDocumento()}")
                nombre = input().strip()
                for emp in Sede.getlistaSedes().get(sede).getlistaEmpleados():
                    if emp.getNombre() == nombre or (nombre.isdigit() and emp.getDocumento() == int(nombre)):
                        a_despedir.append(emp)

        seleccion = []
        print("¿Que empleados quieres despedir? Pon su nombre completo, documento o FIN para terminar.")
        for emp in a_despedir:
            print(f"{emp.getNombre()} {emp.getAreaActual()} {emp.getDocumento()}")
        nombre = input().strip()
        while nombre.lower() != "fin":
            for emp in a_despedir:
                if emp.getNombre() == nombre or (nombre.isdigit() and emp.getDocumento() == int(nombre)):
                    seleccion.append(emp)
            nombre = input().strip()

        print("Despidiendo empleados...")
        Empleado.despedirEmpleados(seleccion, True, fecha)
        print("Listo!")
        return seleccion

    def reorganizarEmpleados(despedidos):
        print(f"Todavía nos quedan {len(despedidos)} empleados por reemplazar, revisamos la posibilidad de transferir empleados.")
        necesidades = Sede.obtenerNecesidadTransferenciaEmpleados(despedidos)
        # Desempacamos los datos dados por GestorAplicacion
        roles_a_transferir = necesidades[0]
        transferir_de = necesidades[1]
        a_contratar = necesidades[2]
        # Lista de empleados a transferir de sede, seleccionados por el usuario.
        a_transferir = []
        for rolidx in range(len(roles_a_transferir)):
            rol = roles_a_transferir[rolidx]
            sede = transferir_de[rolidx]
            print(f"Se necesita transferir {rol} de {sede.getNombre()}, estos son los candidatos: Ingresa su getNombre completo para hacerlo.")
            for emp in sede.getlistaEmpleados():
                if emp.getRol() == rol:
                    descripcion = f"Nombre: {emp.getNombre()}, Documento: {emp.getDocumento()}"
                    if emp.getRol() == Rol.VENDEDOR:
                        descripcion += f", Ventas asesoradas: {Venta.acumuladoVentasAsesoradas(emp)}"
                    elif emp.getRol() == Rol.MODISTA:
                        descripcion += f", Pericia: {emp.getPericia()}"
                    else:
                        descripcion += f", contratado en {emp.getFechaContratacion()}"
                    print(descripcion)
            # Obtenemos la cantidad de empleados a seleccionar
            cantidad = sum(1 for emp in despedidos if emp.getRol() == rol)
            for _ in range(cantidad):
                getNombre = input().strip()
                for emp in sede.getlistaEmpleados():
                    if emp.getNombre()==getNombre:
                        a_transferir.append(emp)
        Sede.reemplazarPorCambioSede(despedidos, a_transferir)
        return a_contratar

    def reorganizarEmpleados(despedidos):
        print(f"Todavía nos quedan {len(despedidos)} empleados por reemplazar, revisamos la posibilidad de transferir empleados.")
        necesidades = Sede.obtenerNecesidadTransferenciaEmpleados(despedidos)
        # Desempacamos los datos dados por GestorAplicacion
        rolesATransferir = necesidades[0]
        transferirDe = necesidades[1]
        aContratar = necesidades[2]
        # Lista de empleados a transferir de sede, seleccionados por el usuario.
        aTransferir = []
    
        for rolIdx in range(len(rolesATransferir)):
            rol = rolesATransferir[rolIdx]
            sede = transferirDe[rolIdx]
            print(f"Se necesita transferir {rol} de {Sede.getNombre(sede)}, estos son los candidatos: Ingresa su getNombre completo para hacerlo.")
            for emp in Sede.getListaEmpleados(sede):
                if Empleado.getRol(emp) == rol:
                    descripcion = f"Nombre: {Empleado.getNombre(emp)}, Documento: {Empleado.getDocumento(emp)}"
                    if Empleado.getRol(emp) == Rol.VENDEDOR:
                        descripcion += f", Ventas asesoradas: {Venta.acumuladoVentasAsesoradas(emp)}"
                    elif Empleado.getRol(emp) == Rol.MODISTA:
                        descripcion += f", Pericia: {Empleado.getPericia(emp)}"
                    else:
                        descripcion += f", contratado en {Empleado.getFechaContratacion(emp)}"
                    print(descripcion)
            # Obtenemos la cantidad de empleados a seleccionar
            cantidad = sum(1 for emp in despedidos if Empleado.getRol(emp) == rol)
            for _ in range(cantidad):
                getNombre = input().strip()
                for emp in Sede.getListaEmpleados(sede):
                    if Empleado.getNombre(emp) == getNombre:
                        aTransferir.append(emp)
        Sede.reemplazarPorCambioSede(despedidos, aTransferir)
        return aContratar
    
    def contratarEmpleadosConsola(aReemplazar, fecha):
        elecciones = Persona.entrevistar(aReemplazar)
        aptos = elecciones[0]
        rolesAReemplazar = elecciones[1]
        cantidad = elecciones[2]
        aContratar = []
        for i in range(len(rolesAReemplazar)):
            rol = rolesAReemplazar[i]
            cantidadNecesaria = cantidad[i]
            print(f"Se necesitan {cantidadNecesaria} {rol}s, estos son los candidatos:")
            for persona in aptos:
                if Persona.getRol(persona) == rol:
                    print(f"Nombre: {Persona.getNombre(persona)}, Documento: {Persona.getDocumento(persona)}, con {Persona.getExperiencia(persona)} años de experiencia.")
            print("Ingresa el getNombre de los que quieres contratar.")
            for cantidadContratada in range(cantidadNecesaria):
                getNombre = input().strip()
                for persona in aptos:
                    if Persona.getNombre(persona) == getNombre:
                        aContratar.append(persona)
                        print(f"Seleccionaste a {Persona.getNombre(persona)} con {Persona.calcularSalario(persona) - Persona.valorEsperadoSalario()} de diferencia salarial sobre el promedio")
        Persona.contratar(aContratar, aReemplazar, fecha)
        
    def errorDeReemplazo(persona):
        print(f"No se pudo contratar a {Persona.getNombre(persona)}, no sabemos a quien reemplaza.")    
        
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
        print("\nCalculando estimado entre Ventas y Deudas para ver el estado de endeudamiento de la empresa...")
        while porcentaje < 0.0 or porcentaje > 1:
            print("\nIngrese porcentaje a modificar para fidelidad de los clientes sin membresía, entre 0% y 100%")
            porcentaje = Main.nextIntSeguro() / 100.0
        diferenciaEstimado = EvaluacionFinanciera.estimadoVentasGastos(Main.fecha, porcentaje, Main.nuevoBalance)
        # Un mes se puede dar por salvado si el 80% de los gastos se pueden ver
        # cubiertos por las ventas predichas
        return diferenciaEstimado
    # Interacción 3
    def planRecuperacion(diferenciaEstimada, bancos):
        from src.gestorAplicacion.bodega.prenda import Prenda
        from src.gestorAplicacion.administracion.deuda import Deuda
        if diferenciaEstimada > 0:
            print("\nEl estimado es positivo, las ventas superan las deudas")
            print("Hay dinero suficiente para hacer el pago de algunas Deudas")
            Deuda.compararDeudas(Main.fecha)
        else:
            print("\nEl estimado es negativo, la deuda supera las ventas")
            print("No hay Dinero suficiente para cubrir los gastos de la empresa, tendremos que pedir un préstamo")
            i = -1
            nombreBanco = None
            while i < 0 or i >= len(bancos):
                for idx in range(len(bancos)):
                    print(f"{idx}: {Banco.getNombreEntidad(bancos[idx])}")
                print(f"\nIngrese número de 0 a {len(bancos) - 1} para solicitar el prestamo al Banco de su elección")
                i = Main.nextIntSeguro()
                if 0 <= i < len(bancos):
                    nombreBanco = Banco.getNombreEntidad(bancos[i])
            cuotas = 0
            while cuotas <= 0 or cuotas > 18:
                print("Ingrese número de 1 a 18 para las cuotas en que se dividirá la deuda")
                cuotas = Main.nextIntSeguro()
            deudaAdquirir = Deuda(Main.fecha, diferenciaEstimada, nombreBanco, "Banco", cuotas)
        print("\nAnalizando posibilidad de hacer descuentos para subir las ventas...")
        descuento = Venta.blackFriday(Main.fecha)
        bfString = None
        if descuento <= 0.0:
            bfString = ("El análisis de ventas realizado sobre el Black Friday arrojó que la audiencia no reacciona tan bien a los descuentos, ""propusimos no hacer descuentos")
            print("\nSegún las Ventas anteriores, aplicar descuentos no funcionará")
        else:
            bfString = ("El análisis de ventas realizado sobre el Black Friday arrojó que la audiencia reacciona bien a los descuentos, "f"propusimos un descuento del {descuento * 100}%")
            print("\nSegún las Ventas anteriores, aplicar descuentos si funcionará")
        print(f"¿Desea Cambiar el siguiente descuento: {descuento * 100}? marque 1 para Si, 2 para no ")
        num = Main.nextIntSeguro()
        nuevoDescuento = -0.1
        if num == 1:
            while nuevoDescuento < 0.0 or nuevoDescuento > 0.5:
                print("Ingrese descuento entre 0% y 5%")
                nuevoDescuento = Main.nextIntSeguro() / 100.0
        else:
            nuevoDescuento = descuento
        Prenda.prevenciones(descuento, nuevoDescuento, Main.fecha)
        analisisFuturo = (f"\n{bfString}, sin embargo su desición fue aplicar un descuento de: "
                        f"{nuevoDescuento * 100}%.")
        return analisisFuturo

#-----------------------------------------Insumos------------------------------------------------------------------------------------
   
    # Interacción 1 
    def planificarProduccion(fecha, frame):
        from src.gestorAplicacion.bodega.pantalon import Pantalon
        from src.gestorAplicacion.bodega.camisa import Camisa
        retorno = []
        frame = frame
        for sede in Sede.getListaSedes():
            listaXSede = [], insumoXSede = [], cantidadAPedir = []
            pantalonesPredichos = False
            camisasPredichas = False
            prediccionC = None
            for prenda in Sede.getPrendasInventadas(sede):
                if isinstance(prenda, Pantalon) and not pantalonesPredichos:
                    proyeccion = Venta.predecirVentas(fecha, sede, prenda.getNombre())
                    prediccionP = proyeccion * (1 - Venta.getPesimismo())
                    print("\nLa predicción de ventas para " + str(prenda) + " es de " + str(math.ceil(prediccionP)))
                    F2Insumos.prediccion(frame, sede, prenda, prediccionP)
                    for insumo in prenda.getInsumo():
                        insumoXSede.append(insumo)
                    for cantidad in Pantalon.getCantidadInsumo():
                        cantidadAPedir.append(math.ceil(cantidad * prediccionP))
                    pantalonesPredichos = True
                if isinstance(prenda, Camisa) and not camisasPredichas:
                    proyeccion = Venta.predecirVentas(fecha, sede, prenda.getNombre())
                    prediccionC = proyeccion * (1 - Venta.getPesimismo())
                    print("\nLa predicción de ventas para " + str(prenda) + " es de " + str(math.ceil(prediccionC)))
                    F2Insumos.prediccion(frame, sede, prenda, prediccionC)
                    for i, insumo in enumerate(prenda.getInsumo()):
                        cantidad = math.ceil(Camisa.getCantidadInsumo()[i] * prediccionC)
                        if insumo in insumoXSede:
                            index = insumoXSede.index(insumo)
                            cantidadAPedir[index] += cantidad
                        else:
                            insumoXSede.append(insumo)
                            cantidadAPedir.append(cantidad)
                    camisasPredichas = True
            listaXSede.append(insumoXSede)
            listaXSede.append(cantidadAPedir)
            retorno.append(listaXSede)
        return retorno

    # Interacción 2 
    def coordinarBodegas(retorno):
        listaA = []
        for sede in retorno:
            insumosAPedir = [], cantidadAPedir = [], listaSede = [], listaXSede = sede, listaInsumos = listaXSede[0], listaCantidades = listaXSede[1]
            for s in Sede.getListaSedes():
                for i in listaInsumos:
                    productoEnBodega = Sede.verificarProductoBodega(i, s)
                    idxInsumo = listaInsumos.index(i)
                    if productoEnBodega.getEncontrado():
                        listaCantidades[idxInsumo] = max(listaCantidades[idxInsumo] - Sede.getCantidadInsumosBodega(s)[productoEnBodega.index], 0)
                    cantidadNecesaria = listaCantidades[listaInsumos.index(i)]
                    productoEnOtraSede = Sede.verificarProductoOtraSede(i)
                    if productoEnOtraSede.getEncontrado():
                        print(f"\nTenemos el insumo {i.getNombre} en nuestra {productoEnOtraSede.sede}.")
                        print(f"El insumo tiene un costo de {productoEnOtraSede.precio}")
                        print("\nSeleccione una de las siguientes opciones:")
                        print(f"1. Deseo transferir el insumo desde la {productoEnOtraSede.sede}")
                        print("2. Deseo comprar el insumo")
                        opcion = int(input())
                        if opcion == 1:
                            restante = Sede.transferirInsumo(i, s, productoEnOtraSede.sede, cantidadNecesaria)
                            print(f"\n{i} transferido desde {s} con éxito")
                            if restante != 0:
                                insumosAPedir.append(i)
                                cantidadAPedir.append(restante)
                                if Empleado.getNombre(i)== "Tela":
                                    print(f"\nTenemos una cantidad de {restante} cm de tela restantes a pedir")
                                elif i.getNombre == "Boton":
                                    print(f"\nTenemos una cantidad de {restante} botones restantes a pedir")
                                elif i.getNombre == "Cremallera":
                                    print(f"\nTenemos una cantidad de {restante} cremalleras restantes a pedir")
                                else:
                                    print(f"\nTenemos una cantidad de {restante} cm de hilo restantes a pedir")
                            else:
                                print("Insumo transferido en su totalidad")
                        elif opcion == 2:
                            insumosAPedir.append(i)
                            cantidadAPedir.append(cantidadNecesaria)
                        else:
                            print("Esa opción no es valida.")
            listaSede.append(insumosAPedir)
            listaSede.append(cantidadAPedir)
            listaA.append(listaSede)
        return listaA

    # Interacción 3
    def comprarInsumos(fecha, listaA):
        from src.gestorAplicacion.bodega.proveedor import Proveedor
        from src.gestorAplicacion.administracion.deuda import Deuda
        deudas = []
        for sede in listaA:
            insumos = sede[0]
            cantidad = sede[1]
            for sedee in Sede.getListaSedes():
                for idxInsumo in range(len(insumos)):
                    proveedores = []
                    precios = []
                    mejorProveedor = None
                    mejorPrecio = float('inf')
                    cantidadAñadir = 0
                    for proveedor in Proveedor.getListaProveedores():
                        if Proveedor.getInsumo(proveedor) == insumos[idxInsumo]:
                            proveedores.append(proveedor)
                            precios.append(Proveedor.costoDeLaCantidad(proveedor,insumos[idxInsumo], cantidad[idxInsumo]))
                    for x in proveedores:
                        precio = Proveedor.costoDeLaCantidad(x,insumos[idxInsumo], cantidad[idxInsumo])
                        if precio != 0 and precio < mejorPrecio:
                            mejorPrecio = precio
                            mejorProveedor = x
                            Insumo.setProveedor(insumos[idxInsumo],x)
                    print(f"\nTenemos el insumo {Insumo.getNombre(insumos[idxInsumo])} con nuestro proveedor {Proveedor.getNombre((Insumo.getProveedor(insumos[idxInsumo])))}.")
                    if Insumo.getPrecioIndividual(insumos[idxInsumo]) < Insumo.getUltimoPrecio(insumos[idxInsumo]):
                        print("\nDado que el costo de la venta por unidad es menor al ultimo precio por el que compramos el insumo")
                        print(f"\nDesea pedir mas de la cantidad necesaria para la producción? \nCantidad: {cantidad[idxInsumo]}")
                        print("1. Si")
                        print("2. No")
                        opcion = int(input())
                        if opcion == 1:
                            cantidadAñadir = int(input(f"\nCuanta cantidad más desea pedir del insumo {insumos[idxInsumo].getNombre()}"))
                        elif opcion != 2:
                            print("Esa opción no es valida.")
                    cantidad[idxInsumo] += cantidadAñadir
                    Sede.anadirInsumo(insumos[idxInsumo], sedee, cantidad[idxInsumo])
                    print(f"\nInsumo {insumos[idxInsumo]} comprado con éxito")

                    for proveedor in Proveedor.getListaProveedores():
                        montoDeuda = 0
                        if Proveedor.getNombre(Insumo.getProveedor(insumos[idxInsumo])) == Proveedor.getNombre(proveedor):
                            montoDeuda += Insumo.getPrecioIndividual(insumos[idxInsumo]) * cantidad[idxInsumo]
                        if montoDeuda > 0:
                            if Proveedor.getDeuda(proveedor) is None:
                                deuda = Deuda(fecha, montoDeuda, proveedor.getNombre, "Proveedor", Deuda.calcularCuotas(montoDeuda))
                            elif not Deuda.getEstadoDePago(Proveedor.getDeuda(proveedor)):
                                Proveedor.unificarDeudasXProveedor(proveedor,fecha, montoDeuda)
                                deuda = Proveedor.getDeuda(proveedor)
                            deudas.append(deuda)

        return f"Ahora nuestras deudas con los proveedores lucen asi:\n{deudas}"
        
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

    def vender():
        from ..gestorAplicacion.administracion.empleado import Empleado
        from src.gestorAplicacion.bodega.pantalon import Pantalon
        from src.gestorAplicacion.bodega.camisa import Camisa
        from src.gestorAplicacion.administracion.area import Area
        venta = None
        productosSeleccionados = [], cantidadProductos = []
        print("\nIngrese la fecha de la venta:")
        fechaVenta = Main.fecha
        print("\nSeleccione el cliente al que se le realizará la venta:")
        Main.imprimirNoEmpleados()  # Muestra la lista de clientes con índices
        clienteSeleccionado = Main.nextIntSeguro()
        noEmpleados = [persona for persona in Persona.getListaPersonas() if not isinstance(persona, Empleado)]
        cliente = noEmpleados[clienteSeleccionado]
        print("\nSeleccione el número de la sede en la que se encuentra el cliente:")
        for i, sede in enumerate(Sede.getListaSedes()):
            print(f"{i}. {Sede.getNombre(sede)}")
        sedeSeleccionada = Main.nextIntSeguro()
        sede = Sede.getListaSedes()[sedeSeleccionada]
        print("\nSeleccione el número del empleado que se hará cargo del registro de la venta:")
        for i, empleado in enumerate(sede.getListaEmpleados()):
            if Empleado.getAreaActual(empleado) == Area.OFICINA:
                print(f"{i}. {Empleado.getNombre(empleado)}")
        encargadoSeleccionado = Main.nextIntSeguro()
        encargado = Sede.getListaEmpleados(sede)[encargadoSeleccionado]
        print("\nSeleccione el número del empleado que se hará cargo de asesorar la venta:")
        for i, empleado in enumerate(Sede.getListaEmpleados(sede)):
            if empleado.getAreaActual() == Area.VENTAS:
                print(f"{i}. {Empleado.getNombre(empleado)}")
        vendedorSeleccionado = Main.nextIntSeguro()
        vendedor = Sede.getListaEmpleados(sede)[vendedorSeleccionado]
        costosEnvio = 0
        while True:
            print("\nSeleccione el getNombre del producto que venderá:")
            print(f"0. Camisa - Precio {Camisa.precioVenta()}")
            print(f"1. Pantalon - Precio {Pantalon.precioVenta()}")
            productoSeleccionado = input()
            prendaSeleccionada = next((prenda for prenda in Sede.getPrendasInventadasTotal() if Prenda.getNombre(prenda) == productoSeleccionado), None)
            if prendaSeleccionada is None:
                print("Producto no encontrado. Intente nuevamente.")
                continue
            nombrePrendaSeleccionada = Prenda.getNombre(prendaSeleccionada)
            print("Ingrese la cantidad de unidades que se desea del producto elegido:")
            cantidadPrenda = Main.nextIntSeguro()
            cantidadProductos.append(cantidadPrenda)
            cantidadDisponible = sum(1 for prenda in Sede.getPrendasInventadasTotal() if Prenda.getNombre(prenda) == Prenda.getNombre(prendaSeleccionada))
            Main.manejarFaltantes(sede, cantidadPrenda, cantidadDisponible, nombrePrendaSeleccionada, costosEnvio)
            if 0 < cantidadPrenda < len(Sede.getPrendasInventadasTotal()):
                eliminadas = 0
                for i in range(len(Sede.getPrendasInventadasTotal())):
                    if eliminadas >= cantidadPrenda:
                        break
                    if Sede.getPrendasInventadasTotal()[i] == prendaSeleccionada:
                        eliminada = Sede.getPrendasInventadasTotal().pop(i)
                        Sede.getPrendasInventadas(sede).remove(eliminada)
                        eliminadas += 1
                        i -= 1
            print("\n¿Deseas agregar otro producto a la venta?: (si/no)")
            decision = input().lower()
            if decision == "no":
                print("Selección finalizada")
                break
            if decision != "si":
                break
        sumaPreciosPrendas = 0
        cantidadCamisas = 0
        cantidadPantalon = 0
        for prenda in productosSeleccionados:
            if isinstance(prenda, Camisa):
                sumaPreciosPrendas += Camisa.precioVenta()
                cantidadCamisas += 1
                if cantidadCamisas >= 10:
                    descuento = int(sumaPreciosPrendas * 0.05)
                    sumaPreciosPrendas -= descuento
            elif isinstance(prenda, Pantalon):
                sumaPreciosPrendas += Pantalon.precioVenta()
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
        print(f"Subtotal: {sumaPreciosPrendas}")
        comision = int(montoPagar * 0.05)
        Empleado.setRendimientoBonificacion(vendedor,comision)
        
        return venta 

    def imprimirNoEmpleados():
        from ..gestorAplicacion.administracion.empleado import Empleado
        noEmpleados = []
        print("Lista de clientes:")
        for persona in Persona.getListaPersonas():
            if not isinstance(persona, Empleado):
                noEmpleados.append(persona)
        index = 0
        for persona in noEmpleados:
            print(f"{index}. {persona}")
            index += 1

    def realizarVenta(venta):
        from src.gestorAplicacion.bodega.proveedor import Proveedor
        productosSeleccionados = Venta.getArticulos(venta)
        sede = Venta.getSede(venta)
        banco = Sede.getCuentaSede(sede)
        totalPrendas = len(productosSeleccionados)

        insumosBodega = Sede.getListaInsumosBodega(sede)
        cantidadInsumosBodega = Sede.getCantidadInsumosBodega(sede)

        bolsasSeleccionadas = []
        capacidadTotal = 0

        while capacidadTotal < totalPrendas:
            print("\nSeleccione el tamaño de bolsa:")
            bp, bm, bg = False, False, False
            for i in range(len(insumosBodega)):
                bolsa = insumosBodega[i]
                if isinstance(bolsa, Bolsa):
                    capacidad = bolsa.getCapacidadMaxima()
                    cantidad = Sede.getCantidadInsumosBodega(sede)[i]
                    if capacidad == 1 and cantidad > 0:
                        bp = True
                    if capacidad == 3 and cantidad > 0:
                        bm = True
                    if capacidad == 8 and cantidad > 0:
                        bg = True

            if bp: print("1. Bolsa pequeña (1 producto)")
            if bm: print("2. Bolsa mediana (3 productos)")
            if bg: print("3. Bolsa grande (8 productos)")

            opcionBolsa = Main.nextIntSeguro()

            capacidadBolsa = 0
            nombreBolsa = None
            if opcionBolsa == 1:
                capacidadBolsa = 1
                nombreBolsa = "Bolsa pequeña"
            elif opcionBolsa == 2:
                capacidadBolsa = 3
                nombreBolsa = "Bolsa mediana"
            elif opcionBolsa == 3:
                capacidadBolsa = 8
                nombreBolsa = "Bolsa grande"
            else:
                print("Opción inválida. Intente nuevamente.")
                continue

            bolsaEncontrada = False
            cantidadDisponible = 0
            capacidadTotal += capacidadBolsa
            for i in range(len(Sede.getListaInsumosBodega(sede))):
                insumo = Sede.getListaInsumosBodega(sede)[i]
                if isinstance(insumo, Bolsa) and insumo.getCapacidadMaxima() == capacidadBolsa:
                    cantidadDisponible += cantidadInsumosBodega[i]
                    if cantidadDisponible > 0:
                        bolsasSeleccionadas.append(insumo)
                        cantidadInsumosBodega[i] -= 1
                        bolsaEncontrada = True
                        break
                totalPrendas -= cantidadDisponible
                if capacidadTotal == totalPrendas:
                    break

            for revisarSede in Sede.getListaSedes():
                listaInsumos = Sede.getListaInsumosBodega(revisarSede)
                cantidadInsumos = Sede.getCantidadInsumosBodega(revisarSede)
                for i in range(len(listaInsumos)):
                    insumo = listaInsumos[i]
                    if isinstance(insumo, Bolsa) and cantidadInsumos[i] < 10:
                        print(f"La sede {Sede.getNombre(revisarSede)} tiene menos de 10 bolsas en stock (Cantidad: {cantidadInsumos[i]}).")
                        print("Comprando al proveedor...")
                        for e in range(len(listaInsumos)):
                            insumo = listaInsumos[e]    
                            if isinstance(insumo, Bolsa) and insumo.getNombre() == nombreBolsa:
                                print(f"¿Cuántas bolsas de {insumo.getNombre()} desea comprar?")
                                cantidadComprar = Main.nextIntSeguro()
                                costoCompra = Proveedor.costoDeLaCantidad(insumo, cantidadComprar)
                                banco.setAhorroBanco(Banco.getAhorroBanco(banco) - costoCompra)
                                cantidadInsumosBodega[e] += cantidadComprar
                                insumo.setPrecioCompra(costoCompra)
                                insumo.setPrecioCompra(costoCompra)
                                print(f"Se compraron {cantidadComprar} {nombreBolsa} por un costo total de {costoCompra}")
                                break

        Venta.setBolsas(venta,bolsasSeleccionadas)
        totalVenta = Venta.getMontoPagado(venta) + len(bolsasSeleccionadas) * 2000
        Venta.setMontoPagado(venta,totalVenta)

        print(f"\nVenta realizada. Total de la venta con bolsas: {totalVenta}")
        return venta

    def manejarFaltantes(sede, cantidadPrenda, disponibles, tipoPrenda, costosEnvio):
        faltantes = cantidadPrenda - disponibles

        if faltantes > 0:
            costosEnvio += 3000 + (faltantes * 1000)
            print("Valor de costos de envío: " + str(costosEnvio))
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

            if prendasTransferidas < faltantes:
                print("No se pudieron transferir todas las prendas faltantes. Faltan " + str(faltantes - prendasTransferidas) + " unidades.")

    def tarjetaRegalo(venta):
        from src.gestorAplicacion.bodega.pantalon import Pantalon
        from src.gestorAplicacion.bodega.camisa import Camisa
        sede = Venta.getSede(venta)
        banco = Sede.getCuentaSede(sede)

        print("\n¿Desea usar una tarjeta de regalo? (si/no)")
        respuesta = input().lower()
        nuevoIntento = 1
        while nuevoIntento == 1:
            if respuesta == "si":
                print("Ingrese el código de la tarjeta de regalo:")
                codigoIngresado = int(input())

                if codigoIngresado in Venta.getCodigosRegalo():
                    print("Código válido. Procesando tarjeta de regalo...")
                    indice = Venta.getCodigosRegalo().index(codigoIngresado)
                    montoTarjeta = Venta.getMontosRegalo()[indice]
                    montoVenta = Venta.getMontoPagado(venta)

                    if montoTarjeta >= montoVenta:
                        print("El monto de la tarjeta cubre la totalidad de la venta.")
                        saldoRestante = montoTarjeta - montoVenta
                        Venta.getMontosRegalo()[indice] = saldoRestante
                        Venta.setMontoPagado(venta,0)

                        print("Venta pagada con tarjeta de regalo.")
                        print("Saldo restante en la tarjeta de regalo: $" + str(saldoRestante))
                    else:
                        montoFaltante = montoVenta - montoTarjeta
                        Venta.getMontosRegalo()[indice] = 0
                        venta.setMontoPagado(montoFaltante)
                        print("El monto de la tarjeta no es suficiente para cubrir la venta.")
                        print("Monto restante a pagar: $" + str(montoFaltante))

                    if Venta.getMontosRegalo()[indice] == 0:
                        Venta.getCodigosRegalo().pop(indice)
                        Venta.getMontosRegalo().pop(indice)
                        print("La tarjeta de regalo se ha agotado y ha sido desactivada.")

                    nuevoIntento = 2
                else:
                    print("El código ingresado no es válido. Por favor, intentar de nuevo o pagar el monto total")
                    print("Ingresa 1 para intentar de nuevo.")
                    print("Ingresa 2 para salir del intento")
                    nuevoIntento = Main.nextIntSeguro()
            elif respuesta == "no":
                nuevoIntento -= 1
                break

        print("\n¿Desea comprar una tarjeta de regalo? (si/no)")
        compraTarjeta = input().lower()

        if compraTarjeta == "si":
            print("¿Por cuánto será la tarjeta de regalo? (monto en pesos)")
            montoTarjeta = Main.nextIntSeguro()
            codigoGenerado = Main.generarCodigoAleatorio()
            Venta.getCodigosRegalo().append(codigoGenerado)
            Venta.getMontosRegalo().append(montoTarjeta)
            Banco.setAhorroBanco(banco,Banco.getAhorroBanco(banco) + montoTarjeta)

            print("Tarjeta de regalo generada exitosamente.")
            print("Código: " + codigoGenerado)
            print("Monto: $" + str(montoTarjeta))

        ingreso = Venta.getMontoPagado(venta)
        print("Ingreso calculado: $" + str(ingreso))
        Banco.setAhorroBanco(banco, Banco.getAhorroBanco(banco) + ingreso)

        print("Monto total en la cuenta de la sede: $" + str(Banco.getAhorroBanco(banco)))
        bancoRecibir = Banco.getCuentaPrincipal()
        bancoTransferir = Sede.getCuentaSede(sede)
        if bancoTransferir != bancoRecibir:
            print("\n¿Desea transferir fondos a la cuenta principal? (si/no)")
            transferirFondos = input().lower()
            if transferirFondos == "si":
                print("¿Qué porcentaje desea transferir? (20% o 60%)")
                porcentaje = Main.nextIntSeguro()
                if porcentaje == 20 or porcentaje == 60:
                    montoTransferencia = (Banco.getAhorroBanco(bancoTransferir) * porcentaje / 100) - 50000
                    if montoTransferencia > 0:
                        if bancoRecibir.getNombreCuenta() == "principal":
                            bancoRecibir.setAhorroBanco(Banco.getAhorroBanco(bancoTransferir) - (montoTransferencia + 50000))
                            bancoRecibir.setAhorroBanco(bancoRecibir.getAhorroBanco() + montoTransferencia)
                            print("Transferencia exitosa.")
                            print("Monto transferido: $" + str(montoTransferencia))
                            print("Costo de transferencia: $50000")
                    else:
                        print("Fondos insuficientes para cubrir la transferencia y el costo.")
                else:
                    print("Porcentaje no válido. No se realizará la transferencia.")
        if bancoTransferir is not None:
            print("Estado final de la cuenta de la sede: $" + str(Banco.getAhorroBanco(bancoTransferir)))
        if bancoRecibir is not None:
            print("Estado final de la cuenta principal: $" + str(bancoRecibir.getAhorroBanco()))
            productosSeleccionados = Venta.getArticulos(venta)
            montoPagar = Venta.getMontoPagado(venta)
            tasaIva = 0.19
            valorBase = int(montoPagar / (1 + tasaIva))
            iva = montoPagar - valorBase
            print("\n---- FACTURA ----")
            print("Prendas compradas:")
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
                    print(prenda.getNombre() + " - Cantidad: " + str(cantidadCamisas) + " - Subtotal: $" + str(subtotalCamisas))
                    camisaEncontrada = True
                if isinstance(prenda, Pantalon) and not pantalonEncontrado:
                    print(prenda.getNombre() + " - Cantidad: " + str(cantidadPantalon) + " - Subtotal: $" + str(subtotalPantalon))
                    pantalonEncontrado = True

            print("Valor total a pagar: $" + str(montoPagar))
            print("Subtotal prendas: $" + str(Venta.getSubtotal(venta)))
            print("IVA: $" + str(iva))
            print("Venta registrada por: " + Venta.getEncargado(venta))
            print("Asesor de la compra: " + Venta.getAsesor(venta))

            return "El monto total a pagar por parte del cliente es " + str(montoPagar) + " y el estado final de la cuenta de la sede es $" + str(Banco.getAhorroBanco(bancoTransferir))
    
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

    def pedirModista(cantidadPrendas, sede, idxTanda):
        print(f"Seleccione el modista que se encargará de la tanda #{idxTanda} de producción de {cantidadPrendas} prendas en {sede.getNombre()}:")
        modistas = [empleado for empleado in sede.getListaEmpleados() if empleado.getRol() == Rol.MODISTA]
        for i, modista in enumerate(modistas):
            print(f"{i}. {modista.getNombre()}")
        while True:
            seleccion = Main.nextIntSeguro()
            if 0 <= seleccion < len(modistas):
                return modistas[seleccion]
            else:
                print("Opción inválida. Intente nuevamente.")

    def printsInt2(senall):
        mensajes = {
            1: "La Sede 2 no está trabajando por falta de maquinaria disponible...\n1. ¿Desea producir todo hoy desde la Sede Principal?\n2. ¿Desea producir mañana lo de la Sede 2 desde la sede Principal?",
            2: "\n Marque una opcion correcta entre 1 o 2...\n",
            3: "La Sede Principal no esta trabajando por falta de maquinaria disponible...\n1. ¿Desea producir todo hoy desde la Sede 2\n2. ¿Desea producir mañana lo de la Sede Principal desde la sede 2?",
            4: "\n Marque una opcion correcta entre 1 o 2...\n",
            5: "La Sede Principal esta sobrecargada, ¿Que desea hacer? \n1. Enviar parte de la produccion a la Sede 2, para producir por partes iguales.\n2. Ejecutar produccion, asumiendo todo el costo por sobrecarga en la Sede Principal.",
            6: "Coloca una opcion indicada entre 1 o 2...",
            7: "La Sede 2 esta sobrecargada, ¿Que desea hacer? \n1. Enviar parte de la produccion a la Sede Principal, para producir por partes iguales.\n2. Ejecutar produccion, asumiendo todo el costo por sobrecarga en la Sede 2.",
            8: "Coloca una opcion indicada entre 1 o 2...",
            9: "Las dos sedes estan sobrecargadas, ¿Que quieres hacer?...\n1. Producir mañana las prendas que generan sobrecarga.\n2. Producir todo hoy, asumiendo el costo por sobrecarga.",
            10: "Seleccione una opcion indicada entre 1 o 2...",
            11: "\n Lo sentimos, se debe arreglar la maquinaria en alguna de las dos sedes para comenzar a producir...\n"
        }
        print(mensajes.get(senall, ""))

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
        BordadoraIndustrial = Maquinaria("Bordadora Industrial", 31000000, 500, repuestosBI, sedeP)
        MaquinaDeTermofijado = Maquinaria("Maquina de Termofijado", 20000000, 1000,repuestosMTermofijado, sedeP)
        MaquinaDeTijereado = Maquinaria("Maquina de Tijereado", 5000000, 600, repuestosMTijereado,sedeP)
        Impresora = Maquinaria("Impresora", 800000, 2000, repuestosImp, sedeP)
        Registradora = Maquinaria("Caja Registradora", 700000, 17000, repuestosRe, sedeP)
        Computador = Maquinaria("Computador", 2_000_000, 10000, repuestosComp, sedeP)

        # sede2
        MaquinaDeCoser2 = Maquinaria("Maquina de Coser Industrial", 4250000, 600, repuestosMC2, sede2)
        MaquinaDeCorte2 = Maquinaria("Maquina de Corte", 6000000, 700, repuestosMCorte2, sede2)
        PlanchaIndustrial2 = Maquinaria("Plancha Industrial", 2000000, 900, repuestosPI2, sede2)
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

        i1 = Insumo("Tela", p5, 1 * 20, sedeP)
        i2 = Insumo("Tela", p5, 1 * 20,  sede2)
        i3 = Insumo("Boton", p3, 4 * 20, sedeP)
        i4 = Insumo("Boton", p3, 4 * 20, sede2)
        i5 = Insumo("Cremallera", p4, 1 * 20, sedeP)
        i6 = Insumo("Cremallera", p4, 1 * 20, sede2)
        i7 = Insumo("Hilo", p2, 100 * 20, sedeP)
        i8 = Insumo("Hilo", p2, 100 * 20, sede2)
        i9 = Bolsa("Bolsa", p10, 1 * 20, sedeP, 8)
        i10 = Bolsa("Bolsa", p10, 1 * 20, sede2, 8)
        i11 = Bolsa("Bolsa", p10, 1 * 20, sedeP, 3)
        i12 = Bolsa("Bolsa", p10, 1 * 20, sede2, 3)
        i13 = Bolsa("Bolsa", p10, 1 * 20, sedeP, 1)
        i14 = Bolsa("Bolsa", p10, 1 * 20, sede2, 1)

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
        c7 = Persona("Mauricio Brightman", 8823954, Rol.ASISTENTE, 10, False, Membresia.ORO)
        c8 = Persona("Nicolás Mora", 4365567, Rol.EJECUTIVO, 8, False, Membresia.NULA)
        c9 = Persona("Roberto Mendoza", 28096740, Rol.PRESIDENTE, 2, False, Membresia.ORO)
        c10 = Persona("Hermes Pinzón", 21077781, Rol.ASISTENTE, 2, False, Membresia.NULA)
        c11 = Persona("Julia Solano", 28943158, Rol.SECRETARIA, 10, False, Membresia.BRONCE)
        c12 = Persona("Maria Beatriz Valencia", 6472799, Rol.ASISTENTE, 2, False, Membresia.BRONCE)
        c13 = Persona("Antonio Sanchéz", 8922998, Rol.VENDEDOR, 12, False, Membresia.NULA)
        tiposp = []; cantidadesp = [];tiposc = []; cantidadesc = []
        tiposp.append("Tela")
        tiposp.append("Boton")
        tiposp.append("Cremallera")
        tiposp.append("Hilo")
        cantidadesp.append(200)
        cantidadesp.append(1)
        cantidadesp.append(1)
        cantidadesp.append(300)
        Pantalon.setCantidadInsumo(cantidadesp)
        Pantalon.setTipoInsumo(tiposp)
        tiposc.append("Tela")
        tiposc.append("Boton")
        tiposc.append("Hilo")
        cantidadesc.append(100)
        cantidadesc.append(3)
        cantidadesc.append(90)
        Camisa.setCantidadInsumo(cantidadesc)
        Camisa.setTipoInsumo(tiposc)
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
        v6 = Venta(sedeP, Fecha(25, 11, 24), c4, Wilson, Mario, ps6, 400000, 600_000)
        v6.setCostoEnvio(100000)
        b3.setAhorroBanco(b3.getAhorroBanco() + 600000)
        com6 = round(600_000 * 0.05)
        Wilson.setRendimientoBonificacion(com6)
        maxProductos = 5
        minProductos = 1
        Main.crearVentaAleatoria(minProductos,maxProductos, Fecha(10,11,24), Aura, Cata, 300, sedeP)
        Main.crearVentaAleatoria(minProductos,maxProductos, Fecha(10,11,24), Aura, Mario, 300, sedeP)
        Main.crearVentaAleatoria(minProductos,maxProductos, Fecha(29,11,24), Aura, Cata, 600, sedeP)
        Main.crearVentaAleatoria(minProductos,maxProductos, Fecha(29,11,24), Aura, Mario, 600, sedeP)
        Main.crearVentaAleatoria(minProductos,maxProductos, Fecha(20,12,24), Aura, Cata, 700, sedeP)
        Main.crearVentaAleatoria(minProductos,maxProductos, Fecha(20,12,24), Aura, Mario, 700, sedeP)
        Main.crearVentaAleatoria(minProductos,maxProductos, Fecha(20,1,25), Aura, Cata, 700, sedeP)
        Main.crearVentaAleatoria(minProductos,maxProductos, Fecha(20,1,25), Aura, Mario, 700, sedeP)
        Main.crearVentaAleatoria(minProductos,maxProductos, Fecha(20,1,25), Freddy,Patricia , 300, sede2)
        pass

    @classmethod
    def listaInicialDespedirEmpleado(cls):
        return Empleado.listaInicialDespedirEmpleado(Main.fecha)

    @classmethod
    def despedirEmpleados(cls, empleados):
        Empleado.despedirEmpleados(empleados, True, Main.fecha)
    
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
            if sede.getNombre()==getNombre:
                return sede

if __name__ == "__main__":
    print("Para usar la interfaz grafica, 1. Para usar la consola, 2")
    opcion = input()
    match opcion:
        case "1":
            from src.uiMain.bienvenida.bienvenida import Aplication
            Main.crearSedesMaquinasRepuestos()
            Aplication.bienvenida()
        case "2":
            Main.main()