
# Importar las bibliotecas necesarias
import PySimpleGUI as sg
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Función para calcular la trayectoria, distancia máxima y altura máxima
def calcular_trayectoria(v0, theta):
    theta_rad = np.radians(theta)
    g = 9.8
    t_total = (2 * v0 * np.sin(theta_rad)) / g
    t_intervalo = 0.01
    tiempos = np.arange(0, t_total, t_intervalo)
    x = v0 * np.cos(theta_rad) * tiempos
    y = v0 * np.sin(theta_rad) * tiempos - 0.5 * g * tiempos**2
    distancia_maxima = np.max(x)
    altura_maxima = np.max(y)
    return x, y, distancia_maxima, altura_maxima

# Función para graficar la trayectoria en el lienzo de matplotlib
def graficar_trayectoria(x, y, label):
    plt.plot(x, y, label=label)

# Definir el diseño de la interfaz gráfica con PySimpleGUI
layout = [
    [sg.Text('Número de proyectiles:'), sg.InputText(key='num_proyectiles')],
    [sg.Button('Ingresar')],
    [sg.Canvas(key='fig_canvas')],
    [sg.Multiline(size=(60, 5), key='resultados', disabled=True)],
    [sg.Exit()]
]

# Crear la ventana de PySimpleGUI con el diseño especificado
window = sg.Window('Parámetros de Proyectiles', layout, finalize=True)
fig_canvas = window['fig_canvas']
resultados_text = window['resultados']

# Configuración inicial del gráfico de matplotlib
plt.figure(figsize=(8, 6))
plt.title('Trayectoria de Proyectiles')
plt.xlabel('Distancia (m)')
plt.ylabel('Altura (m)')

# Ciclo principal del programa
while True:
    # Esperar eventos de la ventana
    event, values = window.read()

    # Salir del programa si se cierra la ventana o se presiona 'Exit'
    if event == sg.WINDOW_CLOSED or event == 'Exit':
        break

    # Procesar el evento si se presiona el botón 'Ingresar'
    if event == 'Ingresar':
        try:
            # Obtener el número de proyectiles del usuario
            num_proyectiles = int(values['num_proyectiles'])
            velocidades_iniciales = []
            angulos = []

            resultados = ""

            # Solicitar al usuario ingresar parámetros para cada proyectil
            for i in range(num_proyectiles):
                v0 = float(sg.popup_get_text(f"Ingrese la velocidad inicial del proyectil {i + 1} (m/s): "))
                theta = float(sg.popup_get_text(f"Ingrese el ángulo de lanzamiento del proyectil {i + 1} (grados): "))
                velocidades_iniciales.append(v0)
                angulos.append(theta)

                # Calcular la trayectoria, distancia máxima y altura máxima
                x, y, distancia_maxima, altura_maxima = calcular_trayectoria(v0, theta)
                etiqueta = f'V={v0}m/s, θ={theta}°'
                graficar_trayectoria(x, y, etiqueta)

                # Agregar resultados al texto
                resultados += f"Proyectil {i + 1}:\n"
                resultados += f"Distancia máxima: {distancia_maxima:.2f} m\n"
                resultados += f"Altura máxima: {altura_maxima:.2f} m\n\n"

            # Mostrar leyenda y gráfico
            plt.legend()

            # Integrar el gráfico con PySimpleGUI
            fig_canvas_agg = FigureCanvasTkAgg(plt.gcf(), fig_canvas.Widget)
            fig_canvas_agg.draw()
            fig_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)

            # Mostrar resultados en el cuadro de texto
            resultados_text.update(value=resultados)

        except ValueError:
            sg.popup_error('Por favor, ingrese valores numéricos válidos.')

# Cerrar la ventana al salir del ciclo principal
window.close()

