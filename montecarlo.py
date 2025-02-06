import math
import normal
import random
import time

# Clase de ACUMULADORES y CONTADORES
class Registro:
    def __init__(self):
        self.hombres_c = 0
        self.hombres_gastos = 0
        self.mujeres_c = 0
        self.mujeres_gastos = 0
        self.ventas_c = 0
        self.atendidos_c = 0
        self.ingreso_total = 0
        self.nro_llamada = 0


# Método que da inicio a la SIMULACIÓN, generando de números para saber la cantidad de llamadas por hora
# Posteriormente realiza el llamado al método "Montacarlo" para el cálculo de la fila
def inicio(media, de, horas, desde, tablaintervalo, tablafinal):
    # Elimina los datos anteriores de las tablas en caso de tener datos anteriores
    tablaintervalo.delete(*tablaintervalo.get_children())
    tablafinal.delete(*tablafinal.get_children())

    # Si el usuario elige utilizar la distribución NORMAL para la generación de números
    if de != '':
        de = float(de)
        start_time = time.time()  # Registra el tiempo de inicio
        llamada_actual = []
        con_acu = Registro()
        hasta = desde + 500

        # Recorre hora por hora
        for i in range(horas):

            # Verifica si el número de hora es par o impar (necesario para la generación de números con Box Müller)
            if i % 2 == 0:
                # Llamada al método "normal" para generar los 2 normales para la cantidad de llamadas
                # Si el número de llamada es par genera los 2 normales y luego utiliza solamente n1, guardando n2 para la siguiente corrida
                n1, n2 = normal.normal(media, de)

                # Recorre llamada por llamada
                for j in range(int(n1)):
                    # Contador de número de llamada
                    con_acu.nro_llamada += 1
                    # Realiza una corrida del Montecarlo
                    res = montecarlo(con_acu)
                    # Guarda los valores generados en un vector
                    llamada_actual = [str(i+1), con_acu.nro_llamada, res[0], res[1], res[2], res[3], res[4], res[5], res[6], res[7]
                                      , con_acu.atendidos_c, con_acu.ventas_c, con_acu.hombres_c, con_acu.hombres_gastos,
                                      con_acu.mujeres_c, con_acu.mujeres_gastos, con_acu.ingreso_total]

                    # Comprueba si el número de llamada fue solicitado para mostrar por el usuario, y si es así, agrega la fila en la tabla
                    if desde <= con_acu.nro_llamada <= hasta:
                        tablaintervalo.insert(parent='', index='end', values=llamada_actual)

            # El número de llamada es impar
            else:
                # Si es impar el número de llamada utiliza el n2 guardado
                # Recorre llamada por llamada
                for j in range(int(n2)):
                    # Contador de número de llamada
                    con_acu.nro_llamada += 1
                    # Realiza una corrida del Montecarlo
                    res = montecarlo(con_acu)
                    # Guarda los valores generados en un vector
                    llamada_actual = [str(i+1), con_acu.nro_llamada, res[0], res[1], res[2], res[3], res[4], res[5], res[6], res[7]
                                      , con_acu.atendidos_c, con_acu.ventas_c, con_acu.hombres_c, con_acu.hombres_gastos,
                                      con_acu.mujeres_c, con_acu.mujeres_gastos, con_acu.ingreso_total]

                    # Comprueba si el número de llamada fue solicitado para mostrar por el usuario, y si es así, agrega la fila en la tabla
                    if desde <= con_acu.nro_llamada <= hasta:
                        tablaintervalo.insert(parent='', index='end', values=llamada_actual)

        # Inserta la última fila del Montecarlo a otra tabla aparte
        tablafinal.insert(parent='', index='end', values=llamada_actual)

    # Si el usuario selecciona utilizar la distribución POISSON para la generación de números
    else:
        start_time = time.time()  # Registra el tiempo de inicio
        llamada_actual = []
        con_acu = Registro()
        hasta = desde + 500

        # Recorre hora por hora
        for i in range(horas):
            # Genera el número que representa la cantidad de llamadas
            llamadas = normal.poisson(media)

            # Recorre llamada por llamada
            for j in range(llamadas):
                # Contador de número de llamada
                con_acu.nro_llamada += 1
                # Realiza una corrida del Montecarlo
                res = montecarlo(con_acu)
                # Guarda los valores generados en un vector
                llamada_actual = [str(i + 1), con_acu.nro_llamada, res[0], res[1], res[2], res[3], res[4], res[5],
                                  res[6], res[7]
                    , con_acu.atendidos_c, con_acu.ventas_c, con_acu.hombres_c, con_acu.hombres_gastos,
                                  con_acu.mujeres_c, con_acu.mujeres_gastos, con_acu.ingreso_total]

                # Comprueba si el número de llamada fue solicitado para mostrar por el usuario, y si es así, agrega la fila en la tabla
                if desde <= con_acu.nro_llamada <= hasta:
                    tablaintervalo.insert(parent='', index='end', values=llamada_actual)

        # Inserta la última fila del Montecarlo a otra tabla aparte
        tablafinal.insert(parent='', index='end', values=llamada_actual)

    end_time = time.time()  # Registra el tiempo de finalización

    elapsed_time = end_time - start_time  # Calcula el tiempo transcurrido

    # Imprime en la CONSOLA el tiempo que tardó en ejecutarse la Simulación
    print(f"La función tardó {elapsed_time:.2f} segundos en ejecutarse")
    return llamada_actual

# Función encargada de hacer una corrida del método Montecarlo
def montecarlo(reg):
    # Inicializa el vector con guiones para reemplazar por los valores en caso de que corresponda
    # ["RND Atiende", "Atiende SI/NO", "RND Género", "Género", "RND Compra", "Compra SI/NO", "RND Gasto", "Gasto"]
    resultado = ["-"]*8
    # Verifica si atiende o no y guarda el RND utilizado en el vector
    atiende_var, resultado[0] = atiende()

    # Si el cliente ATIENDE
    if atiende_var:
        # Contador de clientes que atendieron
        reg.atendidos_c += 1
        # Guarda el valor correspondiente en el vector
        resultado[1] = "Atiende"
        # Verifica el género del cliente y guarda el RND utilizado en el vector
        genero_var, resultado[2] = genero()

        # Si el cliente es HOMBRE
        if genero_var:
            # Guarda el género en el vector
            resultado[3] = "Hombre"
            # Verifica si compra o no y guarda el RND utilizado en el vector
            comprah_var, resultado[4] = compraH()

            # Si el cliente COMPRA
            if comprah_var:
                # Contador de los hombres que compraron
                reg.hombres_c += 1
                # Guarda el valor correspondiente en el vector
                resultado[5] = "SI"
                # Verifica qué monto gastó y guarda el RND utilizado en el vector
                monto_vendido, resultado[6] = gastoH()
                # Guarda el monto que gastó en el vector
                resultado[7] = monto_vendido
                # Contador de ventas
                reg.ventas_c += 1
                # Acumulador del ingreso total
                reg.ingreso_total += monto_vendido
                # Acumulador del monto gastado por hombres
                reg.hombres_gastos += monto_vendido

            # Si el cliente NO COMPRA
            else:
                # Guarda el resultado correspondiente en el vector
                resultado[5] = "NO"

        # Si el cliente es MUJER
        else:
            # Guarda el género en el vector
            resultado[3] = "Mujer"
            # Verifica si compra o no y guarda el RND utilizado en el vector
            compram_var, resultado[4] = compraM()

            # Si el cliente COMPRA
            if compram_var:
                # Guarda el valor correspondiente en el vector
                resultado[5] = "SI"
                # Contador de las mujeres que compraron
                reg.mujeres_c += 1
                # Verifica qué monto gastó y guarda el RND utilizado en el vector
                monto_vendido, resultado[6] = gastoM()
                # Guarda el monto que gastó en el vector
                resultado[7] = monto_vendido
                # Contador de ventas
                reg.ventas_c += 1
                # Acumulador del ingreso total
                reg.ingreso_total += monto_vendido
                # Acumulador del monto gastado por hombres
                reg.mujeres_gastos += monto_vendido

            # Si el cliente NO COMPRA
            else:
                # Guarda el resultado correspondiente en el vector
                resultado[5] = "NO"

    # Si el cliente NO ATIENDE
    else:
        # Guarda el valor correspondiente en el vector
        resultado[1] = "No atiende"

    # Devuelve el vector generado
    return resultado

# Función encargada de verificar si atiende o no (según las probabilidades del enunciado)
def atiende():
    rnd = truncar(random.random())
    if rnd < 0.15:
        return False, rnd
    else:
        return True, rnd

# Función encargada de verificar el género (según las probabilidades del enunciado)
def genero():
    rnd = truncar(random.random())
    if rnd < 0.2:
        return True, rnd #Hombre
    else:
        return False, rnd #Mujer

# Función encargada de verificar si el hombre compra o no (según las probabilidades del enunciado)
def compraH():
    rnd = truncar(random.random())
    if rnd < 0.4:
        return True, rnd
    else:
        return False, rnd

# Función encargada de verificar si la mujer compra o no (según las probabilidades del enunciado)
def compraM():
    rnd = truncar(random.random())
    if rnd < 0.7:
        return True, rnd
    else:
        return False, rnd

# Función encargada de verificar el monto gastado por el hombre (según las probabilidades del enunciado)
def gastoH():
    rnd = truncar(random.random())
    if rnd < 0.05:
        return 5, rnd
    elif rnd < 0.25:
        return 10, rnd
    elif rnd < 0.60:
        return 15, rnd
    else:
        return 25, rnd

# Función encargada de verificar el monto gastado por la mujer (según las probabilidades del enunciado)
def gastoM():
    rnd = truncar(random.random())
    if rnd < 0.2:
        return 5, rnd
    elif rnd < 0.8:
        return 10, rnd
    elif rnd < 0.95:
        return 15, rnd
    else:
        return 25, rnd

# Función para TRUNCAR
def truncar(numero):
    truncado = int(numero*100)/100
    return truncado
