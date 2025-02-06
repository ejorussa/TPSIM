import distribuciones

class Empleado:
    def __init__(self, estado, cola, media):
        self.rnd = ""
        self.tiempo_demora = ""
        self.fin = ""
        self.estado = estado
        self.cola_empleado = cola
        self.atendiendo_a = None
        self.media = media

    
    def ocupar(self, cliente, reloj):
        self.estado = "Ocupado"
        self.atendiendo_a = cliente
        self.calcular_fin(reloj)
        # cliente.pasar a estado

    def desocupar(self):
        self.estado = "Libre"
        self.atendiendo_a = None
        self.rnd = ""
        self.tiempo_demora = ""
        self.fin = ""

    def es_libre(self):
        return self.estado == "Libre"

    def es_ocupado(self):
        return self.estado == "Ocupado"

    def mostrar_info(self):
        return self.estado, len(self.cola_empleado)

    def atender(self, cliente, reloj):
        if self.es_ocupado():      #  or len(self.cola_empleado) > 0
            # Mandar a cola
            self.cola_empleado.agregar(cliente)
            self.esperar(cliente)
        else:
            self.ocupar(cliente, reloj)

    def pasar_a(self, empleado_siguiente, reloj):
        empleado_siguiente.atender(self.atendiendo_a, reloj)
        #self.atender_siguiente(reloj) #ESTO HACIA QUE SALGAN DE A DOS EN LA COLA

    
    def atender_siguiente(self, reloj):
        if len(self.cola_empleado) > 0:
            self.calcular_fin(reloj)
            sig_cliente = self.cola_empleado.sacar()
            self.ocupar(sig_cliente, reloj)
        else:
            self.desocupar()

    def calcular_fin(self, reloj):
        self.tiempo_demora, self.rnd = distribuciones.numExponencial(self.media)
        self.fin = self.tiempo_demora + reloj

    def esperar(self, cliente):
        cliente.aparato_electrodomestico.paso_estado_esperando()
