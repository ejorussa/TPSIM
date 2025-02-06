from montecarlo import inicio
import tkinter as tk
import tkinter.ttk as tkk


def btn_SIMULAR(media, de, horas, desde, tablaintervalo, tablafinal, titulo_promedio_ventas, titulo_promedio_ventasxhora,
                titulo_promedio_gastoxmujer, titulo_promedio_gastoxhombre, titulo_promedio_atendidos, ventana):
    ultima = inicio(float(txt_media.get()), txt_de.get(),
           int(txt_horas.get()), int(txt_desde.get()),
           tablaintervalo, tablaf)

    # calculamos promedios
    titulo_promedio_atendidos.config(text=("Promedio de atendidos por hora: " + str(round(ultima[10] / horas, 2))))
    titulo_promedio_ventas.config(text=("Promedio de ventas por hora: " + str(round(ultima[11] / horas, 2)) + " | "))
    titulo_promedio_gastoxhombre.config(text=("Promedio de gasto por Hombre: " + str(round(ultima[13] / ultima[12], 2))+ " | "))
    titulo_promedio_gastoxmujer.config(text=("Promedio de gasto por Mujer: " + str(round(ultima[15] / ultima[14], 2))+ " |  "))
    titulo_promedio_ventasxhora.config(text=("Promedio de Ingreso por hora: " + str(round(ultima[16] / horas, 2))+ " | "))


if __name__ == '__main__':

    # VENTANA DE INICIO

    ventana = tk.Tk()
    ventana.title("Inicio")
    ventana.configure(bg="white")
    ventana.geometry("1920x1080+10+10")

    # LABELS & INPUTS
    titulo_horas = tk.Label(ventana, text="Ingrese la cantidad de horas a simular:", background="white")
    titulo_horas.pack()
    txt_horas = tk.Entry(ventana)
    txt_horas.pack()
    var = tk.StringVar()

    # Creamos una función para habilitar o deshabilitar el Input
    def toggle_entry():
        if opcion_seleccionada.get() == "Normal":
            txt_de.config(state="normal")
        else:
            txt_de.delete(0, tk.END)  # Eliminar texto existente
            txt_de.insert(0, "")  # Insertar nuevo texto
            txt_de.config(state="disabled")

    opcion_seleccionada = tk.StringVar(value="Normal")

    # Creamos los radio buttons
    button1 = tk.Radiobutton(ventana, text="normal", variable=opcion_seleccionada, value="Normal", command=toggle_entry)
    button2 = tk.Radiobutton(ventana, text="poisson", variable=opcion_seleccionada, value="opcion_seleccionada", command=toggle_entry)

    # Los colocamos en la ventana
    button1.pack()
    button2.pack()

    titulo_media = tk.Label(ventana, text="Ingresar Media de llamadas por hora:", background="white")
    titulo_media.pack()
    txt_media = tk.Entry(ventana)
    txt_media.pack()

    titulo_de = tk.Label(ventana, text="Ingresar Desviación Estándar:", background="white")
    titulo_de.pack()
    txt_de = tk.Entry(ventana)
    txt_de.pack()

    titulo_desde = tk.Label(ventana, text="Ingresar el número de Hora desde la que desea ver información:", background="white")
    titulo_desde.pack()
    txt_desde = tk.Entry(ventana)
    txt_desde.pack()

    # BTN SIMULAR
    btn_simular = tk.Button(ventana, text="Simular", command=lambda: btn_SIMULAR(float(txt_media.get()), txt_de.get(),
                                                                                 int(txt_horas.get()), int(txt_desde.get()),
                                                                                 tablaintervalo, tablaf,
                                                                                 titulo_promedio_ventas,
                                                                                 titulo_promedio_ventasxhora,
                                                                                 titulo_promedio_gastoxmujer,
                                                                                 titulo_promedio_gastoxhombre,
                                                                                 titulo_promedio_atendidos, ventana))
    btn_simular.pack()

    # TABLAS
    columnas = ["Nro Hora", "Nro Llamada", "RND Atiende", "Atiende SI/NO", "RND Género", "Género", "RND Compra",
                "Compra SI/NO", "RND Gasto", "Dinero Gastado", "Cantidad de Atendidos", "Cantidad de Ventas",
                "Cantidad de Hombres", "Gastos de Hombres", "Cantidad de Mujeres", "Gastos de Mujeres",
                "Monto Recaudado"]
    tablaintervalo = tkk.Treeview(ventana, columns=[str(i) for i in range(17)], height=25)
    tablaf = tkk.Treeview(ventana, columns=[str(i) for i in range(17)], height=3)
    for col, nombre_columna in enumerate(columnas):
        tablaintervalo.column(column=col, width=100, minwidth=50, anchor='w')
        tablaintervalo.heading(column=col, text=nombre_columna, anchor='w')
        tablaf.column(column=col, width=100, minwidth=50, anchor='w')
        tablaf.heading(column=col, text=nombre_columna, anchor='w')
    tablaintervalo.pack()
    titulo_final = tk.Label(ventana, text="Ultima fila:")
    titulo_final.pack()
    tablaf.pack()

    internal_frame = tk.Frame(ventana)
    internal_frame.columnconfigure(0, weight=20)
    internal_frame.columnconfigure(1, weight=20)
    internal_frame.columnconfigure(2, weight=20)
    internal_frame.columnconfigure(3, weight=20)
    internal_frame.columnconfigure(4, weight=20)

    titulo_promedio_ventasxhora = tk.Label(internal_frame, text="Ingreso esperado por hora:          ")
    titulo_promedio_gastoxhombre = tk.Label(internal_frame, text="Promedio de gasto Hombre:          ")
    titulo_promedio_gastoxmujer = tk.Label(internal_frame, text="Promedio gasto mujer:               ")
    titulo_promedio_ventas = tk.Label(internal_frame, text="Promedio de ventas por hora:             ")
    titulo_promedio_atendidos = tk.Label(internal_frame, text="Promedio de atendidos por horas:      ")

    titulo_promedio_ventas.grid(row=0, column=0)
    titulo_promedio_ventasxhora.grid(row=0, column=1)
    titulo_promedio_gastoxmujer.grid(row=0, column=2)
    titulo_promedio_gastoxhombre.grid(row=0, column=3)
    titulo_promedio_atendidos.grid(row=0, column=4)

    internal_frame.pack()

    ventana.mainloop()


