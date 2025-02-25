from abc import ABC, abstractmethod
from src.gestorAplicacion.administracion.empleado import Empleado
from src.gestorAplicacion.administracion.gastoMensual import GastoMensual
from src.gestorAplicacion.bodega.insumo import Insumo
from src.gestorAplicacion.bodega.maquinaria import Maquinaria
from src.gestorAplicacion.fecha import Fecha
from src.gestorAplicacion.sede import Sede
from src.gestorAplicacion.venta import Venta

class Prenda(GastoMensual):
    porcentajeGanancia = 0.40
    cantidadUltimaProduccion = 0
    cantidadTelaUltimaProduccion = 0
    prendasUltimaProduccion = []
    sobreCostoPorTrabajoExtra=0  #Es un metodo de clase pues aplica para TODA la tanda de producción, no solo para una prenda en específico.

    def __init__(self, fecha: Fecha, sede: Sede, nombre: str, modista:Empleado, descartada: bool, terminada: bool, insumos: Insumo):
        self.fechaFabricacion = fecha
        self.sede = sede
        sede.prendasInventadas.append(self)
        sede.getPrendasInventadasTotal().append(self)
        self.nombre = nombre
        self.modista = modista
        self.descartada = descartada
        self.terminada = terminada
        self.insumo = insumos
        self.costoInsumos = sum(insumo.precioXUnidad for insumo in insumos)
        self.costoProduccion = self.calcularCostoProduccion()
        self.precio = 0
        self.enStock = []
        self.ultimoPaso = []
        if descartada:
            modista.prendasDescartadas += 1
        elif terminada:
            modista.prendasProducidas += 1

    @staticmethod
    def producirPrendas(planProduccion, hoy):
        from src.uiMain.main import Main
        from src.uiMain.startFrame import StartFrame
        stf3 = StartFrame()
        Prenda.cantidadTelaUltimaProduccion = 0
        Prenda.cantidadUltimaProduccion = 0
        Prenda.prendasUltimaProduccion = []
        diaDeProduccion = hoy
        alcanzaInsumos = True
        for dia in planProduccion:
            for i, sede in enumerate(Sede.listaSedes):
                if not Prenda.producirListaPrendas(dia[i], sede, diaDeProduccion):
                    alcanzaInsumos = False
            diaDeProduccion = diaDeProduccion.diaSiguiente()
        stf3.recibeCreadasOrNo(alcanzaInsumos)
        Main.eventoTerminarProduccion.set()
        return
    
    tandasTotales=[] # Una lista de listas
    # Cada lista tiene indice 0 la lista de prendas. Indice 1 

    @classmethod
    def getInstanciasPrenda(cls,planProduccion,sede,fechaProduccion):
        from src.gestorAplicacion.bodega.camisa import Camisa
        from src.gestorAplicacion.bodega.pantalon import Pantalon
        from src.uiMain.main import Main
        cantidadPantalones = planProduccion[0]
        cantidadCamisas = planProduccion[1]
        prendas = []
        insumosPantalon = sede.insumosPorNombre(Pantalon.getTipoInsumo())# Es posible que no se encuentren insumos de tal nombre en la bodega de la sede.
        if not insumosPantalon:
            Main.avisarFaltaDeInsumos(sede, fechaProduccion, "Pantalon")
            return False
        for _ in range(cantidadPantalones):
            if sede.quitarInsumos(insumosPantalon, Pantalon.getCantidadInsumo()): 
                # Quitar los insumos al contar pantalones primero, indica que si no hay suficientes
                # Insumos ni siquiera para los pantalones, no se producirán camisas
                Prenda.cantidadTelaUltimaProduccion += Pantalon.getCantidadInsumo()[Pantalon.getTipoInsumo().index("Tela")]
                pantalon = Pantalon(fechaProduccion, None, False, False, sede, insumosPantalon)
                prendas.append(pantalon)
            else:
                alcanzaInsumos = False
                Main.avisarFaltaDeInsumos(sede, fechaProduccion, "Pantalon")
                break
        insumosCamisa = sede.insumosPorNombre(Camisa.getTipoInsumo()) # Es posible que no se encuentren insumos de tal nombre en la bodega de la sede.
        if not insumosCamisa:
            Main.avisarFaltaDeInsumos(sede, fechaProduccion, "Camisa")
            return False
        for _ in range(cantidadCamisas):
            if sede.quitarInsumos(insumosCamisa, Camisa.getCantidadInsumo()):
                Prenda.cantidadTelaUltimaProduccion += Camisa.getCantidadInsumo()[Camisa.getTipoInsumo().index("Tela")]
                camisa = Camisa(fechaProduccion, None, False, False, sede, insumosCamisa)
                prendas.append(camisa)
            else:
                alcanzaInsumos = False
                Main.avisarFaltaDeInsumos(sede, fechaProduccion, "Camisa")
                break
        idxTanda = 0
        return prendas

    @classmethod
    def producirListaPrendas(cls,planProduccion, sede, fechaProduccion):
        from src.gestorAplicacion.bodega.camisa import Camisa
        from src.gestorAplicacion.bodega.pantalon import Pantalon
        from src.uiMain.main import Main
        alcanzaInsumos = True
        cantidadPantalones = planProduccion[0]
        cantidadCamisas = planProduccion[1]
        prendas = cls.getInstanciasPrenda(planProduccion, sede, fechaProduccion)
        idxTanda = 0
        while prendas:
            tandasPorMaquina = [[] for _ in range(7)]
            for prenda in prendas:
                siguientePaso = prenda.siguientePaso()
                paso = siguientePaso[0].lower()
                if paso == "maquina de corte":
                    tandasPorMaquina[3].append(prenda)
                elif paso == "maquina de tijereado":
                    tandasPorMaquina[4].append(prenda)
                elif paso == "maquina de coser industrial":
                    tandasPorMaquina[5].append(prenda)
                elif paso == "maquina de bordadora":
                    tandasPorMaquina[1].append(prenda)
                elif paso == "maquina de termofijado":
                    tandasPorMaquina[0].append(prenda)
                elif paso == "plancha industrial":
                    tandasPorMaquina[2].append(prenda)
                elif paso == "bordadora industrial":
                    tandasPorMaquina[6].append(prenda)
            modista = Main.pedirModista(len(prendas), sede, idxTanda)
            for tanda in tandasPorMaquina:
                if not tanda:
                    continue
                maquina = Maquinaria.seleccionarDeTipo(sede, tanda[0].ultimoPaso[0])
                for prenda in tanda:
                    maquina.usar(prenda.ultimoPaso[1])
                    resultado = prenda.realizarPaso(modista)
                    if resultado == "DESCARTAR":
                        prenda.descartada = True
                        modista.prendasDescartadas += 1
                        prendas.remove(prenda)
                    elif resultado == "LISTO":
                        prenda.terminada = True
                        modista.prendasProducidas += 1
                        Prenda.prendasUltimaProduccion.append(prenda)
                        prendas.remove(prenda)
                        Prenda.cantidadUltimaProduccion += 1
            idxTanda += 1
        return alcanzaInsumos

    @abstractmethod
    def siguientePaso(self):
        pass
    @abstractmethod
    def realizarPaso(self, modista):
        pass

    @staticmethod
    def gastoMensualClase(fecha):
        gastoPrenda = 0
        gastoActual = 0
        gastoPasado = 0
        for prenda in Sede.prendasInventadasTotal:
            lista = prenda.gastoMensualTipo(fecha, prenda.fechaFabricacion)
            gastoActual += lista[0]
            gastoPasado += lista[1]
        gastoPrenda = gastoActual if gastoActual != 0 else gastoPasado
        return gastoPrenda

    @staticmethod
    def prevenciones(descuento, nuevoDescuento, fecha):
        for sede in Sede.listaSedes:
            for prenda in sede.prendasInventadas:
                if descuento > 0.0 or nuevoDescuento > 0.0:
                    if nuevoDescuento > 0.0:
                        Prenda.porcentajeGanancia -= Prenda.porcentajeGanancia * (1 - nuevoDescuento)
                    Venta.pesimismo -= 0.05
                else:
                    Venta.pesimismo += 0.1
        return Venta.pesimismo

    def calcularCostoInsumos(self):
        self.costoInsumos = sum(Insumo.getPrecioIndividual(insumo) * cantidad for insumo, cantidad in zip(self.insumo, self.getCantidadInsumo()))
        return self.costoInsumos

    def calcularCostoProduccion(self):
        from src.gestorAplicacion.administracion.rol import Rol
        sumSalarios = sum(empleado.rol.getSalarioInicial() for empleado in self.sede.getListaEmpleados() if empleado.rol == Rol.MODISTA)
        self.costoProduccion = round(sumSalarios * 0.01)+ Prenda.sobreCostoPorTrabajoExtra # sobreCostoPorTrabajoExtra aplica para todas las prendas por igual, pues es una concecuencia de como el usuario corra TODA la tanda de producción.
        return self.costoProduccion

    def calcularPrecio(self):
        costoTotal = self.costoInsumos + self.costoProduccion
        gananciaDeseada = costoTotal + (costoTotal * Prenda.porcentajeGanancia)
        self.precio = round(gananciaDeseada)
        return self.precio

    def __str__(self):
        return f"La prenda de tipo {self.nombre}"
    def getPrendasDescartadas(self):
        return self.descartada
    def getNombre(self):
        return self.nombre
    def getInsumo(self):
        return self.insumo
    def getSede(self):
        return self.sede
    @classmethod
    def getCantidadInsumo(cls):
        return cls.cantidadInsumo
    def getCostoInsumos(self):
        return self.costoInsumos
    def getPrecio(self):
        return self.precio
    def getFecha(self):
        return self.fechaFabricacion
    @classmethod
    def getCantidadUltimaProduccion(cls):
        return cls.cantidadUltimaProduccion
    @classmethod
    def getCantidadTelaUltimaProduccion(cls):
        return cls.cantidadTelaUltimaProduccion
    @classmethod
    def setSobreCosto(cls, sobreCosto):
        Prenda.sobreCostoPorTrabajoExtra = sobreCosto
