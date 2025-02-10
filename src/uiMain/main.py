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
