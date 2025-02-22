from src.gestorAplicacion.administracion.empleado import Empleado
from src.gestorAplicacion.bodega.prenda import Prenda
from src.gestorAplicacion.sede import Sede
import random

class Pantalon(Prenda):
    serialVersionUid = 1

    def __init__(self, fecha, modista, descartada, terminada, sede, insumos):
        super().__init__(fecha, sede, "Pantalon", modista, descartada, terminada, insumos)

    def calcularGastoMensual(self):
        gasto = 0
        for index in range(len(self.insumo)):
            tipo = self.insumo[index]
            cantidad = self.cantidadInsumo[index]
            gasto += round(tipo.getPrecioIndividual() * cantidad)
        return gasto

    @staticmethod
    def precioVenta():
        totalPrecios = 0
        totalCantidades = 0
        for pantalon in Sede.getPrendasInventadasTotal():
            if isinstance(pantalon, Pantalon):
                totalPrecios += pantalon.calcularPrecio()
                totalCantidades += 1
        precioVenta = round(totalPrecios / totalCantidades)
        # Se promedian todos los "precios por los que se deberían vender las prendas para que todas las camisas se vendan al mismo precio"
        return precioVenta 
    
    # Usa el modista en el atributo de la clase Prenda
    def siguientePaso(self):
        retorno = []
        if self.pasoActual == 1:
            retorno.append("Maquina de Corte")
            retorno.append(5)
        elif self.pasoActual == 2:
            retorno.append("Maquina de Tijereado")
            retorno.append(2)
        elif self.pasoActual == 3:
            retorno.append("Maquina de Coser Industrial")
            retorno.append(10)
        else:
            retorno.append("LISTO")
            self.terminada = True
        self.ultimoPaso = retorno
        return retorno

    def realizarPaso(self, modista):
        self.modista = modista
        probabilidadDeExito = modista.getPericia()
        if self.pasoActual == 3:
            probabilidadDeExito *= 0.9
        self.pasoActual += 1
        retorno = "CONTINUAR"
        if self.pasoActual > 3:
            retorno = "LISTO"
        if random.random() > probabilidadDeExito:
            retorno = "DESCARTAR"
        return retorno

    cantidadInsumo = [200,1,1,300]
    tipoInsumo = ["Tela","Boton","Cremallera","Hilo"]
    pasoActual = 1
    maquinariaNecesaria = ["Maquina de Corte", "Maquina de Coser Industrial", "Maquina de Tijereado"]

    @staticmethod
    def getTipoInsumo():
        return Pantalon.tipoInsumo
    @staticmethod
    def getCantidadInsumo():
        return Pantalon.cantidadInsumo
    @classmethod
    def setTipoInsumo(cls,tipos):
        cls.tipoInsumo = tipos
    @classmethod
    def setCantidadInsumo(cls,cantidades):
        cls.cantidadInsumo = cantidades
    @staticmethod
    def getMaquinariaNecesaria():
        return Pantalon.maquinariaNecesaria