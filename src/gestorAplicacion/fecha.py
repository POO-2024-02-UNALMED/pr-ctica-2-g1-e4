class Fecha:
    def __init__(self, dia=1, mes=1, ano=2000):
        self.dia = dia
        self.mes = mes
        self.ano = ano

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