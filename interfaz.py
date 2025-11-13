import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from avion import Avion
from detector_colisiones import DetectorColisiones
from tkinter import messagebox

class InterfazRadar:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualizer de Posibles Colisiones Aéreas")

        self.canvas_size = 800
        self.canvas = tk.Canvas(root, width=self.canvas_size, height=self.canvas_size, bg="#4da6ff")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.frame_botones = ttk.Frame(root)
        self.frame_botones.pack(pady=5)

        self.btn_generar = ttk.Button(self.frame_botones, text="Generar Aviones", command=self.generar)
        self.btn_generar.pack(side=tk.LEFT, padx=5)

        self.label_info = ttk.Label(self.frame_botones, text="Scale factor=1.0   num_pares=100")
        self.label_info.pack(side=tk.LEFT, padx=10)

        self.icono_avion = Image.open("avion.png").resize((32, 32))
        self.avion_img = ImageTk.PhotoImage(self.icono_avion)

        self.generar()

    def generar(self):
        self.canvas.delete("all")
        n = 500  # número de aviones
        aviones = Avion.generar_aleatorios(n, rango=self.canvas_size)
        detector = DetectorColisiones(aviones)
        pares = detector.obtener_pares_mas_cercanos(100)

        # Dibuja los aviones
        for avion in aviones:
            self.canvas.create_image(avion.x, avion.y, image=self.avion_img, anchor=tk.CENTER)

        # Dibuja las líneas rojas entre pares cercanos
        for (a1, a2, d) in pares:
            self.canvas.create_line(a1.x, a1.y, a2.x, a2.y, fill="red", width=1)

        # Mostrar los 5 primeros pares en una ventana emergente
        texto = "Pares más cercanos:\n\n"
        for i, (a1, a2, d) in enumerate(pares[:5]):
            texto += f"{i+1}. Avión {a1.id} ↔ Avión {a2.id} → Distancia = {d:.2f}\n"
        messagebox.showinfo("Pares más cercanos", texto)