from typing import List, Any
from src.gestorAplicacion.administracion.rol import Rol
from src.gestorAplicacion.membresia import Membresia
from src.gestorAplicacion.fecha import Fecha

class Persona:
    listaPersonas = []  # List of people

    def __init__(self, nombre: str, documento: int, rol: Rol, experiencia: int, trabaja: bool, membresia: Membresia):
        self.nombre = nombre
        self.documento = documento
        self.rol = rol
        self.experiencia = experiencia
        self.trabaja = trabaja
        self.membresia = membresia
        self.salario = self.calcularSalario()
        Persona.listaPersonas.append(self)

    def __str__(self) -> str:
        return f"Nombre: {self.nombre} - Documento: {self.documento} - Rol: {self.rol}"
    def getRol(self):
        return self.rol
    def getMembresia(self):
        return self.membresia
    def getDocumento(self):
        return self.documento
    def getNombre(self):
        return self.nombre
    def getExperiencia(self):
        return self.experiencia
    def isTrabaja(self):
        return self.trabaja
    @staticmethod
    def getListaPersonas():
        return Persona.listaPersonas
    @staticmethod
    def setListaPersonas(lista):
        Persona.listaPersonas = lista  # Used when deserializing

    # Interaction 3 of Human Management
    # Returns the list of suitable candidates, the list of roles, and how many of each role.
    @staticmethod
    def entrevistar(aReemplazar):
        rolesAReemplazar = []
        cantidad = []
        for empleado in aReemplazar:
            if empleado.getRol() not in rolesAReemplazar:
                rolesAReemplazar.append(empleado.getRol())
                cantidad.append(0)
            rolIdx = rolesAReemplazar.index(empleado.getRol())
            cantidad[rolIdx] += 1

        aptos = []

        for persona in Persona.listaPersonas:
            if not persona.trabaja and persona.getRol() in rolesAReemplazar:
                aptos.append(persona)

        return [aptos, rolesAReemplazar, cantidad]

    # Interaction 3 of Human Management
    @staticmethod
    def contratar(aContratar, aReemplazar, fecha: Fecha):
        from src.gestorAplicacion.bodega.maquinaria import Maquinaria
        from src.uiMain.main import Main
        from src.gestorAplicacion.administracion.empleado import Empleado
        for persona in aContratar:
            area = None
            sede = None
            for antiguo in aReemplazar:
                if antiguo.getRol() == persona.getRol():
                    area = antiguo.getAreaActual()
                    sede = antiguo.getSede()
                    aReemplazar.remove(antiguo)
                    break
            if area is not None and sede is not None:
                emp = Empleado(area, fecha, sede, persona)
                Maquinaria.asignarMaquinaria(emp)
                emp.setSalario(int(persona.getRol().getSalarioInicial() + persona.getRol().getSalarioInicial() * 0.5 * persona.getExperiencia()))
            else:
                Main.errorDeReemplazo(persona)

    def rolString(self) -> str:
        rolString = str(self.rol) if self.rol is not None else "Sin rol"
        trabajaString = "Trabaja" if self.trabaja else "No trabaja"
        membresiaString = str(self.membresia) if self.membresia is not None else "Sin membresía"

        return (f"Nombre: {self.nombre}, Documento: {self.documento}, Rol: {rolString}, "
                f"Experiencia: {self.experiencia}, Trabaja: {trabajaString}, "
                f"Membresía: {membresiaString}")

    def calcularSalario(self) -> int:
        return round((self.rol.getSalarioInicial() * 0.05) * self.experiencia) + self.rol.getSalarioInicial()

    @staticmethod
    def valorEsperadoSalario() -> int:
        valorEsperado = 0
        for persona in Persona.listaPersonas:
            from src.gestorAplicacion.administracion.empleado import Empleado
            if not isinstance(persona, Empleado):
                valorEsperado += persona.calcularSalario()
        return valorEsperado // len(Persona.listaPersonas) if Persona.listaPersonas else 0

    @staticmethod
    def diferenciaSalarios() -> int:
        from src.gestorAplicacion.administracion.empleado import Empleado
        return Persona.valorEsperadoSalario() - Empleado.valorEsperadoSalario()