
class Cliente:
    def __init__(self, aparato, estadoa):
        self.aparato_electrodomestico = aparato
        self.estado = estadoa

    def finalizar(self):
        self.estado = "Cobrado"

    



