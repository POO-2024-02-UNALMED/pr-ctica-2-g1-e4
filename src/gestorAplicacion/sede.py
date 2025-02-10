from src.gestorAplicacion.administracion.resultado import Resultado
from src.gestorAplicacion.administracion.rol import Rol
from src.gestorAplicacion.bodega.insumo import Insumo
from .administracion.area import Area
from .fecha import Fecha
from .venta import Venta
from .bodega.maquinaria import Maquinaria
from typing import List



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

    