from Servidores.emplead import Empleado


class EmpleadoCobro(Empleado):

  def ocupar(self, cliente, reloj):
    super().ocupar(cliente, reloj)
    cliente.estado = "Siendo Cobrado"
    cliente.aparato_electrodomestico.estado = "Listo"

  def esperar(self, cliente):
    cliente.estado = "Esperando Cobro"
    cliente.aparato_electrodomestico.estado = "Listo"

