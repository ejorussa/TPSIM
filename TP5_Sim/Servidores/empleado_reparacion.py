from Servidores.emplead import Empleado


class EmpleadoReparacion(Empleado):
    def ayudar(self):
        self.estado = "Ayudando"

    def esta_ayudando(self):
        return self.estado == 'Ayudando'
