import math
import random

# Función encargada de generar los números aleatorios con una distribución NORMAL
def normal(media, de):
    rnd1 = random.random()
    rnd2 = random.random()
    n1 = (pow(-2 * math.log(rnd1), 1 / 2) * math.cos(2 * math.pi * rnd2)) * de + media
    n2 = (pow(-2 * math.log(rnd1), 1 / 2) * math.sin(2 * math.pi * rnd2)) * de + media
    return n1, n2

# Función encargada de generar los números aleatorios con una distribución POISSON
def poisson(media):
    p = 1
    x = -1
    a = math.exp(-media)
    while p >= a:
        u = random.random()
        p = p * u
        x = x + 1
    return x
