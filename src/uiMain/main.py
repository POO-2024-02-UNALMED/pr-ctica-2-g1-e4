import math
import random
from src.gestorAplicacion.administracion.area import Area
from src.gestorAplicacion.administracion.banco import Banco
from src.gestorAplicacion.administracion.deuda import Deuda
from src.gestorAplicacion.administracion.evaluacionFinanciera import EvaluacionFinanciera
from src.gestorAplicacion.administracion.rol import Rol
from src.gestorAplicacion.bodega.bolsa import Bolsa
from src.gestorAplicacion.bodega.camisa import Camisa
from src.gestorAplicacion.bodega.maquinaria import Maquinaria
from src.gestorAplicacion.bodega.pantalon import Pantalon
from src.gestorAplicacion.bodega.prenda import Prenda
from src.gestorAplicacion.bodega.proveedor import Proveedor
from src.gestorAplicacion.fecha import Fecha
from src.gestorAplicacion.venta import Venta
from ..gestorAplicacion.administracion import Empleado
from ..gestorAplicacion import Persona, Sede
import locale
from typing import List

locale.setlocale(locale.LC_ALL, 'es_ES')
comparador = locale.strxfrm

class Main:

    def main():
        fecha = Main.ingresarFecha()
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
                despedidos = Main.despedirEmpleados(fecha)
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
                sede.getHistorialVentas().add(venta)
            elif opcion == 5:
                maquina = Maquinaria()
                sedePrueba = Sede() 
                plan = sedePrueba.planProduccion(maquina.agruparMaquinasDisponibles(fecha), fecha)
                creadas = Prenda.producirPrendas(plan,fecha)
                if (creadas):
                    print(Prenda.getCantidadUltimaProduccion()+" Prendas creadas con éxito")
                else:
                    print("No se pudo producir todo, los insumos no alcanzaron, producimos "+Prenda.getCantidadUltimaProduccion()+" prendas")
                
            #elif opcion == 6:
                #Serializador.serializar()
                #sys.exit(0)
                
            else:
                print("Esa opción no es valida.")

    def ingresarFecha():
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
        print(f"No se pudo producir {tipo_prenda} en la sede {sede.getNombre()} por falta de insumos en la fecha {fecha}.")
        print(f"Hasta el momento se ha usado {Prenda.getCantidadTelaUltimaProduccion()} en tela.")

    def despedirEmpleados(fecha):
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
                    if comparador.compare(emp.getNombre(), nombre) == 0:
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
                nombre = in_stream.readline().strip()
                for persona in aptos:
                    if comparador.compare(persona.getNombre(), nombre) == 0:
                        a_contratar.append(persona)
                        print(f"Seleccionaste a {persona.getNombre()} con {persona.calcularSalario() - persona.valorEsperadoSalario()} de diferencia salarial sobre el promedio")

        Persona.contratar(a_contratar, a_reemplazar, fecha)

    def errorDeReemplazo(persona):
        print(f"No se pudo contratar a {persona.getNombre()}, no sabemos a quien reemplaza.")

    def calcularBalanceAnterior(fecha):
        print("\nObteniendo balance entre Ventas y Deudas para saber si las ventas cubren los gastos de la producción de nuestras prendas...")
        balance_costos_produccion = Venta.calcular_balance_venta_produccion(fecha)
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
                                deuda = Deuda(fecha, monto_deuda, proveedor.nombre, "Proveedor", Deuda.calcular_cuotas(monto_deuda))
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
                            sede.getPrendasInventadas().add(prenda)
                            prendas_transferidas += 1

                    if prendas_transferidas == faltantes:
                        break

            if prendas_transferidas < faltantes:
                print("No se pudieron transferir todas las prendas faltantes. Faltan " + str(faltantes - prendas_transferidas) + " unidades.")
    
    def tarjetaRegalo (venta):
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
        sede_p = next((sede for sede in Sede.getlistaSedes() if sede.getNombre() == "Sede Principal"), None)
        if sede_p:
            for insumo in sede_p.getListaInsumosBodega():
                compatibles = [prov for prov in Proveedor.get_lista_proveedores() if prov.getInsumo().getNombre() == insumo.getNombre()]
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