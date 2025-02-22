from src.gestorAplicacion.administracion.empleado import Empleado
from src.gestorAplicacion.fecha import Fecha
from src.gestorAplicacion.sede import Sede
from typing import List, Optional
import random
from src.gestorAplicacion.bodega.prenda import Prenda
from src.gestorAplicacion.bodega.insumo import Insumo

class Camisa(Prenda):
    serialVersionUid = 1
    cantidadInsumo = []; tipoInsumo = []
    pasoActual = 1

    maquinariaNecesaria = ["Maquina de Corte", "Bordadora Industrial", "Maquina de Coser Industrial", "Maquina de Termofijado", "Plancha Industrial"]

    def __init__(self, fecha: Fecha, modista: Empleado, descartada: bool, terminada: bool, sede: Sede, insumos: List[Insumo]):
        super().__init__(fecha, sede, "Camisa", modista, descartada, terminada, insumos)

    def calcularGastoMensual(self) -> int:
        gasto = 0
        for i in range(len(self.insumo)):
            tipo = self.insumo[i]
            cantidad = self.cantidadInsumo[i]
            gasto += round(tipo.getPrecioIndividual() * cantidad)
        return gasto

    @staticmethod
    def precioVenta() -> int:
        precios = 0
        cantidades = 0
        precioVenta = 0
        for camisa in Sede.getPrendasInventadasTotal():
            if isinstance(camisa, Camisa):
                precios += camisa.calcularPrecio()
                cantidades += 1
        if cantidades > 0:
            precioVenta = round(precios / cantidades) # Se promedian todos los "precios por los que se deberían vender las prendas para que todas las camisas se vendan al mismo"
        return precioVenta # El sobrecosto de producción hace parte de el costo de producción, por ende no se añade aquí y hace parte de calcularPrecio()

    def siguientePaso(self) -> List[Optional[int]]:
        retorno = []
        if self.pasoActual == 1:
            retorno.extend(["Maquina de Corte", 5])
        elif self.pasoActual == 2:
            retorno.extend(["Maquina de Coser Industrial", 10])
        elif self.pasoActual == 3:
            retorno.extend(["Plancha Industrial", 5])
        elif self.pasoActual == 4:
            retorno.extend(["Bordadora Industrial", 5])
        elif self.pasoActual == 5:
            retorno.extend(["Maquina de Termofijado", 10])
        else:
            retorno.append("LISTO")
        self.ultimoPaso = retorno
        return retorno

    def realizarPaso(self, modista: Empleado) -> str:
        self.modista = modista
        probabilidadDeExito = modista.getPericia()
        if self.pasoActual == 2:
            probabilidadDeExito *= 0.9
        elif self.pasoActual == 3:
            probabilidadDeExito *= 0.8
        elif self.pasoActual == 5:
            probabilidadDeExito *= 0.9
        retorno = "CONTINUAR"
        self.pasoActual += 1
        suerte = random.random()
        if self.pasoActual > 4:
            return "LISTO"
        if suerte > probabilidadDeExito:
            retorno = "DESCARTAR"
            self.descartada = True
        return retorno

    @staticmethod
    def getTipoInsumo():
        return Camisa.tipoInsumo
    @staticmethod
    def getCantidadInsumo():
        return Camisa.cantidadInsumo
    @staticmethod
    def setTipoInsumo(tipos):
        Camisa.tipoInsumo = tipos
    @staticmethod
    def setCantidadInsumo(cantidades):
        Camisa.cantidadInsumo = cantidades
    @staticmethod
    def getMaquinariaNecesaria():
        return Camisa.maquinariaNecesaria