
class Cola:
    def __init__(self):
        self.cola = []

    def __len__(self):
        return len(self.cola)

    def sacar(self):
        return self.cola.pop()

    def agregar(self, elemento):
        self.cola = [elemento] + self.cola
