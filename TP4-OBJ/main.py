from Servidores.cola import Cola
from Servidores.empleado_recepcion import EmpleadoRecepcion
from Servidores.empleado_reparacion import EmpleadoReparacion
from Servidores.empleado_inspeccion import EmpleadoInspeccion
from Servidores.empleado_cobro import EmpleadoCobro
from Clientes.cliente import Cliente
from Clientes.aparato_electrodomestico import Aparato
from distribuciones import numExponencial
import tkinter as tk
import pandas as pd
from tkinter import messagebox

def simular(n, clientes,recepcion, reparacion,inspeccion,cobro, nombre, intervalo):

    # VALIDACIONES
    if nombre == "":
        messagebox.showinfo("Archivo SIN NOMBRE!", "Por favor, ingrese un nombre para el archivo Excel...")
    else:
        # Vector que corresponde a la fila de los títulos en el Excel
        vector_txt = ["Evento", "Reloj", "RND", "Tiempo entre llegadas", "Próxima llegada cliente",
                      "RND", "Tiempo demora recepción", "Fin atención recepción",
                      "RND", "Tiempo demora reparación", "Fin reparación empleado 1", "Fin reparación empleado 2",
                      "RND", "Tiempo demora inspección", "Fin atención inspección",
                      "RND", "Hay fallas SI/NO", " RND", "Tiempo demora cobro", "Fin atención cobro",
                      "Estado empleado Recepción", "Cola Recepción", "Estado empleado Reparación 1",
                      "Estado empleado Reparación 2", "Cola Reparación",
                      "Estado empleado Inspección", "Cola Inspección", "Estado empleado Cobro", "Cola Cobro",
                      "Contador aparatos que no esperaron",
                      "Contador aparatos entendidos",
                      "Contador de aparatos que volvieron a reparación", "Contador de aparatos que demoraron más de 30'",
                      "AC tiempo demora en reparación", "AC tiempo de demora en 3 fases de aparatos que no esperaron"]

        # Definir la ruta y el nombre del archivo de Excel
        archivo_excel = nombre + '.xlsx'

        # Crear un DataFrame vacío
        df = pd.DataFrame()
        df_temporal = pd.DataFrame([])

        # Añadir la nueva fila al DataFrame principal
        df = pd.concat([df, df_temporal], ignore_index=True)

        # Parámetros para distribuciones
        media_llegada_clientes = clientes
        media_atencion_recepcion = recepcion
        media_atencion_reparacion = reparacion
        media_atencion_inspeccion = inspeccion
        media_atencion_cobro = cobro

        # Cantidad de simulaciones
        num_sim = n

        # Empleados (SERVIDORES)
        emp_recepcion = EmpleadoRecepcion("Libre", Cola(), media_atencion_recepcion)

        cola_reparacion = Cola()
        emp_reparacion_1 = EmpleadoReparacion("Libre", cola_reparacion, media_atencion_reparacion)
        emp_reparacion_2 = EmpleadoReparacion("Libre", cola_reparacion, media_atencion_reparacion)
        emp_reparacion_1.compañero = emp_reparacion_2
        emp_reparacion_2.compañero = emp_reparacion_1

        emp_inspeccion = EmpleadoInspeccion("Libre", Cola(), media_atencion_inspeccion)

        emp_cobro = EmpleadoCobro("Libre", Cola(), media_atencion_cobro)

        # VECTOR ESTADO
        evento = ""
        reloj = 0
        # Evento llegada_cliente
        tiempo_entre_llegada_cliente, rnd_llegada_cliente = numExponencial(media_llegada_clientes)
        proxima_llegada_cliente = tiempo_entre_llegada_cliente + reloj
        # Los otros eventos y los servidores se manejan a  partir de los atributos de los objetos
        # Contadores
        contador_tres_fases = contador_atendidos = contador_volvieron_a_reparacion = contador_demoraron_mas30_en_fase = 0
        # Acumuladores
        ac_tiempo_demora_reparacion = ac_tiempo_demora_de_los_que_no_esperaron = 0

        # Vector ESTADO inicial
        vector = [evento, reloj, rnd_llegada_cliente, tiempo_entre_llegada_cliente, proxima_llegada_cliente,
                  emp_recepcion.rnd, emp_recepcion.tiempo_demora, emp_recepcion.fin,
                  emp_reparacion_1.rnd, emp_reparacion_1.tiempo_demora, emp_reparacion_1.fin, emp_reparacion_2.fin,
                  emp_inspeccion.rnd, emp_inspeccion.tiempo_demora, emp_inspeccion.fin,
                  emp_inspeccion.rnd_hay_fallos, "", emp_cobro.rnd, emp_cobro.tiempo_demora, emp_cobro.fin,
                  emp_recepcion.estado,
                  len(emp_recepcion.cola_empleado), emp_reparacion_1.estado, emp_reparacion_2.estado,
                  len(emp_reparacion_1.cola_empleado),
                  emp_inspeccion.estado, len(emp_inspeccion.cola_empleado), emp_cobro.estado, len(emp_cobro.cola_empleado),
                  contador_tres_fases, contador_atendidos,
                  contador_volvieron_a_reparacion, contador_demoraron_mas30_en_fase,
                  ac_tiempo_demora_reparacion, ac_tiempo_demora_de_los_que_no_esperaron]

        # Inicialización del vector de clientes que van a entrar en la simulación
        clientes = []
        contador = 0   # Para saber el número de cliente
        vector_txt_0 = ["", "", "llegada_cliente", "", "", "fin_atencion_recepcion", "", "", "fin_atencion_reparacion_i",
                        "", "", "", "fin_atencion_inspeccion", "", "", "", "",
                        "fin_atencion_cobro", "", "", "Empleado Recepción", "", "Empleado Reparación", "", "",
                        "Empleado Inspección", "", "Empleado Cobro", "",
                        "", "", "", "", "", ""]  # *35

        # tabla.insert(parent='', index='end', values=vector)
        # Podría borrarse, se declara en cada iteración del FOR
        '''proximos = {'Llegada cliente': vector[4], 'Fin atención recepción': vector[7],
                    'Fin atención reparación empleado 1': vector[10], 'Fin atención reparación empleado 2': vector[11],
                    'Fin atención inspección': vector[14], 'Fin atención cobro': vector[19]}'''

        # Método para saber próximo evento (diccionario)
        llaves = 'Llegada cliente', 'Fin atención recepción', 'Fin atención reparación empleado 1', 'Fin atención reparación empleado 2', 'Fin atención inspección', 'Fin atención cobro'
        indices = 4, 7, 10, 11, 14, 19

        # Creación del DataFrame para el Excel
        df_temporal = pd.DataFrame([vector])
        # Añadir la nueva fila al DataFrame principal
        df = pd.concat([df, df_temporal], ignore_index=True)

        # ITERACIONES de la simulación
        for i in range(num_sim):
            vector_ant = [evento, reloj, rnd_llegada_cliente, tiempo_entre_llegada_cliente, proxima_llegada_cliente,
                          emp_recepcion.rnd, emp_recepcion.tiempo_demora, emp_recepcion.fin,
                          emp_reparacion_1.rnd, emp_reparacion_1.tiempo_demora, emp_reparacion_1.fin, emp_reparacion_2.fin,
                          emp_inspeccion.rnd, emp_inspeccion.tiempo_demora, emp_inspeccion.fin,
                          emp_inspeccion.rnd_hay_fallos, emp_inspeccion.hay_fallos, emp_cobro.rnd, emp_cobro.tiempo_demora,
                          emp_cobro.fin, emp_recepcion.estado,
                          len(emp_recepcion.cola_empleado), emp_reparacion_1.estado, emp_reparacion_2.estado,
                          len(emp_reparacion_1.cola_empleado),
                          emp_inspeccion.estado, len(emp_inspeccion.cola_empleado), emp_cobro.estado,
                          len(emp_cobro.cola_empleado), contador_tres_fases, contador_atendidos,
                          contador_volvieron_a_reparacion, contador_demoraron_mas30_en_fase,
                          ac_tiempo_demora_reparacion, ac_tiempo_demora_de_los_que_no_esperaron]

            # Se verifica el próximo evento
            proximos = {}
            for j in range(6):
                if str(vector[indices[j]]) != "":
                    proximos[llaves[j]] = (float(vector[indices[j]]))

            minimo = min(proximos.values())
            for nombre, valor in proximos.items():

                if valor == minimo:
                    reloj, evento = minimo, nombre
                    break

            # Evento llegada_cliente
            if evento == 'Llegada cliente':
                tiempo_entre_llegada_cliente, rnd_llegada_cliente = numExponencial(media_llegada_clientes)
                proxima_llegada_cliente = tiempo_entre_llegada_cliente + reloj
                cliente = Cliente(Aparato("", reloj, "", False), "")
                emp_recepcion.atender(cliente, reloj)
                contador += 1
                if intervalo > i:
                    clientes.append(cliente)
                # cambiar
                elif intervalo < i < (intervalo + 500):
                    vector_txt_0.append(str(contador))
                    vector_txt_0.append(str(contador))
                    vector_txt_0.append(str(contador))
                    vector_txt_0.append(str(contador))
                    vector_txt_0.append(str(contador))
                    clientes.append(cliente)
                    vector_txt.append("Estado Cliente")
                    vector_txt.append("Estado Aparato")
                    vector_txt.append("Hora llegada")
                    vector_txt.append("Hora Inicio Reparacion")
                    vector_txt.append("Esperó SI/NO ")

            # Evento fin_atencion_recepcion
            elif evento == 'Fin atención recepción':
                emp_recepcion.pasar_a(emp_reparacion_1, reloj)
                emp_recepcion.atender_siguiente(reloj)

            # Evento fin_atencion_reparacion_1
            elif evento == 'Fin atención reparación empleado 1':
                tiempo_reparacion = emp_reparacion_1.pasar_a(emp_inspeccion, reloj)
                emp_reparacion_1.atender_siguiente(reloj)
                ac_tiempo_demora_reparacion += tiempo_reparacion

            # Evento fin_atencion_reparacion_2
            elif evento == 'Fin atención reparación empleado 2':
                tiempo_reparacion = emp_reparacion_2.pasar_a(emp_inspeccion, reloj)
                emp_reparacion_2.atender_siguiente(reloj)
                ac_tiempo_demora_reparacion += tiempo_reparacion

            # Evento fin_atencion_inspeccion
            elif evento == 'Fin atención inspección':
                a, e, r, mas30, tiempo_en_3_fases = emp_inspeccion.revisar(emp_cobro, emp_reparacion_1, reloj)
                contador_atendidos += a
                contador_tres_fases += e
                contador_volvieron_a_reparacion += r
                contador_demoraron_mas30_en_fase += mas30
                ac_tiempo_demora_de_los_que_no_esperaron += tiempo_en_3_fases
                emp_inspeccion.atender_siguiente(reloj)

            # Evento fin atencion cobro
            else:
                # elif evento == 'Fin atención cobro':
                emp_cobro.atendiendo_a.finalizar()
                emp_cobro.atender_siguiente(reloj)

            vector = [evento, reloj, rnd_llegada_cliente, tiempo_entre_llegada_cliente, proxima_llegada_cliente,
                      emp_recepcion.rnd, emp_recepcion.tiempo_demora, emp_recepcion.fin,
                      emp_reparacion_1.rnd, emp_reparacion_1.tiempo_demora, emp_reparacion_1.fin, emp_reparacion_2.fin,
                      emp_inspeccion.rnd, emp_inspeccion.tiempo_demora, emp_inspeccion.fin,
                      emp_inspeccion.rnd_hay_fallos, emp_inspeccion.hay_fallos, emp_cobro.rnd, emp_cobro.tiempo_demora,
                      emp_cobro.fin, emp_recepcion.estado,
                      len(emp_recepcion.cola_empleado), emp_reparacion_1.estado, emp_reparacion_2.estado,
                      len(emp_reparacion_1.cola_empleado),
                      emp_inspeccion.estado, len(emp_inspeccion.cola_empleado), emp_cobro.estado,
                      len(emp_cobro.cola_empleado), contador_tres_fases, contador_atendidos,
                      contador_volvieron_a_reparacion, contador_demoraron_mas30_en_fase,
                      ac_tiempo_demora_reparacion, ac_tiempo_demora_de_los_que_no_esperaron]

            for n in range(len(vector)):
                if n in [2, 3, 5, 6, 8, 9, 12, 13, 15, 16, 17, 18]:
                    if str(vector[n]) == str(vector_ant[n]) and n != 16:
                        vector[n] = ""
                    if vector[15] == "" and n == 16:
                        vector[n] = ""
            if intervalo > i:
                for cliente in clientes:
                    if cliente.estado == "Cobrado":
                        clientes.remove(cliente)
            if intervalo < i < (intervalo + 500):
                for j in range(len(clientes)):
                    if clientes[j] == 1 or clientes[j].estado == "Cobrado":
                        vector.append("")
                        vector.append("")
                        vector.append("")
                        vector.append("")
                        vector.append("")
                        clientes[j] = 1
                    else:
                        vector.append(clientes[j].estado)
                        vector.append(clientes[j].aparato_electrodomestico.estado)
                        vector.append(clientes[j].aparato_electrodomestico.inicio_atencion)
                        vector.append(clientes[j].aparato_electrodomestico.inicio_reparacion)
                        vector.append(clientes[j].aparato_electrodomestico.esperando)

                df_temporal = pd.DataFrame([vector])
                # Añadir la nueva fila al DataFrame principal
                df = pd.concat([df, df_temporal], ignore_index=True)

        df = pd.concat([pd.DataFrame([vector_txt], index=[0]), df]).reset_index(drop=True)
        df = pd.concat([pd.DataFrame([vector_txt_0], index=[0]), df]).reset_index(drop=True)
        df.to_excel(archivo_excel, index=False)

        # MÉTRICAS
        txt_probabilidad_aparato_no_espera_3fases.configure(text="Probabilidad de que un aparato no tenga que esperar en ninguna de las 3 fases: " +
                                                                  str(contador_tres_fases/contador_atendidos * 100) + "%")
        txt_tiempo_medio_aparato_no_espero_3fases.configure(text="Tiempo medio que se tarda en devolver el aparato si no esperó en ninguna de las 3 fases: " +
                                                                 str(ac_tiempo_demora_de_los_que_no_esperaron/contador_tres_fases))
        txt_porcentaje_aparatos_volvieron_reparacion.configure(text="Porcentaje de los aparatos que volvieron a la fase de reparación: " +
                                                               str(contador_volvieron_a_reparacion/contador_atendidos * 100)+ "%")
        txt_tiempo_medio_en_reparacion.configure(text="Tiempo medio que tarda un aparato en la fase de reparación: " +
                                                 str(ac_tiempo_demora_reparacion/contador_atendidos))
        txt_aparatos_mas_30mins.configure(text="Cantidad de aparatos que tardaron más de 30 minutos en ser devueltos al cliente: " +
                                          str(contador_demoraron_mas30_en_fase))


if __name__ == '__main__':

    # Creación de la ventana
    ventana = tk.Tk()
    ventana.title("Inicio")
    ventana.configure(bg="white")
    ventana.geometry("1300x620+10+10")
    titulo_intervalo = tk.Label(ventana, text="Ingrese desde que simulacion desea ver informacion:", background="white")
    titulo_intervalo.pack()
    txt_nros_intervalo = tk.Entry(ventana)
    txt_nros_intervalo.pack()
    titulo_simulaciones = tk.Label(ventana, text="Ingrese la cantidad de simulaciones:", background="white")
    titulo_simulaciones.pack()
    txt_nros_simulaciones = tk.Entry(ventana)
    txt_nros_simulaciones.pack()
    titulo_media_llegada_clientes = tk.Label(ventana, text="Ingrese la media para el evento llegada_cliente:", background="white")
    titulo_media_llegada_clientes.pack()
    txt_media_llegada_clientes = tk.Entry(ventana)
    txt_media_llegada_clientes.pack()
    titulo_fin_atencion_recepcion = tk.Label(ventana, text="Ingrese la media para el evento fin_atencion_cliente:", background="white")
    titulo_fin_atencion_recepcion.pack()
    txt_fin_atencion_recepcion = tk.Entry(ventana)
    txt_fin_atencion_recepcion.pack()
    titulo_fin_reparacion = tk.Label(ventana, text="Ingrese la media para el evento fin_atencion_reparacion:", background="white")
    titulo_fin_reparacion.pack()
    txt_fin_reparacion = tk.Entry(ventana)
    txt_fin_reparacion.pack()
    titulo_fin_inspeccion= tk.Label(ventana, text="Ingrese la media para el evento fin_inspeccion:", background="white")
    titulo_fin_inspeccion.pack()
    txt_fin_inspeccion = tk.Entry(ventana)
    txt_fin_inspeccion.pack()
    titulo_fin_cobro = tk.Label(ventana, text="Ingrese la media para el evento fin_cobro:", background="white")
    titulo_fin_cobro.pack()
    txt_fin_cobro = tk.Entry(ventana)
    txt_fin_cobro.pack()
    titulo_nombre = tk.Label(ventana, text="Ingrese nombre para el Excel:", background="white")
    titulo_nombre.pack()
    txt_nombre = tk.Entry(ventana)
    txt_nombre.pack()

    btn_simular = tk.Button(ventana, text="Simular", command=lambda: simular(int(txt_nros_simulaciones.get()),
                                                                                int(txt_media_llegada_clientes.get()),
                                                                                int(txt_fin_atencion_recepcion.get()),
                                                                                int(txt_fin_reparacion.get()),
                                                                                int(txt_fin_inspeccion.get()),
                                                                                int(txt_fin_cobro.get()),
                                                                                txt_nombre.get(), int(txt_nros_intervalo.get())
                                                                                 ))
    btn_simular.pack()

    # MÉTRICAS (Labels)
    txt_probabilidad_aparato_no_espera_3fases = tk.Label(ventana, text="Probabilidad de que un aparato no tenga que esperar en ninguna de las 3 fases: ", background="white")
    txt_probabilidad_aparato_no_espera_3fases.pack()
    txt_tiempo_medio_aparato_no_espero_3fases = tk.Label(ventana, text="Tiempo medio que se tarda en devolver el aparato si no esperó en ninguna de las 3 fases: ", background="white")
    txt_tiempo_medio_aparato_no_espero_3fases.pack()
    txt_porcentaje_aparatos_volvieron_reparacion = tk.Label(ventana, text="Porcentaje de los aparatos que volvieron a la fase de reparación: ", background="white")
    txt_porcentaje_aparatos_volvieron_reparacion.pack()
    txt_tiempo_medio_en_reparacion = tk.Label(ventana, text="Tiempo medio que tarda un aparato en la fase de reparación: ", background="white")
    txt_tiempo_medio_en_reparacion.pack()
    txt_aparatos_mas_30mins = tk.Label(ventana, text="Cantidad de aparatos que tardaron más de 30 minutos en ser devueltos al cliente: ", background="white")
    txt_aparatos_mas_30mins.pack()

    ventana.mainloop()





