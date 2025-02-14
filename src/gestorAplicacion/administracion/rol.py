from enum import Enum

class Rol(Enum):
    PRESIDENTE = 3000000
    EJECUTIVO = 2000000
    ASISTENTE = 1000000
    DISEÑADOR = 2000000
    MODISTA = 1000000
    SECRETARIA = 1000000
    PLANTA = 1500000
    VENDEDOR = 1000000

    def __init__(self, initialSalary):
        self.initialSalary = initialSalary

    def getSalarioInicial(self):
        return self.initialSalary