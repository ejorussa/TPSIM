import random
import math


# realiza los cálculos necesarios para pasar un número a una distribución uniforme y las guarda en una tabla

# Generador de números con distribución exponencial
def numExponencial(media):
    rnd = random.random()
    exp = (-media * math.log(1 - rnd))
    return exp, rnd


# Realiza los cálculos necesarios para pasar un número a una distribución Poisson y los guarda en una tabla
# Usamos algoritmo dado por el profesor y lo utilizamos las veces deseadas
def poisson(lamd):
        p = 1
        x = -1
        a = math.exp(-lamd)
        while p >= a:
            rnd = random.random()
            p = p * rnd
            x = x + 1
        return x, rnd
