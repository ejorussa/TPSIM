
class Empleado:
    def __init__(self, estado, cola):
        self.estado = estado
        self.cola_empleado = cola
        self.atendiendo_a = None
    
    def ocupar(self, cliente):
        self.estado = "Ocupado"
        self.atendiendo_a = cliente

    def desocupar(self):
        self.estado = "Libre"
        self.atendiendo_a = None

    def es_libre(self):
        return self.estado == "Libre"

    def es_ocupado(self):
        return self.estado == "Ocupado"

    def mostrar_info(self):
        return self.estado, len(self.cola_empleado)
