from enum import Enum

class Rol(Enum):
    PRESIDENTE = 3000000; 
    EJECUTIVO = 2000000; 
    ASISTENTE = 1200000; 
    DISEÑADOR = 2000000; 
    MODISTA = 1300000; 
    SECRETARIA = 1400000; 
    PLANTA = 1500000; 
    VENDEDOR = 1000000
    def __init__(self, initialSalary):
        self.initialSalary = initialSalary
    def getSalarioInicial(self):
        return self.initialSalary
    
    # He cambiado los salarios porque para python, si 2 miembros de un enum son iguales, son el mismo.
    # ver https://stackoverflow.com/questions/31537316/python-enums-with-duplicate-values