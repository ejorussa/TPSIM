from Servidores.emplead import Empleado


class EmpleadoRecepcion(Empleado):

    def ocupar(self, cliente, reloj):
        super().ocupar(cliente, reloj)
        cliente.estado = "Siendo Atendido"
        cliente.aparato_electrodomestico.estado = "Esperando"

    def esperar(self, cliente):
        cliente.estado = "Esperando Recepcion"
        cliente.aparato_electrodomestico.estado = "Esperando"
