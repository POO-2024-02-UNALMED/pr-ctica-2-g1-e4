from src.gestorAplicacion.administracion.empleado import Empleado
from src.gestorAplicacion.bodega.prenda import Prenda
from src.gestorAplicacion.sede import Sede
import random

class Pantalon(Prenda):
    serial_version_uid = 1

    def __init__(self, fecha, modista, descartada, terminada, sede, insumos):
        super().__init__(fecha, sede, "Pantalon", modista, descartada, terminada, insumos)

    def calcularGastoMensual(self):
        gasto = 0
        for index in range(len(self.insumo)):
            tipo = self.insumo[index]
            cantidad = self.cantidad_insumo[index]
            gasto += round(tipo.get_precio_individual() * cantidad)
        return gasto

    @staticmethod
    def PrecioVenta():
        total_precios = 0
        total_cantidades = 0
        for pantalon in Sede.get_prendas_inventadas_total():
            if isinstance(pantalon, Pantalon):
                total_precios += pantalon.calcular_precio()
                total_cantidades += 1
        precio_venta = round(total_precios / total_cantidades)
        # Se promedian todos los "precios por los que se deberían vender las prendas para que todas las camisas se vendan al mismo precio"
        return precio_venta

    # Usa el modista en el atributo de la clase Prenda
    def siguientePaso(self):
        retorno = []
        if self.paso_actual == 1:
            retorno.append("Maquina de Corte")
            retorno.append(5)
        elif self.paso_actual == 2:
            retorno.append("Maquina de Tijereado")
            retorno.append(2)
        elif self.paso_actual == 3:
            retorno.append("Maquina de Coser Industrial")
            retorno.append(10)
        else:
            retorno.append("LISTO")
            self.terminada = True
        self.ultimo_paso = retorno
        return retorno

    def realizarPaso(self, modista):
        self.modista = modista
        probabilidad_de_exito = modista.get_pericia()
        if self.paso_actual == 3:
            probabilidad_de_exito *= 0.9
        self.paso_actual += 1
        retorno = "CONTINUAR"
        if self.paso_actual > 3:
            retorno = "LISTO"
        if random.random() > probabilidad_de_exito:
            retorno = "DESCARTAR"
        return retorno

    cantidad_insumo = []
    tipo_insumo = []
    paso_actual = 1
    maquinaria_necesaria = ["Maquina de Corte", "Maquina de Coser Industrial", "Maquina de Tijereado"]

    @staticmethod
    def getTipoInsumo():
        return Pantalon.tipo_insumo
    @staticmethod
    def getCantidadInsumo():
        return Pantalon.cantidad_insumo
    @staticmethod
    def setTipoInsumo(tipos):
        Pantalon.tipo_insumo = tipos
    @staticmethod
    def setCantidadInsumo(cantidades):
        Pantalon.cantidad_insumo = cantidades
    @staticmethod
    def getMaquinariaNecesaria():
        return Pantalon.maquinaria_necesaria