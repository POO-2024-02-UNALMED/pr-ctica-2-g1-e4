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

    prendasTandaActual=[] # Lista de prendas separadas por maquina
    planesDeProduccion = [] # Contiene una lista con los numeros por prenda, la fecha y la sede.
    tandasPorMaquina=[] # Preparado por getSiguienteTanda y seprarPrendasPorMaquina
    idxPlanProduccion = 0
    idxTanda = 0
    faltaInsumos = False

    @classmethod
    def prepararElaboracion(cls,planProduccion):
        from src.uiMain.main import Main
        cls.prendasTandaActual=[] # Lista de prendas separadas por maquina
        cls.idxDiaProduccion = 0
        cls.idxTanda = 0
        cls.faltaInsumos = False

        cls.cantidadTelaUltimaProduccion = 0
        cls.cantidadUltimaProduccion = 0
        cls.prendasUltimaProduccion = []

        diaDeProduccion = Main.fecha
        for dia in planProduccion:
            for i, sede in enumerate(Sede.listaSedes):
                cls.planesDeProduccion.append([dia[i],diaDeProduccion,sede])
        
        cls.prendasTandaActual=cls.getInstanciasPrenda(cls.planesDeProduccion[0][0],cls.planesDeProduccion[0][2],cls.planesDeProduccion[0][1])
        cls.separarPrendasPorMaquina(cls.prendasTandaActual)
    
    @classmethod
    def getSedeTandaActual(cls):
        return cls.planesDeProduccion[cls.idxPlanProduccion][2]
    
    @classmethod
    def getFechaTandaActual(cls):
        return cls.planesDeProduccion[cls.idxPlanProduccion][1]

    @classmethod
    def cantidadPrendasTanda(cls):
        return len(cls.prendasTandaActual)

        
    @classmethod
    def getSiguienteTanda(cls,modista)->bool: # Retorna si terminamos la producción
        terminamosPrendas=cls.producirListaPrendas(cls.planesDeProduccion[cls.idxPlanProduccion][2],modista)
        cls.separarPrendasPorMaquina(cls.prendasTandaActual)
        if terminamosPrendas:
            cls.idxPlanProduccion+=1
            if cls.idxPlanProduccion>=len(cls.planesDeProduccion):
                return True
            nuevaSede=cls.planesDeProduccion[cls.idxPlanProduccion][2]
            cls.prendasTandaActual=cls.getInstanciasPrenda(cls.planesDeProduccion[cls.idxPlanProduccion][0],nuevaSede,cls.planesDeProduccion[cls.idxPlanProduccion][1])
            cls.separarPrendasPorMaquina(cls.prendasTandaActual)
        return False

    @classmethod
    def avisarFaltaDeInsumos(cls):
        cls.faltaInsumos=True

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
                cls.avisarFaltaDeInsumos()
                break
        insumosCamisa = sede.insumosPorNombre(Camisa.getTipoInsumo()) # Es posible que no se encuentren insumos de tal nombre en la bodega de la sede.
        if not insumosCamisa:
            cls.avisarFaltaDeInsumos()
            return False
        for _ in range(cantidadCamisas):
            if sede.quitarInsumos(insumosCamisa, Camisa.getCantidadInsumo()):
                Prenda.cantidadTelaUltimaProduccion += Camisa.getCantidadInsumo()[Camisa.getTipoInsumo().index("Tela")]
                camisa = Camisa(fechaProduccion, None, False, False, sede, insumosCamisa)
                prendas.append(camisa)
            else:
                cls.avisarFaltaDeInsumos()
                break
        return prendas

    @classmethod
    def separarPrendasPorMaquina(cls,prendas):
        cls.tandasPorMaquina = [[] for _ in range(7)]
        for prenda in prendas:
            siguientePaso = prenda.siguientePaso()
            paso = siguientePaso[0].lower()
            if paso == "maquina de corte":
                cls.tandasPorMaquina[3].append(prenda)
            elif paso == "maquina de tijereado":
                cls.tandasPorMaquina[4].append(prenda)
            elif paso == "maquina de coser industrial":
                cls.tandasPorMaquina[5].append(prenda)
            elif paso == "maquina de bordadora":
                cls.tandasPorMaquina[1].append(prenda)
            elif paso == "maquina de termofijado":
                cls.tandasPorMaquina[0].append(prenda)
            elif paso == "plancha industrial":
                cls.tandasPorMaquina[2].append(prenda)
            elif paso == "bordadora industrial":
                cls.tandasPorMaquina[6].append(prenda)
        

    @classmethod
    def producirListaPrendas(cls,sede,modista)->bool: # Retorna True si se acabaron las prendas a producir
        from src.gestorAplicacion.bodega.camisa import Camisa
        from src.gestorAplicacion.bodega.pantalon import Pantalon
        from src.uiMain.main import Main
        idxTanda = 0
        for tanda in cls.tandasPorMaquina:
            if not tanda:
                continue
            maquina = Maquinaria.seleccionarDeTipo(sede, tanda[0].ultimoPaso[0])
            for prenda in tanda:
                maquina.usar(prenda.ultimoPaso[1])
                resultado = prenda.realizarPaso(modista)
                if resultado == "DESCARTAR":
                    prenda.descartada = True
                    modista.prendasDescartadas += 1
                    cls.prendasTandaActual.remove(prenda)
                elif resultado == "LISTO":
                    prenda.terminada = True
                    modista.prendasProducidas += 1
                    Prenda.prendasUltimaProduccion.append(prenda)
                    cls.prendasTandaActual.remove(prenda)
                    Prenda.cantidadUltimaProduccion += 1
        idxTanda += 1
        return len(cls.prendasTandaActual) == 0

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
