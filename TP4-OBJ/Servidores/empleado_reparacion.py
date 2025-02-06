from Servidores.emplead import Empleado
from distribuciones import numExponencial


class EmpleadoReparacion(Empleado):
    def __init__(self, estado, cola, media):
        super().__init__(estado, cola, media)
        self.compañero = None

    def ayudar(self):
        self.estado = "Ayudando"

    def esta_ayudando(self):
        return self.estado == 'Ayudando'

    def ocupar(self, cliente, reloj):
        super().ocupar(cliente, reloj)
        cliente.estado = "Esperando Aparato"
        cliente.aparato_electrodomestico.estado = "Siendo Reparado"
        cliente.aparato_electrodomestico.inicio_reparacion = reloj

    def esperar(self, cliente):
        cliente.estado = "Esperando Aparato"
        cliente.aparato_electrodomestico.estado = "Esperando Reparacion"

    def atender(self, cliente, reloj):
        self.tiempo_demora, self.rnd = numExponencial(self.media)
        if self.es_libre() and self.compañero.es_libre():
            self.tiempo_demora *= 0.5
            self.fin = self.tiempo_demora + reloj
            self.ocupar(cliente, reloj)
            self.compañero.ayudar()
            self.atendiendo_a.aparato_electrodomestico.iniciar_reparacion(reloj)
        elif self.esta_ayudando():
            self.compañero.fin = (self.compañero.fin - reloj) / 0.5 + reloj
            self.fin = self.tiempo_demora + reloj
            self.ocupar(cliente, reloj)
            self.atendiendo_a.aparato_electrodomestico.iniciar_reparacion(reloj)
        elif self.compañero.esta_ayudando():
            self.fin = (self.fin - reloj) / 0.5 + reloj
            self.compañero.fin = self.tiempo_demora + reloj
            self.compañero.ocupar(cliente, reloj)
            self.compañero.atendiendo_a.aparato_electrodomestico.iniciar_reparacion(reloj)
        # elif self.es_libre(): Atiendo yo solo
        else:
            self.cola_empleado.agregar(cliente)
            self.esperar(cliente)

    def atender_siguiente(self, reloj):
        if self.compañero.esta_ayudando():
            self.compañero.desocupar()
        self.desocupar()
        # if len(cola) // elif mi_compa.esta_ayudando()
        if self.compañero.es_ocupado():
            self.ayudar()
            self.compañero.fin = (self.compañero.fin - reloj) * 0.5 + reloj
        if len(self.cola_empleado) > 0:
            sig_cliente = self.cola_empleado.sacar()
            self.atender(sig_cliente, reloj)

    def pasar_a(self, empleado_siguiente, reloj):
        tiempo_reparacion = self.atendiendo_a.aparato_electrodomestico.calcular_reparacion(reloj)
        super().pasar_a(empleado_siguiente, reloj)
        return tiempo_reparacion


