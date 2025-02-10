#* Equipo 4 grupo 1
# * Clase Banco
# * Representa un banco con una cuenta y un ahorro, posiblemente deudas.

from typing import List

class Banco:
    listaBancos = []
    cuentaPrincipal = None

    def __init__(self, cuenta, nombre, ahorro, interes):
        self.nombreEntidad = nombre
        self.nombreCuenta = cuenta
        self.deuda=[]
        self.ahorroBanco = ahorro
        self.interes = interes
        Banco.listaBancos.append(self)

    def actualizarDeuda(self, ndeuda):
        self.deuda.append(ndeuda)

    def transaccion(self, monto: int):
        self.ahorroBanco += monto

    def __str__(self):
        return f"La Cuenta: {self.nombreCuenta} en: {self.nombreEntidad} tiene un Ahorro de: {self.ahorroBanco:,} y para pedir un préstamo el Banco tiene un interés de: {self.interes * 100}%"

    @classmethod
    def totalAhorros(cls):
        total = sum(b.getAhorroBanco() for b in cls.listaBancos)
        return total

    # ------------------- Getters y Setters -------------------
    def getNombreEntidad(self) -> str:
        return self.nombreEntidad

    def getNombreCuenta(self) -> str:
        return self.nombreCuenta

    def getDeuda(self) -> List:
        return self.deuda

    def getAhorroBanco(self) -> int:
        return self.ahorroBanco

    def getInteres(self) -> float:
        return self.interes

    @staticmethod
    def getListaBancos() -> List['Banco']:
        return Banco.listaBancos

    def setNombreEntidad(self, nombre_banco: str):
        self.nombreEntidad = nombre_banco

    def setNombreCuenta(self, nombreCuenta: str):
        self.nombreCuenta = nombreCuenta

    def setAhorroBanco(self, ahorroBanco: int):
        self.ahorroBanco = ahorroBanco

    def setInteres(self, interes: float):
        self.interes = interes

    @staticmethod
    def setListaBancos(listaBancos: List['Banco']):
        if listaBancos is None:
            raise ValueError("La lista no puede ser nula")
        Banco.listaBancos = listaBancos

    @staticmethod
    def getCuentaPrincipal():
        return Banco.cuentaPrincipal

    @staticmethod
    def setCuentaPrincipal(cuentaPrincipal: 'Banco'):
        Banco.cuentaPrincipal = cuentaPrincipal
