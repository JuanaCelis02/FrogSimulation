import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageDraw, ImageFont
import tkinter as tk
from tkinter import ttk
import time

# Crear la ventana
window = tk.Tk()
fig, ax = plt.subplots()
iteration = 0
finalPositions = []

window.title("Frog Simulation")

# Crear la tabla de información de las simulaciones
tv = ttk.Treeview(window, columns=("Col1", "Col2", "Col3"))
tv.grid(row=2, column=2)

tv.column("#0", width=40)
tv.column("Col1", width=120, anchor="center")
tv.column("Col2", width=120, anchor="center")
tv.column("Col3", width=120, anchor="center")

tv.heading("#0", text="#", anchor="center")
tv.heading("Col1", text="Saltos", anchor="center")
tv.heading("Col2", text="Posicion final", anchor="center")
tv.heading("Col3", text="Tiempos(Ms)", anchor="center")

# Función para simular los saltos de la rana
def simulate_frog_jumps():
    actualPosition = 0
    jumpsMade = 0
    frequentPositions = {0: 1}

    for _ in range(1000000):
        jump = random.randint(0, 1)

        if jump == 0:
            actualPosition -= 1
        else:
            actualPosition += 1

        jumpsMade += 1

        if actualPosition in frequentPositions:
            frequentPositions[actualPosition] += 1
        else:
            frequentPositions[actualPosition] = 1

    return actualPosition, frequentPositions

# Función para mostrar las estadísticas en la tabla
def display_stats(iteration, actualPosition, executionTime):
    tv.insert("", "end", text=iteration, values=("1,000,000", actualPosition, executionTime))

# Función para mostrar el gráfico de barras
def display_bar_chart(frequentPositions):
    ax.clear()
    ax.bar(frequentPositions.keys(), frequentPositions.values(), align='center')
    ax.set_xlabel('Position')
    ax.set_ylabel('Frequency')
    ax.set_title('Frequency of positions reached by the frog')
    fig.set_size_inches(6, 4)
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().grid(row=1, column=0)

# Función para mostrar el histograma de posiciones finales
def display_histogram(finalPositions):
    fig2, ax2 = plt.subplots()
    ax2.hist(finalPositions)
    ax2.set_xlabel('Position')
    ax2.set_ylabel('Frequency')
    ax2.set_title('Frequency of final frog positions')
    fig2.set_size_inches(6, 4)
    canvas2 = FigureCanvasTkAgg(fig2, master=window)
    canvas2.draw()
    canvas2.get_tk_widget().grid(row=1, column=2)

# Función para crear la imagen de la rana
def create_frog_image(actualPosition):
    image = Image.new('RGB', (500, 500), 'black')
    draw = ImageDraw.Draw(image)

    frog = Image.open('rana.png')
    frog = frog.resize((100, 100))

    draw.line([(50, 250), (450, 250)], fill='white', width=5)
    image.paste(frog, (200, 140))

    font = ImageFont.truetype('arial.ttf', 36)
    draw.text((220, 250), str(actualPosition), fill='white', font=font)

    image.show()

# Función principal para la simulación
def simulation():
    start = time.time()
    actualPosition, frequentPositions = simulate_frog_jumps()
    end = time.time()

    global iteration
    iteration += 1
    executionTime = (end - start) * 1000

    finalPositions.append(actualPosition)

    display_stats(iteration, actualPosition, executionTime)
    display_bar_chart(frequentPositions)
    display_histogram(finalPositions)
    create_frog_image(actualPosition)

# Función para cerrar la ventana
def close():
    plt.close(fig)
    window.destroy()

# Crear el botón de inicio
startButton = tk.Button(window, text="Start Simulation", command=simulation)
startButton.grid(row=0, column=1)

# Ejecutar la ventana
window.protocol("WM_DELETE_WINDOW", close)
window.mainloop()
