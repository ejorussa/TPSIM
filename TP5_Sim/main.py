
import random

import distribuciones
from Servidores.cola import Cola
from Servidores.emplead import Empleado
from Servidores.empleado_reparacion import EmpleadoReparacion
from Clientes.cliente import Cliente
from Clientes.aparato_electrodomestico import Aparato
from distribuciones import numExponencial
import time
import tkinter as tk
from tkinter import ttk
import math


def mandar_a_reparacion(fin_atencion_empleado_1, fin_atencion_empleado_2, empleado_anterior):
    tiempo_demora_reparacion, rnd_reparacion = numExponencial(media_atencion_reparacion)
    if emp_reparacion_1.es_libre() and emp_reparacion_2.es_libre():
        tiempo_demora_reparacion *= 0.5
        fin_atencion_empleado_1 = tiempo_demora_reparacion + reloj
        emp_reparacion_1.ocupar(empleado_anterior.atendiendo_a)
        emp_reparacion_2.ayudar()
        emp_reparacion_1.atendiendo_a.estado = "Esperando aparato"
        emp_reparacion_1.atendiendo_a.aparato_electrodomestico.iniciar_reparacion(reloj)
    elif emp_reparacion_1.esta_ayudando() and emp_reparacion_2.es_ocupado():
        fin_atencion_empleado_2 = (fin_atencion_empleado_2 - reloj) / 0.5 + reloj
        fin_atencion_empleado_1 = tiempo_demora_reparacion + reloj
        emp_reparacion_1.ocupar(empleado_anterior.atendiendo_a)
        emp_reparacion_1.atendiendo_a.estado = "Esperando aparato"
        emp_reparacion_1.atendiendo_a.aparato_electrodomestico.iniciar_reparacion(reloj)
    elif emp_reparacion_2.esta_ayudando() and emp_reparacion_1.es_ocupado():
        fin_atencion_empleado_1 = (fin_atencion_empleado_1 - reloj) / 0.5 + reloj
        fin_atencion_empleado_2 = tiempo_demora_reparacion + reloj
        emp_reparacion_2.ocupar(empleado_anterior.atendiendo_a)
        emp_reparacion_2.atendiendo_a.estado = "Esperando aparato"
        emp_reparacion_2.atendiendo_a.aparato_electrodomestico.iniciar_reparacion(reloj)
    else:
        emp_reparacion_1.cola_empleado.agregar(empleado_anterior.atendiendo_a)
        tiempo_demora_reparacion = rnd_reparacion = ""
    return fin_atencion_empleado_1, fin_atencion_empleado_2, tiempo_demora_reparacion, rnd_reparacion

def obtener_minimo(a, b, c, d, e, f):
    variables = locals()  # Obtener diccionario con los nombres y valores de las variables
    minimo = min(variables.values())  # Obtener el valor mínimo

    for nombre, valor in variables.items():
        if valor == minimo:
            return minimo, nombre


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Inicio temporizador
    inicio = time.time()
    ventana = tk.Tk()
    vector_txt = ["evento", "reloj", "rnd_llegada_cliente", "tiempo_entre_llegada_cliente", "proxima_llegada_cliente",
              "rnd_fin_recepcion", "tiempo_demora_recepcion", "fin_atencion_recepcion",
              "rnd_reparacion", "tiempo_demora_reparacion", "fin_atencion_empleado_1", "fin_atencion_empleado_2",
              "rnd_inspeccion", "tiempo_demora_inspeccion", "fin_atencion_inspeccion",
              "rnd_fallos", "hay_fallas", " rnd_fin_atencion_cobro", "tiempo_demora_cobro", "fin_atencion_cobro",
              "estado_recepcion",
              "cola_recepcion", "estado1", "estado2", "cola_en_reparacion",
              "estado_inspeccion", "cola_inspeccion", "estado_cobro", "cola_cobro", " contador_tres_fases",
              "contador_atendidos",
              "contador_volvieron_a_reparacion", "contador_demoraron_mas30_en_fase",
              "ac_tiempo_demora_reparacion", "ac_tiempo_demora_de_los_que_no_esperaron"]
    tabla = ttk.Treeview(ventana, columns=tuple(f'col{i+1}' for i in range(35)), height=500)
    for i in range(35):
        tabla.heading(column=i, text=vector_txt[i])
        if i<13:
            tabla.column(i, width=100)
    tabla.pack()


    # Desde cuál hasta cuál mostrar

    # Parámetros para distribuciones
    media_llegada_clientes = 15
    media_atencion_recepcion = 3
    media_atencion_reparacion = 20
    media_atencion_inspeccion = 5
    media_atencion_cobro = 5

    # Cantidad de simulaciones
    num_sim = 500

    # Empleados (SERVIDORES)
    emp_recepcion = Empleado("Libre",Cola())

    cola_reparacion = Cola()
    emp_reparacion_1 = EmpleadoReparacion("Libre", cola_reparacion)
    emp_reparacion_2 = EmpleadoReparacion("Libre", cola_reparacion)

    emp_inspeccion = Empleado("Libre",Cola())

    emp_cobro = Empleado("Libre", Cola())

    # Vector Estado
    evento = ""
    reloj = 0
    # Evento llegada_cliente
    tiempo_entre_llegada_cliente, rnd_llegada_cliente = numExponencial(media_llegada_clientes)
    proxima_llegada_cliente = tiempo_entre_llegada_cliente + reloj
    # Evento fin_atencion_recepcion
    rnd_fin_recepcion = tiempo_demora_recepcion = fin_atencion_recepcion = ""
    # Evento fin_atencion_reparacion
    rnd_reparacion = tiempo_demora_reparacion = fin_atencion_empleado_1 = fin_atencion_empleado_2 = ""
    # Evento fin_atencion_inspeccion
    rnd_inspeccion = tiempo_demora_inspeccion = fin_atencion_inspeccion = rnd_fallos = hay_fallas = ""
    # Evento fin_atencion_cobro
    rnd_fin_atencion_cobro = tiempo_demora_cobro = fin_atencion_cobro = ""
    # Empleado recepción
    estado_recepcion, cola_recepcion = emp_recepcion.mostrar_info()
    # Empleado Reparación
    estado1 = emp_reparacion_1.estado
    estado2 = emp_reparacion_2.estado
    cola_en_reparacion = len(cola_reparacion.cola)
    # Empleado Inspección
    estado_inspeccion, cola_inspeccion = emp_inspeccion.mostrar_info()
    # Empleado Cobro
    estado_cobro, cola_cobro = emp_cobro.mostrar_info()
    # Contadores
    contador_tres_fases = contador_atendidos = contador_volvieron_a_reparacion = contador_demoraron_mas30_en_fase = 0
    # Acumuladores
    ac_tiempo_demora_reparacion = ac_tiempo_demora_de_los_que_no_esperaron = 0

    vector = [evento, reloj, rnd_llegada_cliente, tiempo_entre_llegada_cliente, proxima_llegada_cliente, rnd_fin_recepcion, tiempo_demora_recepcion, fin_atencion_recepcion,
              rnd_reparacion, tiempo_demora_reparacion, fin_atencion_empleado_1, fin_atencion_empleado_2, rnd_inspeccion, tiempo_demora_inspeccion, fin_atencion_inspeccion,
              rnd_fallos, hay_fallas, rnd_fin_atencion_cobro, tiempo_demora_cobro, fin_atencion_cobro, estado_recepcion, cola_recepcion, estado1, estado2, cola_en_reparacion,
              estado_inspeccion, cola_inspeccion, estado_cobro, cola_cobro, contador_tres_fases, contador_atendidos, contador_volvieron_a_reparacion, contador_demoraron_mas30_en_fase,
              ac_tiempo_demora_reparacion, ac_tiempo_demora_de_los_que_no_esperaron]
    tabla.insert(parent='', index='end', values=vector)
    # Podría borrarse, se declara en cada iteración del FOR
    proximos = {'Llegada cliente': vector[4], 'Fin atención recepción': vector[7], 'Fin atención reparación empleado 1': vector[10], 'Fin atención reparación empleado 2': vector[11], 'Fin atención inspección': vector[14], 'Fin atención cobro': vector[17]}
    llaves = 'Llegada cliente', 'Fin atención recepción', 'Fin atención reparación empleado 1', 'Fin atención reparación empleado 2', 'Fin atención inspección','Fin atención cobro'
    indices = 4, 7, 10, 11, 14, 19
    for i in range(num_sim):
        vector_ant = [evento, reloj, rnd_llegada_cliente, tiempo_entre_llegada_cliente, proxima_llegada_cliente,
                      rnd_fin_recepcion, tiempo_demora_recepcion, fin_atencion_recepcion,
                      rnd_reparacion, tiempo_demora_reparacion, fin_atencion_empleado_1, fin_atencion_empleado_2,
                      rnd_inspeccion, tiempo_demora_inspeccion, fin_atencion_inspeccion,
                      rnd_fallos, hay_fallas, rnd_fin_atencion_cobro, tiempo_demora_cobro, fin_atencion_cobro,
                      estado_recepcion, cola_recepcion, estado1, estado2, cola_en_reparacion,
                      estado_inspeccion, cola_inspeccion, estado_cobro, cola_cobro, contador_tres_fases, contador_atendidos,
                      contador_volvieron_a_reparacion, contador_demoraron_mas30_en_fase,
                      ac_tiempo_demora_reparacion, ac_tiempo_demora_de_los_que_no_esperaron]
        proximos = {}
        for j in range(5):
            if str(vector[indices[j]]) != "":
                proximos[llaves[j]] = (float(vector[indices[j]]))

        minimo = min(proximos.values())
        for nombre, valor in proximos.items():

            if valor == minimo:
                reloj, evento = minimo, nombre
                break

        # Evento llegada_cliente
        if evento == 'Llegada cliente':
            # Calcula la próxima llegada
            tiempo_entre_llegada_cliente, rnd_llegada_cliente = numExponencial(media_llegada_clientes)
            proxima_llegada_cliente = tiempo_entre_llegada_cliente + reloj
            if emp_recepcion.es_libre():
                aparato = Aparato("Siendo Atendido", reloj, 0, False)
                cliente = Cliente(aparato, "Siendo Atendido")
                emp_recepcion.ocupar(cliente)
                estado_recepcion = emp_recepcion.estado
                tiempo_demora_recepcion, rnd_fin_recepcion = numExponencial(media_atencion_recepcion)
                fin_atencion_recepcion = reloj + tiempo_demora_recepcion

            else:
                aparato = Aparato("Esperando Recepcion", 0, 0, True)
                cliente = Cliente(aparato, "Esperando recepcion")
                emp_recepcion.cola_empleado.agregar(cliente)
                cola_recepcion = len(emp_recepcion.cola_empleado)
                tiempo_entre_llegada_cliente = rnd_llegada_cliente = ""


# HACE FALTA VACIAR LOS CAMPOS RND Y EL TIEMPO DEMORA CUANDO NO SE RECALCULAN
# REESCRIBIR LOS TEXTOS DE LOS ESTADOS DE LOS EMPLEADOS CUANDO NO HAY NADIE EN LA COLA Y EL EVENTO ES FIN ATENCIÓN

        # Evento fin_atencion_recepcion
        elif evento == 'Fin atención recepción':
            fin_atencion_empleado_1, fin_atencion_empleado_2, tiempo_demora_reparacion, rnd_reparacion = mandar_a_reparacion(fin_atencion_empleado_1, fin_atencion_empleado_2, emp_recepcion)

            if len(emp_recepcion.cola_empleado) > 0:
                emp_recepcion.atendiendo_a = emp_recepcion.cola_empleado.sacar()
                tiempo_demora_recepcion, rnd_fin_recepcion = numExponencial(media_atencion_recepcion)
                fin_atencion_recepcion = reloj + tiempo_demora_recepcion
            else:
                emp_recepcion.desocupar()
                fin_atencion_recepcion = rnd_fin_recepcion = tiempo_demora_recepcion = ""
            cola_recepcion = len(emp_recepcion.cola_empleado)

        # Evento fin_atencion_reparacion_1
        elif evento == 'Fin atención reparación empleado 1':
            if emp_reparacion_2.esta_ayudando() and emp_reparacion_1.es_ocupado():
                emp_reparacion_2.desocupar() # esto faltaba
            if emp_inspeccion.es_libre():
                tiempo_demora_inspeccion, rnd_inspeccion = distribuciones.poisson(media_atencion_inspeccion)
                fin_atencion_inspeccion = tiempo_demora_inspeccion + reloj
                emp_inspeccion.ocupar(emp_reparacion_1.atendiendo_a)
                emp_inspeccion.atendiendo_a.aparato_electrodomestico.estado = "Siendo Inspeccionado"
            else:
                emp_inspeccion.cola_empleado.agregar(emp_reparacion_1.atendiendo_a)
                emp_reparacion_1.atendiendo_a.aparato_electrodomestico.estado = "Esperando Inspeccion"
            emp_reparacion_1.desocupar()
            if len(emp_reparacion_1.cola_empleado) > 0:
                tiempo_demora_reparacion, rnd_reparacion = numExponencial(media_atencion_reparacion)
                if emp_reparacion_2.es_libre():    # --> Se podría validar tranquilamente con if emp_remparacion.es_libre()
                    tiempo_demora_reparacion *= 0.5
                    emp_reparacion_2.ayudar()
                fin_atencion_empleado_1 = reloj + tiempo_demora_reparacion
                emp_reparacion_1.ocupar(cola_reparacion.sacar())
            elif len(cola_reparacion.cola) == 0:
                tiempo_demora_reparacion = rnd_reparacion = fin_atencion_empleado_1 = ""
                if emp_reparacion_2.es_ocupado():
                    fin_atencion_empleado_2 = (fin_atencion_empleado_2 - reloj) * 0.5 + reloj
                    emp_reparacion_1.ayudar()

        # Evento fin_atencion_reparacion_2
        elif evento == 'Fin atención reparación empleado 2':
            if emp_reparacion_1.esta_ayudando() and emp_reparacion_2.es_ocupado():
                emp_reparacion_1.desocupar()   # esto faltaba
            if emp_inspeccion.es_libre():
                tiempo_demora_inspeccion, rnd_inspeccion = distribuciones.poisson(media_atencion_inspeccion)
                fin_atencion_inspeccion = tiempo_demora_inspeccion + reloj
                emp_inspeccion.ocupar(emp_reparacion_2.atendiendo_a)
                emp_inspeccion.atendiendo_a.aparato_electrodomestico.estado = "Siendo Inspeccionado"
            else:
                emp_inspeccion.cola_empleado.agregar(emp_reparacion_2.atendiendo_a)
                emp_reparacion_2.atendiendo_a.aparato_electrodomestico.estado = "Esperando Inspeccion"
            emp_reparacion_2.desocupar()
            if len(cola_reparacion.cola) > 0:
                tiempo_demora_reparacion, rnd_reparacion = numExponencial(media_atencion_reparacion)
                if emp_reparacion_1.es_libre():
                    tiempo_demora_reparacion *= 0.5
                    emp_reparacion_1.ayudar()
                fin_atencion_empleado_2 = reloj + tiempo_demora_reparacion
                emp_reparacion_2.ocupar(emp_reparacion_1.cola_empleado.sacar())
            elif len(cola_reparacion.cola) == 0:
                tiempo_demora_reparacion = rnd_reparacion = fin_atencion_empleado_2 = ""
                if emp_reparacion_1.es_ocupado():
                    fin_atencion_empleado_1 = (fin_atencion_empleado_1 - reloj) * 0.5 + reloj
                    emp_reparacion_2.ayudar()

        # Evento fin_atencion_inspeccion
        elif evento == 'Fin atención inspección':
            hay_fallas = False
            rnd_fallos = round(random.random(), 2)
            if rnd_fallos < 0.25:
                hay_fallas = True
                mandar_a_reparacion(fin_atencion_empleado_1, fin_atencion_empleado_2, emp_inspeccion)
                emp_inspeccion.atendiendo_a.aparato_electrodomestico.iniciar_reparacion(reloj)
            elif emp_cobro.es_libre():
                emp_cobro.ocupar(emp_inspeccion.atendiendo_a)
                tiempo_demora_cobro, rnd_fin_atencion_cobro = distribuciones.numExponencial(media_atencion_cobro)
                fin_atencion_cobro = tiempo_demora_cobro + reloj
                emp_cobro.atendiendo_a.estado = "Siendo Cobrado"
            else:
                emp_cobro.cola_empleado.agregar(emp_inspeccion.atendiendo_a)
                emp_inspeccion.atendiendo_a.estado = "Esperando Cobro"
            emp_inspeccion.desocupar()
            if len(emp_inspeccion.cola_empleado) > 0: # se fija en la cola y si hay lo atiende
                emp_inspeccion.ocupar(emp_inspeccion.cola_empleado.sacar())
                tiempo_demora_inspeccion, rnd_inspeccion = distribuciones.poisson(media_atencion_inspeccion)
                fin_atencion_inspeccion = tiempo_demora_inspeccion + reloj
                emp_inspeccion.atendiendo_a.aparato_electrodomestico.estado = "Siendo Inspeccionado"
            elif len(emp_inspeccion.cola_empleado) == 0:
                fin_atencion_inspeccion = rnd_inspeccion = tiempo_demora_inspeccion = ""


        # Evento fin atencion cobro
        elif evento == 'Fin atención cobro':
            if len(emp_cobro.cola_empleado) > 0:
                tiempo_demora_cobro, rnd_fin_atencion_cobro = distribuciones.numExponencial(media_atencion_cobro)
                fin_atencion_cobro = tiempo_demora_cobro + reloj
                emp_cobro.ocupar(emp_cobro.cola_empleado.sacar())
                emp_cobro.atendiendo_a.estado = "Siendo Cobrado"
            else:
                emp_cobro.desocupar()
                rnd_fin_atencion_cobro = ""

        cola_en_reparacion = len(emp_reparacion_1.cola_empleado)
        cola_recepcion = len(emp_recepcion.cola_empleado)
        cola_cobro = len(emp_cobro.cola_empleado)
        cola_inspeccion = len(emp_inspeccion.cola_empleado)
        vector = [evento, reloj, rnd_llegada_cliente, tiempo_entre_llegada_cliente, proxima_llegada_cliente,
                  rnd_fin_recepcion, tiempo_demora_recepcion, fin_atencion_recepcion,
                  rnd_reparacion, tiempo_demora_reparacion, fin_atencion_empleado_1, fin_atencion_empleado_2,
                  rnd_inspeccion, tiempo_demora_inspeccion, fin_atencion_inspeccion,
                  rnd_fallos, hay_fallas, rnd_fin_atencion_cobro, tiempo_demora_cobro, fin_atencion_cobro,
                  estado_recepcion,
                  cola_recepcion, estado1, estado2, cola_en_reparacion,
                  estado_inspeccion, cola_inspeccion, estado_cobro, cola_cobro, contador_tres_fases, contador_atendidos,
                  contador_volvieron_a_reparacion, contador_demoraron_mas30_en_fase,
                  ac_tiempo_demora_reparacion, ac_tiempo_demora_de_los_que_no_esperaron]

        for n in range(len(vector)):
            if n in [2, 3,5,6,8,9,12,13,15,16,17,18]:
                if str(vector[n]) == str(vector_ant[n]):
                    vector[n] = ""

        if i < 500:
            tabla.insert(parent='', index='end', values=vector)
            print(vector)
    # Finalizo temporizador
    fin = time.time()
    tiempo_transcurrido = fin - inicio
    print(tiempo_transcurrido)
    ventana.mainloop()


