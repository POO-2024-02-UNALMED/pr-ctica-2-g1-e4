class Fecha:
    def __init__(self, dia=1, mes=1, ano=2000):
        self.dia = dia
        self.mes = mes
        self.ano = ano
        self.anio = ano % 100
    def getDia(self):
        return self.dia
    def setDia(self, dia):
        self.dia = dia
    def getMes(self):
        return self.mes
    def setMes(self, mes):
        self.mes = mes
    def getAno(self):
        return self.ano
    def setAno(self, ano):
        self.ano = ano
    def restarMeses(self, meses):
        mes = self.mes - meses
        ano = self.ano
        if mes <= 0:
            mes += 12
            ano -= 1
        return Fecha(self.dia, mes, ano)
    def compararAno(año1, año2):
        if (año1==año2):
            return True
        return False
    def compararMes(mes1, mes2):
        if (mes1==mes2):
            return True
        return False
    def compararDia(dia1, dia2):
        if (dia1==dia2):
            return True
        return False
    @staticmethod
    def compararFecha(fecha1, fecha2):
        return (Fecha.compararAno(fecha1.ano, fecha2.ano) and
                Fecha.compararMes(fecha1.mes, fecha2.mes) and
                Fecha.compararDia(fecha1.dia, fecha2.dia))
    def diasHasta(self, hasta):
        dias = (hasta.ano - self.ano) * 365
        dias += (hasta.mes - self.mes) * 30
        dias += hasta.dia - self.dia
        return dias
    def diaSiguiente(self):
        nuevaFecha = Fecha(self.dia, self.mes, self.ano)
        nuevaFecha.dia += 1
        if nuevaFecha.dia > 31:
            nuevaFecha.dia = 1
            nuevaFecha.mes += 1
            if nuevaFecha.mes > 12:
                nuevaFecha.mes = 1
                nuevaFecha.ano += 1
        return nuevaFecha
    def __str__(self):
        return f"Día: {self.dia} Mes: {self.mes} Año: {self.ano}"
    def strCorto(self):
        return f"{self.dia}/{self.mes}/{self.ano}"
    
    def esBisiesto(self):
        """Determina si el año (solo con dos cifras) es bisiesto."""
        return (self.anio % 4 == 0 and self.anio % 100 != 0) or (self.anio % 400 == 0)

    def diasEnMes(self):
        """Retorna la cantidad de días que tiene el mes actual."""
        if self.mes in [4, 6, 9, 11]:  # Abril, Junio, Septiembre, Noviembre
            return 30
        elif self.mes == 2:  # Febrero
            return 29 if self.esBisiesto() else 28
        else:  # Meses con 31 días
            return 31

    def aDiasTotales(self):
        """Convierte la fecha a un número total de días desde el año 00."""
        totalDias = self.dia
        
        # Sumar días de los años anteriores (solo tomando en cuenta los últimos dos dígitos del año)
        for year in range(0, self.anio):
            totalDias += 366 if Fecha(1, 1, year).esBisiesto() else 365

        # Sumar días de los meses anteriores en el mismo año
        for mes in range(1, self.mes):
            totalDias += Fecha(1, mes, self.anio).diasEnMes()

        return totalDias