from abc import ABC, abstractmethod

from src.gestorAplicacion.administracion.gastoMensual import GastoMensual
from src.gestorAplicacion.bodega.camisa import Camisa
from src.gestorAplicacion.bodega.maquinaria import Maquinaria
from src.gestorAplicacion.bodega.pantalon import Pantalon
from src.gestorAplicacion.sede import Sede
from src.gestorAplicacion.venta import Venta
from src.uiMain.main import Main

class Prenda(ABC,GastoMensual):
    porcentajeGanancia = 0.40
    cantidadUltimaProduccion = 0
    cantidadTelaUltimaProduccion = 0
    

    def __init__(self, fecha, sede, nombre, modista, descartada, terminada, insumos):
        self.fecha_fabricacion = fecha
        self.sede = sede
        self.nombre = nombre
        self.modista = modista
        self.descartada = descartada
        self.terminada = terminada
        self.insumo = insumos
        self.costo_insumos = sum(insumo.precio_individual for insumo in insumos)
        self.costo_produccion = self.calcularCostoProduccion()
        self.precio = 0
        self.en_stock = []
        self.ultimo_paso = []

        if descartada:
            modista.prendas_descartadas += 1
        elif terminada:
            modista.prendas_producidas += 1

    @staticmethod
    def producirPrendas(plan_produccion, hoy):
        Prenda.cantidadTelaUltimaProduccion = 0
        Prenda.cantidadUltimaProduccion = 0
        dia_de_produccion = hoy
        alcanza_insumos = True

        for dia in plan_produccion:
            for i, sede in enumerate(Sede.lista_sedes):
                if not Prenda.producirListaPrendas(dia[i], sede, dia_de_produccion):
                    alcanza_insumos = False
            dia_de_produccion = dia_de_produccion.diaSiguiente()

        return alcanza_insumos

    @staticmethod
    def producirListaPrendas(plan_produccion, sede, fecha_produccion):
        alcanza_insumos = True
        cantidad_pantalones = plan_produccion[0]
        cantidad_camisas = plan_produccion[1]
        prendas = []

        insumos_pantalon = sede.insumos_por_nombre(Pantalon.tipo_insumo())
        for _ in range(cantidad_pantalones):
            if sede.quitar_insumos(insumos_pantalon, Pantalon.cantidad_insumo()):
                Prenda.cantidadTelaUltimaProduccion += Pantalon.cantidad_insumo()[Pantalon.tipo_insumo().index("Tela")]
                pantalon = Pantalon(fecha_produccion, sede, insumos_pantalon)
                prendas.append(pantalon)
            else:
                alcanza_insumos = False
                Main.avisar_falta_de_insumos(sede, fecha_produccion, "Pantalon")
                break

        insumos_camisa = sede.insumos_por_nombre(Camisa.tipo_insumo())
        for _ in range(cantidad_camisas):
            if sede.quitar_insumos(insumos_camisa, Camisa.cantidad_insumo()):
                Prenda.cantidadTelaUltimaProduccion += Camisa.cantidad_insumo()[Camisa.tipo_insumo().index("Tela")]
                camisa = Camisa(fecha_produccion, sede, insumos_camisa)
                prendas.append(camisa)
            else:
                alcanza_insumos = False
                Main.avisar_falta_de_insumos(sede, fecha_produccion, "Camisa")
                break

        idx_tanda = 0
        while prendas:
            tandas = [[] for _ in range(7)]
            for prenda in prendas:
                siguiente_paso = prenda.siguiente_paso()
                paso = siguiente_paso[0].lower()
                if paso == "maquina de corte":
                    tandas[3].append(prenda)
                elif paso == "maquina de tijereado":
                    tandas[4].append(prenda)
                elif paso == "maquina de coser industrial":
                    tandas[5].append(prenda)
                elif paso == "maquina de bordadora":
                    tandas[1].append(prenda)
                elif paso == "maquina de termofijado":
                    tandas[0].append(prenda)
                elif paso == "plancha industrial":
                    tandas[2].append(prenda)
                elif paso == "bordadora industrial":
                    tandas[6].append(prenda)

            modista = Main.pedir_modista(len(prendas), sede, idx_tanda)
            for tanda in tandas:
                if not tanda:
                    continue
                maquina = Maquinaria.seleccionar_de_tipo(sede, tanda[0].ultimo_paso[0])
                for prenda in tanda:
                    maquina.usar(prenda.ultimo_paso[1])
                    resultado = prenda.realizar_paso(modista)
                    if resultado == "DESCARTAR":
                        prenda.descartada = True
                        modista.prendas_descartadas += 1
                        prendas.remove(prenda)
                    elif resultado == "LISTO":
                        prenda.terminada = True
                        modista.prendas_producidas += 1
                        prendas.remove(prenda)
                        Prenda.cantidadUltimaProduccion += 1
            idx_tanda += 1

        return alcanza_insumos

    @abstractmethod
    def siguientePaso(self):
        pass

    @abstractmethod
    def realizarPaso(self, modista):
        pass

    @staticmethod
    def gastoMensualClase(fecha):
        gasto_prenda = 0
        gasto_actual = 0
        gasto_pasado = 0
        for prenda in Sede.prendas_inventadas_total:
            lista = prenda.gasto_mensual_tipo(fecha, prenda.fecha_fabricacion)
            gasto_actual += lista[0]
            gasto_pasado += lista[1]
        gasto_prenda = gasto_actual if gasto_actual != 0 else gasto_pasado
        return gasto_prenda

    @staticmethod
    def prevenciones(descuento, nuevo_descuento, fecha):
        for sede in Sede.lista_sedes:
            for prenda in sede.prendas_inventadas:
                if descuento > 0.0 or nuevo_descuento > 0.0:
                    if nuevo_descuento > 0.0:
                        Prenda.porcentajeGanancia -= Prenda.porcentajeGanancia * (1 - nuevo_descuento)
                    Venta.pesimismo -= 0.05
                else:
                    Venta.pesimismo += 0.1
        return Venta.pesimismo

    def calcularCostoInsumos(self):
        self.costo_insumos = sum(insumo.precio_individual * cantidad for insumo, cantidad in zip(self.insumo, self.cantidad_insumo()))
        return self.costo_insumos

    def calcularCostoProduccion(self):
        sum_salarios = sum(empleado.rol.salario_inicial for empleado in self.sede.lista_empleados if empleado.rol == Rol.MODISTA)
        self.costo_produccion = round(sum_salarios * 0.01)
        return self.costo_produccion

    def calcularPrecio(self):
        costo_total = self.costo_insumos + self.costo_produccion
        ganancia_deseada = costo_total + (costo_total * Prenda.porcentajeGanancia)
        self.precio = round(ganancia_deseada)
        return self.precio

    def __str__(self):
        return f"La prenda de tipo {self.nombre}"
    
    def getPrendasDescartadas(self):
        return self.descartada
    
    def getNombre(self):
        return self.nombre
    
    def getInsumo(self):
        return self.insumo
    
    @classmethod
    def getCantidadInsumo(cls):
        return cls.cantidadInsumo
    
    def getCostoInsumos(self):
        return self.costoInsumos
    
    def getPrecio(self) :
        return self.precio
    
    @classmethod
    def getCantidadUltimaProduccion(cls):
        return cls.cantidadUltimaProduccion
    

    @classmethod
    def getCantidadTelaUltimaProduccion(cls):
        return cls.cantidadTelaUltimaProduccion
    