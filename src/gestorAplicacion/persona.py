from typing import List, Any
from src.gestorAplicacion.administracion.rol import Rol
from src.gestorAplicacion.membresia import Membresia
from src.gestorAplicacion.fecha import Fecha

class Persona:
    lista_personas = []  # List of people

    def __init__(self, nombre: str, documento: int, rol: Rol, experiencia: int, trabaja: bool, membresia: Membresia):
        self.nombre = nombre
        self.documento = documento
        self.rol = rol
        self.experiencia = experiencia
        self.trabaja = trabaja
        self.membresia = membresia
        self.salario=self.calcularSalario()
        Persona.lista_personas.append(self)

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
        return Persona.lista_personas
    @staticmethod
    def setListaPersonas(lista):
        Persona.lista_personas = lista  # Used when deserializing

    # Interaction 3 of Human Management
    # Returns the list of suitable candidates, the list of roles, and how many of each role.
    @staticmethod
    def entrevistar(a_reemplazar):
        roles_a_reemplazar = []
        cantidad = []
        for empleado in a_reemplazar:
            if empleado.get_rol() not in roles_a_reemplazar:
                roles_a_reemplazar.append(empleado.get_rol())
                cantidad.append(0)
            rol_idx = roles_a_reemplazar.index(empleado.get_rol())
            cantidad[rol_idx] += 1

        aptos = []

        for persona in Persona.lista_personas:
            if not persona.trabaja and persona.get_rol() in roles_a_reemplazar:
                aptos.append(persona)

        return [aptos, roles_a_reemplazar, cantidad]

    # Interaction 3 of Human Management
    @staticmethod
    def contratar(a_contratar, a_reemplazar, fecha: Fecha):
        from src.gestorAplicacion.bodega.maquinaria import Maquinaria
        from src.uiMain.main import Main
        from src.gestorAplicacion.administracion.empleado import Empleado
        for persona in a_contratar:
            area = None
            sede = None
            for antiguo in a_reemplazar:
                if antiguo.get_rol() == persona.get_rol():
                    area = antiguo.get_area_actual()
                    sede = antiguo.get_sede()
                    a_reemplazar.remove(antiguo)
                    break
            if area is not None and sede is not None:
                emp = Empleado(area, fecha, sede, persona)
                Maquinaria.asignarMaquinaria(emp)
                emp.setSalario(int(persona.get_rol().getSalarioInicial() + persona.get_rol().getSalarioInicial() * 0.5 * persona.get_experiencia()))
            else:
                Main.error_de_reemplazo(persona)

    def rolString(self) -> str:
        rol_string = str(self.rol) if self.rol is not None else "Sin rol"
        trabaja_string = "Trabaja" if self.trabaja else "No trabaja"
        membresia_string = str(self.membresia) if self.membresia is not None else "Sin membresía"

        return (f"Nombre: {self.nombre}, Documento: {self.documento}, Rol: {rol_string}, "
                f"Experiencia: {self.experiencia}, Trabaja: {trabaja_string}, "
                f"Membresía: {membresia_string}")

    def calcularSalario(self) -> int:
        return round((self.rol.getSalarioInicial() * 0.05) * self.experiencia) + self.rol.getSalarioInicial()

    @staticmethod
    def valorEsperadoSalario() -> int:
        valor_esperado = 0
        for persona in Persona.lista_personas:
            from src.gestorAplicacion.administracion.empleado import Empleado
            if not isinstance(persona, Empleado):
                valor_esperado += persona.calcular_salario()
        return valor_esperado // len(Persona.lista_personas) if Persona.lista_personas else 0

    @staticmethod
    def diferenciaSalarios() -> int:
        from src.gestorAplicacion.administracion.empleado import Empleado
        return Persona.valorEsperadoSalario() - Empleado.valorEsperadoSalario()