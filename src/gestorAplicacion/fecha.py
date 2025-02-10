class Fecha:
    def __init__(self, dia=1, mes=1, año=2000):
        self.dia = dia
        self.mes = mes
        self.año = año

    def getDia(self):
        return self.dia

    def setDia(self, dia):
        self.dia = dia

    def getMes(self):
        return self.mes

    def setMes(self, mes):
        self.mes = mes

    def getAño(self):
        return self.año

    def setAño(self, año):
        self.año = año


    def restarMeses(self, meses):
        mes = self.mes - meses
        año = self.año
        if mes <= 0:
            mes += 12
            año -= 1
        return Fecha(self.dia, mes, año)

    @staticmethod
    def compararFecha(fecha1, fecha2):
        return (Fecha.comparar_año(fecha1.año, fecha2.año) and
                Fecha.comparar_mes(fecha1.mes, fecha2.mes) and
                Fecha.comparar_dia(fecha1.dia, fecha2.dia))

    def diasHasta(self, hasta):
        dias = (hasta.año - self.año) * 365
        dias += (hasta.mes - self.mes) * 30
        dias += hasta.dia - self.dia
        return dias

    def diaSiguiente(self):
        nueva_fecha = Fecha(self.dia, self.mes, self.año)
        nueva_fecha.dia += 1
        if nueva_fecha.dia > 31:
            nueva_fecha.dia = 1
            nueva_fecha.mes += 1
            if nueva_fecha.mes > 12:
                nueva_fecha.mes = 1
                nueva_fecha.año += 1
        return nueva_fecha

    def __str__(self):
        return f"Día: {self.dia} Mes: {self.mes} Año: {self.año}"