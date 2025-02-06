class Aparato:
    def __init__(self, estado, inicio_atencion, inicio_reparacion, esperando_flag):
        self.estado = estado
        self.inicio_atencion = inicio_atencion
        self.inicio_reparacion = inicio_reparacion
        self.esperando = esperando_flag

    def iniciar_reparacion(self, reloj):
        self.inicio_reparacion = reloj
        self.estado = "Siendo Reparado"

    def paso_estado_esperando(self):
        self.esperando = True