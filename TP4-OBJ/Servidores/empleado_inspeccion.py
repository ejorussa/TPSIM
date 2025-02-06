from Servidores.emplead import Empleado
import random
from distribuciones import poisson


class EmpleadoInspeccion(Empleado):
    def __init__(self, estado, cola, media):
        super().__init__(estado, cola, media)
        self.hay_fallos = False
        self.rnd_hay_fallos = ""

    def ocupar(self, cliente, reloj):
        super().ocupar(cliente, reloj)
        cliente.aparato_electrodomestico.estado ="Siendo Inspeccionado"

    def esperar(self, cliente):
        cliente.aparato_electrodomestico.estado = "Esperando Inspeccion"

    def revisar(self, empleado_siguiente, empleado_anterior, reloj):
        self.rnd_hay_fallos = random.random()
        self.hay_fallos = False
        if self.rnd_hay_fallos < 0.25:
            self.hay_fallos = True
            self.pasar_a(empleado_anterior, reloj)
            return 0, 0, 1, 0, 0
        else:
            n = self.mas_30(self.atendiendo_a.aparato_electrodomestico, reloj)
            if self.atendiendo_a.aparato_electrodomestico.esperando:
                self.pasar_a(empleado_siguiente, reloj)
                return 1, 0, 0, n, 0
            else:
                res = self.atendiendo_a.aparato_electrodomestico.tiempo_en_3_fases(reloj)
                self.pasar_a(empleado_siguiente, reloj)
                return 1, 1, 0, n, res

    def mas_30(self, obj,reloj):
        if (reloj-obj.inicio_atencion) >= 30:
            return 1
        else:
            return 0

    def calcular_fin(self, reloj):
        self.tiempo_demora, self.rnd = poisson(self.media)
        self.fin = self.tiempo_demora + reloj




