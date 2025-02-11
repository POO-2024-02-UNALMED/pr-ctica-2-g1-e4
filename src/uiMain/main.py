import math
import random
from src.gestorAplicacion.administracion.banco import Banco
from src.gestorAplicacion.administracion.rol import Rol
from src.gestorAplicacion.bodega.bolsa import Bolsa
from src.gestorAplicacion.bodega.insumo import Insumo
from src.gestorAplicacion.fecha import Fecha
from src.gestorAplicacion.membresia import Membresia
from src.gestorAplicacion.venta import Venta
from ..gestorAplicacion.persona import Persona
from src.gestorAplicacion.sede import Sede
from typing import List

class Main:
    fecha=None 
    def main():
        from src.gestorAplicacion.bodega.prenda import Prenda
        from src.gestorAplicacion.bodega.maquinaria import Maquinaria
        #fecha = Main.ingresarFecha()
        print("Ecomoda a la orden, presiona enter para continuar")
        input()
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
                despedidos = Main.despedirEmpleados(Main.fecha)
                a_contratar = Main.reorganizarEmpleados(despedidos)
                Main.contratarEmpleados(a_contratar)
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
                sede.getHistorialVentas().append(venta)
            elif opcion == 5:
                maquina = Maquinaria()
                sedePrueba = Sede() 
                plan = sedePrueba.planProduccion(maquina.agruparMaquinasDisponibles(Main.fecha), Main.fecha)
                creadas = Prenda.producirPrendas(plan,Main.fecha)
                if (creadas):
                    print(Prenda.getCantidadUltimaProduccion()+" Prendas creadas con éxito")
                else:
                    print("No se pudo producir todo, los insumos no alcanzaron, producimos "+Prenda.getCantidadUltimaProduccion()+" prendas")
                
            #elif opcion == 6:
                #Serializador.serializar()
                #sys.exit(0)
                
            else:
                print("Esa opción no es valida.")

    def ingresarFecha(diaI,mesI,añoI):
        fecha=None
        partes = diaI.split()
        numero=-1
        if partes[-1].isdigit():
            numero = int(partes[-1])
        dia = numero
        partes = mesI.split()
        if partes[-1].isdigit():
            numero = int(partes[-1])
        mes = numero
        partes = añoI.split()
        if partes[-1].isdigit():
            numero = int(partes[-1])
        año = numero
        if dia <= 0 or dia > 31:
            startFrame.borrar()
        elif mes <= 0 or mes > 12:
            startFrame.borrar()
        elif año <= 0:
            startFrame.borrar()
        else:
            fecha = Fecha(dia, mes, año)
            Main.fecha=fecha
        return fecha
    
    def  avisarFaltaDeInsumos(sede, fecha, tipo_prenda):
        from src.gestorAplicacion.bodega.prenda import Prenda
        print(f"No se pudo producir {tipo_prenda} en la sede {sede.getNombre()} por falta de insumos en la fecha {fecha}.")
        print(f"Hasta el momento se ha usado {Prenda.getCantidadTelaUltimaProduccion()} en tela.")

    def despedirEmpleados(fecha):
        from ..gestorAplicacion.administracion.empleado import Empleado
        print("Obteniendo lista sugerida de empleados")
        info_despidos= Empleado.listaInicialDespedirEmpleado(fecha)
        a_despedir = info_despidos[0]
        mensajes = info_despidos[1]

        for mensaje in mensajes:
            print(mensaje)

        print("\nEsta es una lista de empleados que no estan rindiendo correctamente, ¿que deseas hacer?")

        diferenciaSalarios -= Persona.diferenciaSalarios()
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
        necesidades = Sede.obtener_necesidad_transferencia_empleados(despedidos)
        
        # Desempacamos los datos dados por GestorAplicacion
        roles_a_transferir = necesidades[0]
        transferir_de = necesidades[1]
        a_contratar = necesidades[2]

        # Lista de empleados a transferir de sede, seleccionados por el usuario.
        a_transferir = []

        for rolidx in range(len(roles_a_transferir)):
            rol = roles_a_transferir[rolidx]
            sede = transferir_de[rolidx]
            print(f"Se necesita transferir {rol} de {sede.getNombre()}, estos son los candidatos: Ingresa su nombre completo para hacerlo.")
            
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
                nombre = input().strip()
                for emp in sede.getlistaEmpleados():
                    if emp.getNombre()==nombre:
                        a_transferir.append(emp)

        Sede.reemplazarPorCambioSede(despedidos, a_transferir)

        return a_contratar

    def contratarEmpleados(a_reemplazar,fecha):
        elecciones = Persona.entrevistar(a_reemplazar)
        aptos = elecciones[0]
        roles_a_reemplazar = elecciones[1]
        cantidad = elecciones[2]

        a_contratar = []
        for i in range(len(roles_a_reemplazar)):
            rol = roles_a_reemplazar[i]
            cantidad_necesaria = cantidad[i]

            print(f"Se necesitan {cantidad_necesaria} {rol}s, estos son los candidatos:")

            for persona in aptos:
                if persona.getRol() == rol:
                    print(f"Nombre: {persona.getNombre()}, Documento: {persona.getDocumento()}, con {persona.getExperiencia()} años de experiencia.")

            print("Ingresa el nombre de los que quieres contratar.")

            for cantidad_contratada in range(cantidad_necesaria):
                nombre = input().strip()
                for persona in aptos:
                    if persona.getNombre()==nombre:
                        a_contratar.append(persona)
                        print(f"Seleccionaste a {persona.getNombre()} con {persona.calcularSalario() - persona.valorEsperadoSalario()} de diferencia salarial sobre el promedio")

        Persona.contratar(a_contratar, a_reemplazar, fecha)

    def errorDeReemplazo(persona):
        print(f"No se pudo contratar a {persona.getNombre()}, no sabemos a quien reemplaza.")

    def calcularBalanceAnterior(fecha):
        from src.gestorAplicacion.administracion.evaluacionFinanciera import EvaluacionFinanciera
        from src.gestorAplicacion.administracion.deuda import Deuda
        from src.gestorAplicacion.administracion.area import Area
        print("\nObteniendo balance entre Ventas y Deudas para saber si las ventas cubren los gastos de la producción de nuestras prendas...")
        balance_costos_produccion = Venta.calcularBalanceVentaProduccion(fecha)
        eleccion = 0
        while eleccion <= 0 or eleccion > 3:
            print("\nIngrese las deudas que quiere calcular")
            print("Ingrese 1 para proveedor, 2 para Banco o 3 para ambos")
            eleccion = Main.nextIntSeguro()
        
        deuda_calculada = Deuda.calcularDeudaMensual(fecha, eleccion)
        balance_total = balance_costos_produccion - deuda_calculada
        empleado = None
        elegible_empleados = []
        
        for empleado_actual in Sede.getListaEmpleadosTotal():
            if empleado_actual.getAreaActual() == Area.DIRECCION:
                elegible_empleados.append(empleado_actual)
        
        indice_empleado = -1
        while indice_empleado < 0 or indice_empleado >= len(elegible_empleados):
            for indice in range (len(elegible_empleados)):
                print(f"{indice} {elegible_empleados[indice]}")
            print(f"\nIngrese número de 0 a {len(elegible_empleados) - 1} según el Directivo que escoja para registrar el balance")
            indice_empleado = Main.nextIntSeguro()
            empleado = elegible_empleados[indice_empleado]
        
        nuevo_balance = EvaluacionFinanciera(balance_total, empleado)
        return nuevo_balance

    # Interaccion 2 Sistema Financiero
    def calcularEstimado(fecha, balance_anterior):
        from src.gestorAplicacion.administracion.evaluacionFinanciera import EvaluacionFinanciera
        print("\nCalculando estimado entre Ventas y Deudas para ver el estado de endeudamiento de la empresa...")
        porcentaje = -1.0
        while porcentaje < 0.0 or porcentaje > 1:
            print("\nIngrese porcentaje a modificar para fidelidad de los clientes sin membresía, entre 0% y 100%")
            porcentaje = Main.nextIntSeguro() / 100.0
        
        diferencia_estimado = EvaluacionFinanciera.estimadoVentasGastos(fecha, porcentaje, balance_anterior)
        # Un mes se puede dar por salvado si el 80% de los gastos se pueden ver
        # cubiertos por las ventas predichas
        return diferencia_estimado

    def planRecuperacion(diferencia_estimada, fecha, bancos):
        from src.gestorAplicacion.bodega.prenda import Prenda
        from src.gestorAplicacion.administracion.deuda import Deuda
        if diferencia_estimada > 0:
            print("\nEl estimado es positivo, las ventas superan las deudas")
            print("Hay dinero suficiente para hacer el pago de algunas Deudas")
            Deuda.compararDeudas(fecha)
        else:
            print("\nEl estimado es negativo, la deuda supera las ventas")
            print("No hay Dinero suficiente para cubrir los gastos de la empresa, tendremos que pedir un préstamo")
            i = -1
            nombre_banco = None
            while i < 0 or i >= len(bancos):
                for idx in range(len(bancos)):
                    print(f"{idx}: {bancos[idx].getNombreEntidad()}")
                print(f"\nIngrese número de 0 a {len(bancos) - 1} para solicitar el prestamo al Banco de su elección")
                i = Main.nextIntSeguro()
                if 0 <= i < len(bancos):
                    nombre_banco = bancos[i].getNombreEntidad()

            cuotas = 0
            while cuotas <= 0 or cuotas > 18:
                print("Ingrese número de 1 a 18 para las cuotas en que se dividirá la deuda")
                cuotas = Main.nextIntSeguro()

            deuda_adquirir = Deuda(fecha, diferencia_estimada, nombre_banco, "Banco", cuotas)

        print("\nAnalizando posibilidad de hacer descuentos para subir las ventas...")
        descuento = Venta.blackFriday(fecha)
        bf_string = None
        if descuento <= 0.0:
            bf_string = ("El análisis de ventas realizado sobre el Black Friday arrojó que la audiencia no reacciona tan bien a los descuentos, "
                        "propusimos no hacer descuentos")
            print("\nSegún las Ventas anteriores, aplicar descuentos no funcionará")
        else:
            bf_string = ("El análisis de ventas realizado sobre el Black Friday arrojó que la audiencia reacciona bien a los descuentos, "
                        f"propusimos un descuento del {descuento * 100}%")
            print("\nSegún las Ventas anteriores, aplicar descuentos si funcionará")

        print(f"¿Desea Cambiar el siguiente descuento: {descuento * 100}? marque 1 para Si, 2 para no ")
        num = Main.nextIntSeguro()
        nuevo_descuento = -0.1
        if num == 1:
            while nuevo_descuento < 0.0 or nuevo_descuento > 0.5:
                print("Ingrese descuento entre 0% y 5%")
                nuevo_descuento = Main.nextIntSeguro() / 100.0
        else:
            nuevo_descuento = descuento

        Prenda.prevenciones(descuento, nuevo_descuento, fecha)
        analisis_futuro = (f"\n{bf_string}, sin embargo su desición fue aplicar un descuento de: "
                        f"{nuevo_descuento * 100}%.")
        return analisis_futuro
    
    def planificar_produccion(fecha):
        from src.gestorAplicacion.bodega.pantalon import Pantalon
        from src.gestorAplicacion.bodega.camisa import Camisa
        retorno = []

        for sede in Sede.getlistaSedes():
            print("\nPara la " + sede.getNombre())
            print("Tenemos un porcentaje de pesimismo: " + str(round(Venta.getPesimismo() * 100)) + "%")
            print("\nSeleccione una de las siguientes opciones:")
            print("1. Estoy de acuerdo con el porcentaje de pesimismo")
            print("2. Deseo cambiar el porcentaje de pesimismo")

            opcion = int(input())
            if opcion == 2:
                new_pesimismo = int(input("Ingrese el nuevo porcentaje de pesimismo % ")) / 100
                Venta.setPesimismo(new_pesimismo)
            elif opcion != 1:
                print("Esa opción no es valida.")

            lista_x_sede = []
            insumo_x_sede = []
            cantidad_a_pedir = []
            pantalones_predichos = False
            camisas_predichas = False

            for prenda in sede.get_prendas_inventadas():
                if isinstance(prenda, Pantalon) and not pantalones_predichos:
                    proyeccion = Venta.predecirVentas(fecha, sede, prenda.getNombre())
                    prediccion_p = proyeccion * (1 - Venta.getPesimismo())
                    print("\nLa predicción de ventas para " + str(prenda) + " es de " + str(math.ceil(prediccion_p)))

                    for insumo in prenda.getInsumo():
                        insumo_x_sede.append(insumo)
                    for cantidad in Pantalon.getCantidadInsumo():
                        cantidad_a_pedir.append(math.ceil(cantidad * prediccion_p))
                    pantalones_predichos = True

                if isinstance(prenda, Camisa) and not camisas_predichas:
                    proyeccion = Venta.predecirVentas(fecha, sede, prenda.getNombre())
                    prediccion_c = proyeccion * (1 - Venta.getPesimismo())
                    print("\nLa predicción de ventas para " + str(prenda) + " es de " + str(math.ceil(prediccion_c)))

                    for i, insumo in enumerate(prenda.getInsumo()):
                        cantidad = math.ceil(Camisa.getCantidadInsumo()[i] * prediccion_c)
                        if insumo in insumo_x_sede:
                            index = insumo_x_sede.index(insumo)
                            cantidad_a_pedir[index] += cantidad
                        else:
                            insumo_x_sede.append(insumo)
                            cantidad_a_pedir.append(cantidad)
                    camisas_predichas = True

            lista_x_sede.append(insumo_x_sede)
            lista_x_sede.append(cantidad_a_pedir)
            retorno.append(lista_x_sede)

        return retorno
    
    def coordinarBodegas(retorno):
        lista_a = []
        
        for sede in retorno:
            insumos_a_pedir = []
            cantidad_a_pedir = []
            lista_sede = []

            lista_x_sede = sede
            lista_insumos = lista_x_sede[0]
            lista_cantidades = lista_x_sede[1]

            for s in Sede.getlistaSedes():
                for i in lista_insumos:
                    producto_en_bodega = Sede.verificarProductoBodega(i, s)
                    idx_insumo = lista_insumos.index(i)
                    if producto_en_bodega.getEncontrado():
                        lista_cantidades[idx_insumo] = max(lista_cantidades[idx_insumo] - s.getCantidadInsumosBodega()[producto_en_bodega.index], 0)

                    cantidad_necesaria = lista_cantidades[lista_insumos.index(i)]
                    producto_en_otra_sede = Sede.verificarProductoOtraSede(i)
                    if producto_en_otra_sede.getEncontrado():
                        print(f"\nTenemos el insumo {i.nombre} en nuestra {producto_en_otra_sede.sede}.")
                        print(f"El insumo tiene un costo de {producto_en_otra_sede.precio}")
                        print("\nSeleccione una de las siguientes opciones:")
                        print(f"1. Deseo transferir el insumo desde la {producto_en_otra_sede.sede}")
                        print("2. Deseo comprar el insumo")

                        opcion = int(input())
                        if opcion == 1:
                            restante = Sede.transferir_insumo(i, s, producto_en_otra_sede.sede, cantidad_necesaria)
                            print(f"\n{i} transferido desde {s} con éxito")
                            if restante != 0:
                                insumos_a_pedir.append(i)
                                cantidad_a_pedir.append(restante)
                                if i.nombre == "Tela":
                                    print(f"\nTenemos una cantidad de {restante} cm de tela restantes a pedir")
                                elif i.nombre == "Boton":
                                    print(f"\nTenemos una cantidad de {restante} botones restantes a pedir")
                                elif i.nombre == "Cremallera":
                                    print(f"\nTenemos una cantidad de {restante} cremalleras restantes a pedir")
                                else:
                                    print(f"\nTenemos una cantidad de {restante} cm de hilo restantes a pedir")
                            else:
                                print("Insumo transferido en su totalidad")
                        elif opcion == 2:
                            insumos_a_pedir.append(i)
                            cantidad_a_pedir.append(cantidad_necesaria)
                        else:
                            print("Esa opción no es valida.")

            lista_sede.append(insumos_a_pedir)
            lista_sede.append(cantidad_a_pedir)
            lista_a.append(lista_sede)

        return lista_a


    def comprarInsumos(fecha, lista_a):
        from src.gestorAplicacion.bodega.proveedor import Proveedor
        from src.gestorAplicacion.administracion.deuda import Deuda
        deudas = []

        for sede in lista_a:
            insumos = sede[0]
            cantidad = sede[1]

            for sedee in Sede.getlistaSedes():
                for idx_insumo in range(len(insumos)):
                    proveedores = []
                    precios = []
                    mejor_proveedor = None
                    mejor_precio = float('inf')
                    cantidad_añadir = 0

                    for proveedor in Proveedor.getListaProveedores():
                        if proveedor.getInsumo() == insumos[idx_insumo]:
                            proveedores.append(proveedor)
                            precios.append(proveedor.costoDeLaCantidadd(insumos[idx_insumo], cantidad[idx_insumo]))

                    for x in proveedores:
                        precio = x.costoDeLaCantidad(insumos[idx_insumo], cantidad[idx_insumo])
                        if precio != 0 and precio < mejor_precio:
                            mejor_precio = precio
                            mejor_proveedor = x
                            insumos[idx_insumo].setProveedor(x)

                    print(f"\nTenemos el insumo {insumos[idx_insumo].nombre} con nuestro proveedor {insumos[idx_insumo].proveedor.nombre}.")

                    if insumos[idx_insumo].getPrecioIndividual() < insumos[idx_insumo].getUltimoPrecio():
                        print("\nDado que el costo de la venta por unidad es menor al ultimo precio por el que compramos el insumo")
                        print(f"\nDesea pedir mas de la cantidad necesaria para la producción? \nCantidad: {cantidad[idx_insumo]}")
                        print("1. Si")
                        print("2. No")

                        opcion = int(input())
                        if opcion == 1:
                            cantidad_añadir = int(input(f"\nCuanta cantidad más desea pedir del insumo {insumos[idx_insumo].getNombre()}"))
                        elif opcion != 2:
                            print("Esa opción no es valida.")

                    cantidad[idx_insumo] += cantidad_añadir

                    Sede.añadirInsumo(insumos[idx_insumo], sedee, cantidad[idx_insumo])
                    print(f"\nInsumo {insumos[idx_insumo]} comprado con éxito")

                    for proveedor in Proveedor.getListaProveedores():
                        monto_deuda = 0
                        if insumos[idx_insumo].getProveedor().getNombre() == proveedor.getNombre():
                            monto_deuda += insumos[idx_insumo].getPrecioIndividual() * cantidad[idx_insumo]
                        if monto_deuda > 0:
                            if proveedor.getDeuda() is None:
                                deuda = Deuda(fecha, monto_deuda, proveedor.nombre, "Proveedor", Deuda.calcularCuotas(monto_deuda))
                            elif not proveedor.getDeuda().getEstadodePago():
                                proveedor.unificarDeudasXProveedor(fecha, monto_deuda)
                                deuda = proveedor.getDeuda()
                            deudas.append(deuda)

        return f"Ahora nuestras deudas con los proveedores lucen asi:\n{deudas}"
        
    def nextIntSeguro():
        while True:
            respuesta = input()
            if respuesta.isdigit():
                return int(respuesta)
            else:
                print("Por favor ingrese un número entero")

    def dondeRetirar():
        
        print("\n*Seleccione la sede desde donde comprara el Respuesto:\n")
        if Sede.getlistaSedes()[0].getCuentaSede().getAhorroBanco() >= Main.proveedorBdelmain.getPrecio():
            print(f"1. {Sede.getlistaSedes()[0].getNombre()} tiene disponible: {Sede.getlistaSedes()[0].getCuentaSede().getAhorroBanco()}")
        if Sede.getlistaSedes()[1].getCuentaSede().getAhorroBanco() >= Main.proveedorBdelmain.getPrecio():
            print(f"2. {Sede.getlistaSedes()[1].getNombre()} tiene disponible: {Sede.getlistaSedes()[1].getCuentaSede().getAhorroBanco()}")

        opcion = 0
        while opcion != 1 and opcion != 2:
            opcion = int(input())
            if opcion == 1:
                nuevo_dinero_sede = Sede.getlistaSedes()[0].getCuentaSede().getAhorroBanco() - Main.proveedorBdelmain.getInsumo().getPrecioIndividual()
                Sede.getlistaSedes()[0].getCuentaSede().setAhorroBanco(nuevo_dinero_sede)

                print(f"El repuesto se compro exitosamente desde la {Sede.getlistaSedes()[0].getNombre()}, saldo disponible:")
                print(f"{Sede.getlistaSedes()[0].getNombre()} = {Sede.getlistaSedes()[0].getCuentaSede().getAhorroBanco()}")
                print(f"{Sede.getlistaSedes()[1].getNombre()} = {Sede.getlistaSedes()[1].getCuentaSede().getAhorroBanco()}")

            elif opcion == 2:
                nuevo_dinero_sede = Sede.getlistaSedes()[1].getCuentaSede().getAhorroBanco() - Main.proveedorBdelmain.getInsumo().getPrecioIndividual()
                Sede.getlistaSedes()[1].getCuentaSede().setAhorroBanco(nuevo_dinero_sede)

                print(f"El repuesto se compro exitosamente desde la sede {Sede.getlistaSedes()[1].getNombre()}, saldo disponible:")
                print(f"{Sede.getlistaSedes()[0].getNombre()} = {Sede.getlistaSedes()[0].getCuentaSede().getAhorroBanco()}")
                print(f"{Sede.getlistaSedes()[1].getNombre()} = {Sede.getlistaSedes()[1].getCuentaSede().getAhorroBanco()}")
            else:
                print("Opcion incorrecta, marque 1 o 2 segun desee")

    def recibeProveedorB(proveedor_b):
        Main.proveedorBdelmain = proveedor_b

    def recibeProveedorB():
        return Main.proveedorBdelmain

    def vender():
        from ..gestorAplicacion.administracion.empleado import Empleado
        from src.gestorAplicacion.bodega.pantalon import Pantalon
        from src.gestorAplicacion.bodega.camisa import Camisa
        from src.gestorAplicacion.administracion.area import Area
        venta = None
        productos_seleccionados = []
        cantidad_productos = []
        print("\nIngrese la fecha de la venta:")
        fecha_venta = Main.fecha
        print("\nSeleccione el cliente al que se le realizará la venta:")
        Main.imprimirNoEmpleados()  # Muestra la lista de clientes con índices
        cliente_seleccionado = Main.nextIntSeguro()
        no_empleados = [persona for persona in Persona.getListaPersonas() if not isinstance(persona, Empleado)]
        cliente = no_empleados[cliente_seleccionado]

        print("\nSeleccione el número de la sede en la que se encuentra el cliente:")
        for i, sede in enumerate(Sede.getlistaSedes()):
            print(f"{i}. {sede.getNombre()}")
        sede_seleccionada = Main.nextIntSeguro()
        sede = Sede.getlistaSedes()[sede_seleccionada]

        print("\nSeleccione el número del empleado que se hará cargo del registro de la venta:")
        for i, empleado in enumerate(sede.getlistaEmpleados()):
            if empleado.getAreaActual() == Area.OFICINA:
                print(f"{i}. {empleado.getNombre()}")
        encargado_seleccionado = Main.nextIntSeguro()
        encargado = sede.getlistaEmpleados()[encargado_seleccionado]

        print("\nSeleccione el número del empleado que se hará cargo de asesorar la venta:")
        for i, empleado in enumerate(sede.getlistaEmpleados()):
            if empleado.getAreaActual() == Area.VENTAS:
                print(f"{i}. {empleado.getNombre()}")
        vendedor_seleccionado = Main.nextIntSeguro()
        vendedor = sede.getlistaEmpleados()[vendedor_seleccionado]

        costos_envio = 0

        while True:
            print("\nSeleccione el nombre del producto que venderá:")
            print(f"0. Camisa - Precio {Camisa.precioVenta()}")
            print(f"1. Pantalon - Precio {Pantalon.precioVenta()}")
            producto_seleccionado = input()
            prenda_seleccionada = next((prenda for prenda in Sede.getPrendasInventadasTotal() if prenda.getNombre() == producto_seleccionado), None)
            
            if prenda_seleccionada is None:
                print("Producto no encontrado. Intente nuevamente.")
                continue

            nombre_prenda_seleccionada = prenda_seleccionada.getNombre()
            print("Ingrese la cantidad de unidades que se desea del producto elegido:")
            cantidad_prenda = Main.nextIntSeguro()
            cantidad_productos.append(cantidad_prenda)
            cantidad_disponible = sum(1 for prenda in Sede.getPrendasInventadasTotal() if prenda.getNombre() == prenda_seleccionada.getNombre())
            
            Main.manejarFaltantes(sede, cantidad_prenda, cantidad_disponible, nombre_prenda_seleccionada, costos_envio)
            
            if 0 < cantidad_prenda < len(Sede.getPrendasInventadasTotal()):
                eliminadas = 0
                for i in range(len(Sede.getPrendasInventadasTotal())):
                    if eliminadas >= cantidad_prenda:
                        break
                    if Sede.getPrendasInventadasTotal()[i] == prenda_seleccionada:
                        eliminada = Sede.getPrendasInventadasTotal().pop(i)
                        sede.getPrendasInventadas().remove(eliminada)
                        eliminadas += 1
                        i -= 1

            print("\n¿Deseas agregar otro producto a la venta?: (si/no)")
            decision = input().lower()
            if decision == "no":
                print("Selección finalizada")
                break
            if decision != "si":
                break

        suma_precios_prendas = 0
        cantidad_camisas = 0
        cantidad_pantalon = 0
        for prenda in productos_seleccionados:
            if isinstance(prenda, Camisa):
                suma_precios_prendas += Camisa.precioVenta()
                cantidad_camisas += 1
                if cantidad_camisas >= 10:
                    descuento = int(suma_precios_prendas * 0.05)
                    suma_precios_prendas -= descuento
            elif isinstance(prenda, Pantalon):
                suma_precios_prendas += Pantalon.precioVenta()
                cantidad_pantalon += 1
                if cantidad_pantalon >= 10:
                    descuento = int(suma_precios_prendas * 0.05)
                    suma_precios_prendas -= descuento

        IVA = int((costos_envio + suma_precios_prendas) * 0.19)
        venta = Venta(sede, fecha_venta, cliente, vendedor, encargado, productos_seleccionados)
        venta.setCostoEnvio(costos_envio)
        suma_precios_prendas += costos_envio
        monto = suma_precios_prendas + IVA + costos_envio
        monto_pagar = int(monto - (monto * cliente.getMembresia().getPorcentajeDescuento()))
        venta.setMontoPagado(monto_pagar)
        venta.setSubtotal(suma_precios_prendas)
        print(f"Subtotal: {suma_precios_prendas}")
        comision = int(monto_pagar * 0.05)
        vendedor.setRendimientoBonificacion(comision)
        
        return venta 

    def imprimirNoEmpleados():
        from ..gestorAplicacion.administracion.empleado import Empleado
        no_empleados = []
        print("Lista de clientes:")
        for persona in Persona.getListaPersonas():
            if not isinstance(persona, Empleado):
                no_empleados.append(persona)
        index=0
        for persona in no_empleados:
            print(f"{index}. {persona}")
            index+=1

    def realizarVenta(venta):
        from src.gestorAplicacion.bodega.proveedor import Proveedor
        productos_seleccionados = venta.getArticulos()
        sede = venta.getSede()
        banco = sede.getCuentaSede()
        total_prendas = len(productos_seleccionados)

        insumos_bodega = sede.getListaInsumosBodega()
        cantidad_insumos_bodega = sede.getCantidadInsumosBodega()

        bolsas_seleccionadas = []
        capacidad_total = 0

        while capacidad_total < total_prendas:
            print("\nSeleccione el tamaño de bolsa:")
            bp, bm, bg = False, False, False
            for i in range(len(insumos_bodega)):
                bolsa = insumos_bodega[i]
                if isinstance(bolsa, Bolsa):
                    capacidad = bolsa.getCapacidadMaxima()
                    cantidad = sede.getCantidadInsumosBodega()[i]
                    if capacidad == 1 and cantidad > 0:
                        bp = True
                    if capacidad == 3 and cantidad > 0:
                        bm = True
                    if capacidad == 8 and cantidad > 0:
                        bg = True

            if bp: print("1. Bolsa pequeña (1 producto)")
            if bm: print("2. Bolsa mediana (3 productos)")
            if bg: print("3. Bolsa grande (8 productos)")

            opcion_bolsa = Main.nextIntSeguro()

            capacidad_bolsa = 0
            nombre_bolsa = None
            if opcion_bolsa == 1:
                capacidad_bolsa = 1
                nombre_bolsa = "Bolsa pequeña"
            elif opcion_bolsa == 2:
                capacidad_bolsa = 3
                nombre_bolsa = "Bolsa mediana"
            elif opcion_bolsa == 3:
                capacidad_bolsa = 8
                nombre_bolsa = "Bolsa grande"
            else:
                print("Opción inválida. Intente nuevamente.")
                continue

            bolsa_encontrada = False
            cantidad_disponible = 0
            capacidad_total += capacidad_bolsa
            for i in range(len(sede.getListaInsumosBodega())):
                insumo = sede.getListaInsumosBodega()[i]
                if isinstance(insumo, Bolsa) and insumo.getCapacidadMaxima() == capacidad_bolsa:
                    cantidad_disponible += cantidad_insumos_bodega[i]
                    if cantidad_disponible > 0:
                        bolsas_seleccionadas.append(insumo)
                        cantidad_insumos_bodega[i] -= 1
                        bolsa_encontrada = True
                        break
                total_prendas -= cantidad_disponible
                if capacidad_total == total_prendas:
                    break

            for revisar_sede in Sede.getlistaSedes():
                lista_insumos = revisar_sede.getListaInsumosBodega()
                cantidad_insumos = revisar_sede.getCantidadInsumosBodega()
                for i in range(len(lista_insumos)):
                    insumo=lista_insumos[i]
                    if isinstance(insumo, Bolsa) and cantidad_insumos[i] < 10:
                        print(f"La sede {revisar_sede.getNombre()} tiene menos de 10 bolsas en stock (Cantidad: {cantidad_insumos[i]}).")
                        print("Comprando al proveedor...")
                        for e in range(len(lista_insumos)):
                            insumo=lista_insumos[e]    
                            if isinstance(insumo, Bolsa) and insumo.getNombre() == nombre_bolsa:
                                print(f"¿Cuántas bolsas de {insumo.getNombre()} desea comprar?")
                                cantidad_comprar = Main.nextIntSeguro()
                                costo_compra = Proveedor.costoDeLaCantidad(insumo, cantidad_comprar)
                                banco.setAhorroBanco(banco.getAhorroBanco() - costo_compra)
                                cantidad_insumos_bodega[e] += cantidad_comprar
                                insumo.setPrecioCompra(costo_compra)
                                insumo.setPrecioCompra(costo_compra)
                                print(f"Se compraron {cantidad_comprar} {nombre_bolsa} por un costo total de {costo_compra}")
                                break

        venta.setBolsas(bolsas_seleccionadas)
        total_venta = venta.getMontoPagado() + len(bolsas_seleccionadas) * 2000
        venta.setMontoPagado(total_venta)

        print(f"\nVenta realizada. Total de la venta con bolsas: {total_venta}")
        return venta
    
    
    
    def manejarFaltantes(sede, cantidad_prenda, disponibles, tipo_prenda, costos_envio):
        faltantes = cantidad_prenda - disponibles

        if faltantes > 0:
            costos_envio += 3000 + (faltantes * 1000)
            print("Valor de costos de envío: " + str(costos_envio))
            prendas_transferidas = 0
            for otra_sede in Sede.getlistaSedes():
                if otra_sede != sede:
                    for prenda in otra_sede.getPrendasInventadas():
                        if prenda.getNombre() == tipo_prenda and prendas_transferidas < faltantes:
                            otra_sede.getPrendasInventadas().remove(prenda)
                            sede.getPrendasInventadas().append(prenda)
                            prendas_transferidas += 1

                    if prendas_transferidas == faltantes:
                        break

            if prendas_transferidas < faltantes:
                print("No se pudieron transferir todas las prendas faltantes. Faltan " + str(faltantes - prendas_transferidas) + " unidades.")
    
    def tarjetaRegalo (venta):
                    from src.gestorAplicacion.bodega.pantalon import Pantalon
                    
                    from src.gestorAplicacion.bodega.camisa import Camisa
                    sede = venta.getSede()
                    banco = sede.getCuentaSede()

                    print("\n¿Desea usar una tarjeta de regalo? (si/no)")
                    respuesta = input().lower()
                    nuevo_intento = 1
                    while nuevo_intento == 1:
                        if respuesta == "si":
                            print("Ingrese el código de la tarjeta de regalo:")
                            codigo_ingresado = int(input())

                            if codigo_ingresado in Venta.getCodigosRegalo():
                                print("Código válido. Procesando tarjeta de regalo...")
                                indice = Venta.getCodigosRegalo().index(codigo_ingresado)
                                monto_tarjeta = Venta.getMontosRegalo()[indice]
                                monto_venta = venta.getMontoPagado()

                                if monto_tarjeta >= monto_venta:
                                    print("El monto de la tarjeta cubre la totalidad de la venta.")
                                    saldo_restante = monto_tarjeta - monto_venta
                                    Venta.getMontosRegalo()[indice] = saldo_restante
                                    venta.setMontoPagado(0)

                                    print("Venta pagada con tarjeta de regalo.")
                                    print("Saldo restante en la tarjeta de regalo: $" + str(saldo_restante))
                                else:
                                    monto_faltante = monto_venta - monto_tarjeta
                                    Venta.getMontosRegalo()[indice] = 0
                                    venta.setMontoPagado(monto_faltante)
                                    print("El monto de la tarjeta no es suficiente para cubrir la venta.")
                                    print("Monto restante a pagar: $" + str(monto_faltante))

                                if Venta.getMontosRegalo()[indice] == 0:
                                    Venta.getCodigosRegalo().pop(indice)
                                    Venta.getMontosRegalo().pop(indice)
                                    print("La tarjeta de regalo se ha agotado y ha sido desactivada.")

                                nuevo_intento = 2
                            else:
                                print("El código ingresado no es válido. Por favor, intentar de nuevo o pagar el monto total")
                                print("Ingresa 1 para intentar de nuevo.")
                                print("Ingresa 2 para salir del intento")
                                nuevo_intento = Main.nextIntSeguro()
                        elif respuesta == "no":
                            nuevo_intento -= 1
                            break

                    print("\n¿Desea comprar una tarjeta de regalo? (si/no)")
                    compra_tarjeta = input().lower()

                    if compra_tarjeta == "si":
                        print("¿Por cuánto será la tarjeta de regalo? (monto en pesos)")
                        monto_tarjeta = Main.nextIntSeguro()
                        codigo_generado = Main.generarCodigoAleatorio()
                        Venta.getCodigosRegalo().append(codigo_generado)
                        Venta.getMontosRegalo().append(monto_tarjeta)
                        banco.setAhorroBanco(banco.getAhorroBanco() + monto_tarjeta)

                        print("Tarjeta de regalo generada exitosamente.")
                        print("Código: " + codigo_generado)
                        print("Monto: $" + str(monto_tarjeta))

                    ingreso = venta.getMontoPagado()
                    print("Ingreso calculado: $" + str(ingreso))
                    banco.setAhorroBanco(banco.getAhorroBanco() + ingreso)

                    print("Monto total en la cuenta de la sede: $" + str(banco.getAhorroBanco()))
                    banco_recibir = Banco.getCuentaPrincipal()
                    banco_transferir = sede.getCuentaSede()
                    if banco_transferir != banco_recibir:
                        print("\n¿Desea transferir fondos a la cuenta principal? (si/no)")
                        transferir_fondos = input().lower()
                        if transferir_fondos == "si":
                            print("¿Qué porcentaje desea transferir? (20% o 60%)")
                            porcentaje = Main.nextIntSeguro()
                            if porcentaje == 20 or porcentaje == 60:
                                monto_transferencia = (banco_transferir.getAhorroBanco() * porcentaje / 100) - 50000
                                if monto_transferencia > 0:
                                    if banco_recibir.getNombreCuenta() == "principal":
                                        banco_recibir.setAhorroBanco(banco_transferir.getAhorroBanco() - (monto_transferencia + 50000))
                                        banco_recibir.setAhorroBanco(banco_recibir.getAhorroBanco() + monto_transferencia)
                                        print("Transferencia exitosa.")
                                        print("Monto transferido: $" + str(monto_transferencia))
                                        print("Costo de transferencia: $50000")
                                else:
                                    print("Fondos insuficientes para cubrir la transferencia y el costo.")
                            else:
                                print("Porcentaje no válido. No se realizará la transferencia.")

                    if banco_transferir is not None:
                        print("Estado final de la cuenta de la sede: $" + str(banco_transferir.getAhorroBanco()))
                    if banco_recibir is not None:
                        print("Estado final de la cuenta principal: $" + str(banco_recibir.getAhorroBanco()))

                    productos_seleccionados = venta.getArticulos()
                    monto_pagar = venta.getMontoPagado()
                    tasa_iva = 0.19
                    valor_base = int(monto_pagar / (1 + tasa_iva))
                    iva = monto_pagar - valor_base
                    print("\n---- FACTURA ----")
                    print("Prendas compradas:")
                    cantidad_camisas = 0
                    cantidad_pantalon = 0
                    subtotal_camisas = 0
                    subtotal_pantalon = 0

                    for prenda in productos_seleccionados:
                        if isinstance(prenda, Camisa):
                            cantidad_camisas += 1
                            subtotal_camisas += Camisa.precioVenta()
                        if isinstance(prenda, Pantalon):
                            cantidad_pantalon += 1
                            subtotal_pantalon += Pantalon.precioVenta()

                    camisa_encontrada = False
                    pantalon_encontrado = False
                    for prenda in productos_seleccionados:
                        if isinstance(prenda, Camisa) and not camisa_encontrada:
                            print(prenda.getNombre() + " - Cantidad: " + str(cantidad_camisas) + " - Subtotal: $" + str(subtotal_camisas))
                            camisa_encontrada = True
                        if isinstance(prenda, Pantalon) and not pantalon_encontrado:
                            print(prenda.getNombre() + " - Cantidad: " + str(cantidad_pantalon) + " - Subtotal: $" + str(subtotal_pantalon))
                            pantalon_encontrado = True

                    print("Valor total a pagar: $" + str(monto_pagar))
                    print("Subtotal prendas: $" + str(venta.getsubtotal()))
                    print("IVA: $" + str(iva))
                    print("Venta registrada por: " + venta.getEncargado())
                    print("Asesor de la compra: " + venta.getAsesor())

                    return "El monto total a pagar por parte del cliente es " + str(monto_pagar) + " y el estado final de la cuenta de la sede es $" + str(banco_transferir.getAhorroBanco())    
        
    def generarCodigoAleatorio():
        caracteres = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        while True:
            codigo = ''.join(random.choice(caracteres) for _ in range(8))
            if codigo not in Venta.getCodigosRegalo():
                return codigo

    def actualizarProveedores():
        from src.gestorAplicacion.bodega.proveedor import Proveedor
        sede_p = next((sede for sede in Sede.getlistaSedes() if sede.getNombre() == "Sede Principal"), None)
        if sede_p:
            for insumo in sede_p.getListaInsumosBodega():
                compatibles = [prov for prov in Proveedor.getListaProveedores() if prov.getInsumo().getNombre() == insumo.getNombre()]
                nuevos = compatibles[:]
                random.shuffle(nuevos)
                for i, prov in enumerate(compatibles):
                    prov.setPrecio(nuevos[i].getPrecio())

    def pedirModista(cantidad_prendas, sede, idx_tanda):
        print(f"Seleccione el modista que se encargará de la tanda #{idx_tanda} de producción de {cantidad_prendas} prendas en {sede.getNombre()}:")
        modistas = [empleado for empleado in sede.getlistaEmpleados() if empleado.getRol() == Rol.MODISTA]
        for i, modista in enumerate(modistas):
            print(f"{i}. {modista.getNombre()}")
        while True:
            seleccion = Main.nextIntSeguro()
            if 0 <= seleccion < len(modistas):
                return modistas[seleccion]
            else:
                print("Opción inválida. Intente nuevamente.")

    def prints_int2(senall):
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

    def prints_int1(signal, rep):
        if signal == 1:
            print(f"*{rep.getNombre()} se debe cambiar.\n")
        elif signal == 2:
            print(f"*El proveedor mas barato se llama '{Main.proveedorBdelmain.getNombre()}', y lo vende a: {Main.proveedorBdelmain.getPrecio()}\n")

    def prints_int11(rep, maq, sede, senal):
        if senal == 1:
            print(f"Repuesto: '{rep.getNombre()}' añadido correctamente a la {maq.getNombre()}, de la: {sede.getNombre()}")
        elif senal == 2:
            print("Ninguna de las sedes cuenta con dinero suficiente, considere pedir un prestamo.")
        elif senal == 3:
            print(f"\n--> Por ende, la {maq.getNombre()} de la {maq.getSede().getNombre()}, se encuentra inhabilitada.")

    def prints_int111(maq, senal):
        if senal == 4:
            print(f"\n--> La {maq.getNombre()} de la {maq.getSede().getNombre()} requiere mantenimiento.\n")
        #can you please translate this to python
    
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
    
    def crearSedesMaquinasRepuestos():
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
        p33 = Proveedor(44000, "Tinta por aqui")
        p33.setInsumo(Insumo("Tinta Negra Impresora", p33))
        p34 = Proveedor(50000, "El tintoso")
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
        AgujasMC = Repuesto("Agujas de la Maquina de coser", 12, p13)
        Aceite = Repuesto("Aceite", 60, p16)

        Cuchillas = Repuesto("Cuchillas", 60, p19)
        Afiladores = Repuesto("Afiladores", 750, p22)

        ResistenciaElectrica = Repuesto("Resistencia Electrica", 1500, p25)
        MangueraDeVapor = Repuesto("Manguera de Vapor", 750, p27, 1)

        AgujasBI = Repuesto("Agujas de la Bordadora Industrial", 25, p29)

        BandasDeTransmision = Repuesto("Bandas de Transmision", 2500, p31)

        TintaN = Repuesto("Tinta Negra Impresora", 3000, p33, 1)

        Lector = Repuesto("Lector de barras", 3000, p35)
        PapelQuimico = Repuesto("Papel quimico", 72, p37)

        Cargador = Repuesto("Cargador Computador", 6000, p39)
        Mouse = Repuesto("Mouse Computador", 9000, p41)

        # CREACION DE LAS SEDES QUE MANEJAREMOS, CON SUS RESPECTIVAS MAQUINAS EN CADA
        # UNA DE ELLAS
        sedeP = Sede("Sede Principal")
        sede2 = Sede("Sede 2")

        # AGRUPACION DE LOS REPUESTOS EN LISTAS PARA ENVIARLOS A LAS MAQUINAS
        # CORRESPONDIENTES
        repuestosMC = []
        repuestosMCorte = []
        repuestosPI = []
        repuestosBI = []
        repuestosMTermofijado = []
        repuestosMTijereado = []
        repuestosImp = []
        repuestosRe = []
        repuestosComp = []

        repuestosMC2 = []
        repuestosMCorte2 = []
        repuestosPI2 = []
        repuestosBI2 = []
        repuestosMTermofijado2 = []
        repuestosMTijereado2 = []
        repuestosImp2 = []
        repuestosRe2 = []
        repuestosComp2 = []

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
        BordadoraIndustrial = Maquinaria("Bordadora Industrial", 31000000, 500, repuestosBI, sedeP, "s")
        MaquinaDeTermofijado = Maquinaria("Maquina de Termofijado", 20000000, 1000,repuestosMTermofijado, sedeP)
        MaquinaDeTijereado = Maquinaria("Maquina de Tijereado", 5000000, 600, repuestosMTijereado,sedeP)
        Impresora = Maquinaria("Impresora", 800000, 2000, repuestosImp, sedeP)
        Registradora = Maquinaria("Caja Registradora", 700000, 17000, repuestosRe, sedeP)
        Computador = Maquinaria("Computador", 2_000_000, 10000, repuestosImp, sedeP)

        # sede2
        MaquinaDeCoser2 = Maquinaria("Maquina de Coser Industrial", 4250000, 600, repuestosMC2, sede2, 1)
        MaquinaDeCorte2 = Maquinaria("Maquina de Corte", 6000000, 700, repuestosMCorte2, sede2, False)
        PlanchaIndustrial2 = Maquinaria("Plancha Industrial", 2000000, 900, repuestosPI2, sede2, 1)
        BordadoraIndustrial2 = Maquinaria("Bordadora Industrial", 31000000, 500, repuestosBI2, sede2, 1)
        MaquinaDeTermofijado2 = Maquinaria("Maquina de Termofijado", 20000000, 1000,repuestosMTermofijado2, sede2, 1)
        MaquinaDeTijereado2 = Maquinaria("Maquina de Tijereado", 5000000, 600, repuestosMTijereado2,
                sede2, 1)
        Impresora2 = Maquinaria("Impresora", 800000, 2000, repuestosImp2, sede2, 1)
        Registradora2 = Maquinaria("Caja Registradora", 700000, 17000, repuestosRe2, sede2, 1)
        Computador2 = Maquinaria("Computador", 2_000_000, 10000, repuestosImp2, sede2, 1)

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
        d1.setEstadodePago(True)
        d1.setCapitalPagado(20_000_000)
        d2 = Deuda(Fecha(15, 1, 20), 100_000_000, "Banco Montreal", "Banco", 18)
        d2.setCapitalPagado(100_000_000 / 2)
        b1.actualizarDeuda(d2)
        b2.actualizarDeuda(Deuda(Fecha(10, 1, 24), 5_000_000, "Banco de Bogotá", "Banco", 10))
        tm.actualizarDeuda(Deuda(Fecha(30, 9, 22), 150_000_000, "Inversiones Terramoda", "Banco", 18))
        tm.actualizarDeuda(Deuda(Fecha(20, 2, 23), 800_000, "Inversiones Terramoda", "Banco", 18))

        i1 = Insumo("Tela", 1 * 20, p5, sedeP)
        i2 = Insumo("Tela", 1 * 20, p5, sede2)
        i3 = Insumo("Boton", 4 * 20, p3, sedeP)
        i4 = Insumo("Boton", 4 * 20, p3, sede2)
        i5 = Insumo("Cremallera", 1 * 20, p4, sedeP)
        i6 = Insumo("Cremallera", 1 * 20, p4, sede2)
        i7 = Insumo("Hilo", 100 * 20, p2, sedeP)
        i8 = Insumo("Hilo", 100 * 20, p2, sede2)
        i9 = Bolsa("Bolsa", 1 * 20, p10, sedeP, 8)
        i10 = Bolsa("Bolsa", 1 * 20, p10, sede2, 8)
        i11 = Bolsa("Bolsa", 1 * 20, p10, sedeP, 3)
        i12 = Bolsa("Bolsa", 1 * 20, p10, sede2, 3)
        i13 = Bolsa("Bolsa", 1 * 20, p10, sedeP, 1)
        i14 = Bolsa("Bolsa", 1 * 20, p10, sede2, 1)

        betty = Empleado(Area.DIRECCION, Fecha(1, 1, 23), sedeP, "Beatriz Pinzón", 4269292,
                Rol.PRESIDENTE, 10, Membresia.NULA, Computador)
        Armando = Empleado(Area.DIRECCION, Fecha(30, 11, 20), sedeP, "Armando Mendoza", 19121311,
                Rol.PRESIDENTE, 15, Membresia.PLATA, Computador.copiar())
        Cata = Empleado(Area.OFICINA, Fecha(1, 6, 16), sedeP, "Catalina Ángel", 7296957, Rol.ASISTENTE,
                20, Membresia.ORO, Impresora)
        Mario = (Empleado(Area.OFICINA, Fecha(30, 11, 20), sedeP, "Mario Calderón", 19256002,
                Rol.EJECUTIVO, 4, Membresia.PLATA, Impresora.copiar()))
        Hugo = (Empleado(Area.CORTE, Fecha(1, 5, 14), sedeP, "Hugo Lombardi", 7980705, Rol.DISEÑADOR,
                20, Membresia.ORO, MaquinaDeCorte))
        Inez = (Empleado(Area.CORTE, Fecha(1, 5, 14), sedeP, "Inez Ramirez", 23103023, Rol.MODISTA, 2,
                Membresia.NULA, MaquinaDeCoser))
        Aura = (Empleado(Area.VENTAS, Fecha(1, 2, 23), sedeP, "Aura Maria", 4146118, Rol.SECRETARIA, 2,
                Membresia.NULA, Registradora))
        Sandra = (Empleado(Area.CORTE, Fecha(15, 9, 23), sedeP, "Sandra Patiño", 5941859, Rol.MODISTA,
                5, Membresia.NULA, PlanchaIndustrial))
        Sofia = (Empleado(Area.CORTE, Fecha(30, 9, 22), sedeP, "Sofía Lopez", 5079239, Rol.MODISTA, 6,
                Membresia.NULA, MaquinaDeTermofijado))
        Mariana = (Empleado(Area.CORTE, Fecha(1, 5, 23), sedeP, "Mariana Valdéz", 4051807, Rol.MODISTA,
                10, Membresia.BRONCE, MaquinaDeTijereado))
        Bertha = (Empleado(Area.CORTE, Fecha(25, 2, 20), sedeP, "Bertha Muñoz", 7137741, Rol.MODISTA,
                15, Membresia.BRONCE, BordadoraIndustrial))
        Wilson = (Empleado(Area.VENTAS, Fecha(4, 4, 22), sedeP, "Wilson Sastoque", 9634927, Rol.PLANTA,
                5, Membresia.NULA, Registradora.copiar()))

        Gutierrez = (Empleado(Area.DIRECCION, Fecha(5, 8, 19), sede2, "Saul Gutierrez", 9557933,
                Rol.EJECUTIVO, 11, Membresia.NULA, Computador2))
        Marcela = (Empleado(Area.DIRECCION, Fecha(30, 11, 20), sede2, "Marcela Valencia", 8519803,
                Rol.EJECUTIVO, 10, Membresia.ORO, Computador2.copiar(1)))
        Gabriela = (Empleado(Area.VENTAS, Fecha(1, 1, 24), sede2, "Gabriela Garza", 5287925,
                Rol.VENDEDOR, 9, Membresia.PLATA, Registradora2))
        Patricia = (Empleado(Area.OFICINA, Fecha(5, 2, 23), sede2, "Patricia Fernandez", 4595311,
                Rol.SECRETARIA, 6, Membresia.BRONCE, Impresora2))
        Kenneth = (Empleado(Area.CORTE, Fecha(1, 1, 24), sede2, "Kenneth Johnson", 7494184,
                Rol.MODISTA, 8, Membresia.ORO, PlanchaIndustrial2))
        Robles = (Empleado(Area.OFICINA, Fecha(12, 10, 24), sede2, "Miguel Robles", 7518004,
                Rol.VENDEDOR, 7, Membresia.BRONCE, Impresora2.copiar(1)))
        Alejandra = (Empleado(Area.CORTE, Fecha(1, 2, 24), sede2, "Alejandra Zingg", 6840296,
                Rol.MODISTA, 2, Membresia.BRONCE, BordadoraIndustrial2))
        Cecilia = (Empleado(Area.CORTE, Fecha(1, 2, 23), sede2, "Cecilia Bolocco", 7443886,
                Rol.MODISTA, 10, Membresia.PLATA, MaquinaDeCoser2))
        Freddy = (Empleado(Area.VENTAS, Fecha(31, 1, 22), sede2, "Freddy Contreras", 6740561,
                Rol.PLANTA, 5, Membresia.NULA, Registradora2.copiar(1)))
        Adriana = (Empleado(Area.CORTE, Fecha(18, 6, 25), sede2, "Adriana arboleda", 5927947,
                Rol.MODISTA, 20, Membresia.ORO, MaquinaDeCorte2))
        Karina = (Empleado(Area.CORTE, Fecha(9, 3, 25), sede2, "Karina Larson", 5229381, Rol.MODISTA,
                2, Membresia.PLATA, MaquinaDeTermofijado2))
        Jenny = (Empleado(Area.CORTE, Fecha(1, 8, 24), sede2, "Jenny Garcia", 4264643, Rol.MODISTA, 1,
                Membresia.ORO, MaquinaDeTijereado2))
        ol = Empleado(Area.DIRECCION, Fecha(1, 2, 20), sede2, "Gustavo Olarte", 7470922, Rol.EJECUTIVO,
                3, Membresia.NULA, Computador2.copiar(1))
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
        tiposp = []
        cantidadesp = []
        tiposc = []
        cantidadesc = []
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

import src.uiMain.bienvenida as bienvenida
# Este metodo termina al presionar "seguir a la ventana principal"
bienvenida.bienvenida()

import src.uiMain.startFrame as startFrame
