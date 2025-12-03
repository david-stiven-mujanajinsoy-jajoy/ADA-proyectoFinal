import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from avion import Avion
from detector_colisiones import DetectorColisiones
import os

class InterfazRadar:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Análisis de Tráfico Aéreo")
        self.root.geometry("1100x700")
        
        # Configuración de estilo
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.bg_color = "#1e272e" # Color de fondo oscuro para panel
        self.canvas_bg = "#0c2461" # Azul oscuro tipo radar
        self.text_color = "#d2dae2"
        
        root.configure(bg=self.bg_color)

        # --- Variables de Control ---
        self.num_aviones_var = tk.IntVar(value=20) 
        self.umbral_var = tk.DoubleVar(value=50.0) 

        # --- CARGA DE IMAGEN (CORREGIDA Y ÚNICA) ---
        # 1. Obtiene la ruta de la carpeta donde está ESTE archivo script
        ruta_script = os.path.dirname(os.path.abspath(__file__))
        
        # 2. Une esa ruta con el nombre de la imagen
        ruta_imagen = os.path.join(ruta_script, "avion.png")

        self.usar_imagen = False # Por defecto falso hasta que cargue bien
        self.avion_img = None

        try:
            self.icono_avion_orig = Image.open(ruta_imagen).resize((24, 24))
            self.avion_img = ImageTk.PhotoImage(self.icono_avion_orig)
            self.usar_imagen = True
        except FileNotFoundError:
            # Si falla, solo imprimimos aviso y usaremos círculos después
            print(f"AVISO: No se encontró la imagen en: {ruta_imagen}. Se usarán círculos.")
            self.usar_imagen = False

        
        # 1. Panel de Control (Izquierda)
        self.panel_control = tk.Frame(root, width=300, bg=self.bg_color, padx=15, pady=15)
        self.panel_control.pack(side=tk.LEFT, fill=tk.Y)
        self.panel_control.pack_propagate(False)

        # Título del panel
        tk.Label(self.panel_control, text="Panel de Control", font=("Arial", 14, "bold"), 
                 bg=self.bg_color, fg="white").pack(pady=(0, 20))

        # --- Controles de Parámetros ---
        
        # Input: Cantidad de Aviones
        tk.Label(self.panel_control, text="Cantidad de Aviones (N):", bg=self.bg_color, fg=self.text_color).pack(anchor="w")
        self.entry_n = ttk.Entry(self.panel_control, textvariable=self.num_aviones_var)
        self.entry_n.pack(fill=tk.X, pady=(5, 15))

        # Input: Umbral de Distancia (Slider)
        tk.Label(self.panel_control, text="Umbral de Riesgo (Distancia):", bg=self.bg_color, fg=self.text_color).pack(anchor="w")
        
        self.label_umbral_valor = tk.Label(self.panel_control, text=f"{self.umbral_var.get():.1f} px", 
                                           bg=self.bg_color, fg="#ffdd59", font=("Arial", 10, "bold"))
        self.label_umbral_valor.pack(anchor="e")

        self.scale_umbral = ttk.Scale(self.panel_control, from_=3.0, to=200.0, 
                                      variable=self.umbral_var, command=self.actualizar_label_umbral)
        self.scale_umbral.pack(fill=tk.X, pady=(0, 20))


        # Botón Generar
        self.btn_generar = tk.Button(self.panel_control, text="ANALIZAR ESPACIO AÉREO", 
                                     bg="#00d2d3", fg="black", font=("Arial", 10, "bold"),
                                     command=self.ejecutar_analisis)
        self.btn_generar.pack(fill=tk.X, pady=10, ipady=5)

        # Área de Resultados (Lista con scroll)
        tk.Label(self.panel_control, text="Alertas de Colisión:", bg=self.bg_color, fg="white", font=("Arial", 11, "bold")).pack(anchor="w", pady=(20, 5))
        
        frame_lista = tk.Frame(self.panel_control, bg=self.bg_color)
        frame_lista.pack(fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(frame_lista)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.lista_resultados = tk.Text(frame_lista, height=15, width=30, 
                                        yscrollcommand=scrollbar.set, bg="#34495e", fg="#ecf0f1", font=("Consolas", 9))
        self.lista_resultados.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar.config(command=self.lista_resultados.yview)


        # 2. Canvas del Radar (Derecha)
        self.canvas_frame = tk.Frame(root, bg="black")
        self.canvas_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.canvas_size = 800
        self.canvas = tk.Canvas(self.canvas_frame, bg=self.canvas_bg, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.canvas.bind("<Configure>", self.dibujar_cuadricula)

        self.aviones_actuales = []
        self.pares_riesgo_actuales = []

    def actualizar_label_umbral(self, event=None):
        self.label_umbral_valor.config(text=f"{self.umbral_var.get():.1f} px")

    def dibujar_cuadricula(self, event=None):
        self.canvas.delete("grid")
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        center_x, center_y = w // 2, h // 2
        
        for r in range(50, max(w, h)//2, 100):
            self.canvas.create_oval(center_x-r, center_y-r, center_x+r, center_y+r, 
                                    outline="#4b6584", tags="grid", dash=(2, 4))
        self.canvas.create_line(0, center_y, w, center_y, fill="#4b6584", tags="grid")
        self.canvas.create_line(center_x, 0, center_x, h, fill="#4b6584", tags="grid")


    def validar_inputs(self):
        try:
            n = self.num_aviones_var.get()
            if n < 2 or n > 5000:
                raise ValueError("El número de aviones debe estar entre 2 y 5000.")
            return n
        except tk.TclError:
             messagebox.showerror("Error de Validación", "Por favor ingrese un número entero válido.")
             return None
        except ValueError as e:
             messagebox.showerror("Error de Validación", str(e))
             return None

    def ejecutar_analisis(self):
        n = self.validar_inputs()
        if n is None: return
        
        umbral = self.umbral_var.get()

        self.canvas.delete("all")
        self.dibujar_cuadricula()
        self.lista_resultados.delete(1.0, tk.END)
        self.btn_generar.config(text="Procesando...", state=tk.DISABLED)
        self.root.update()

        w_real = self.canvas.winfo_width()
        h_real = self.canvas.winfo_height()
        rango_generacion = min(w_real, h_real) - 50 

        self.aviones_actuales = Avion.generar_aleatorios(n, rango=rango_generacion)
        
        detector = DetectorColisiones(self.aviones_actuales)
        self.pares_riesgo_actuales = detector.obtener_pares_bajo_umbral(umbral_distancia=umbral)

        self.dibujar_resultados(w_real, h_real)
        self.btn_generar.config(text="ANALIZAR ESPACIO AÉREO", state=tk.NORMAL)


    def dibujar_resultados(self, w, h):
        center_offset_x = (w - (min(w,h)-50)) / 2
        center_offset_y = (h - (min(w,h)-50)) / 2

        count_alertas = 0
        resultados_texto = ""
        
        # 1. Dibujar líneas de riesgo
        for i, (a1, a2, d) in enumerate(self.pares_riesgo_actuales):
            count_alertas += 1
            grosor = max(1, int(5 - (d / self.umbral_var.get()) * 4))
            color_linea = "#ff3838" if d < self.umbral_var.get()/2 else "#ff9f43"
            
            self.canvas.create_line(a1.x + center_offset_x, a1.y + center_offset_y, 
                                    a2.x + center_offset_x, a2.y + center_offset_y, 
                                    fill=color_linea, width=grosor, tags="riesgo")
            
            resultados_texto += f"ALERTA {i+1}: ID {a1.id} ↔ ID {a2.id}\n   Distancia: {d:.2f} px\n\n"

        # 2. Dibujar aviones (Con protección si no hay imagen)
        for avion in self.aviones_actuales:
            x_final = avion.x + center_offset_x
            y_final = avion.y + center_offset_y
            
            if self.usar_imagen and self.avion_img:
                # Si la imagen cargó bien
                self.canvas.create_image(x_final, y_final, 
                                         image=self.avion_img, anchor=tk.CENTER, tags="avion")
            else:
                # Si NO hay imagen, dibujamos un círculo cyan
                r = 5
                self.canvas.create_oval(x_final-r, y_final-r, x_final+r, y_final+r,
                                        fill="#00d2d3", outline="white", tags="avion")
            
            self.canvas.create_text(x_final + 15, y_final,
                                    text=f"id:{avion.id}", fill="#7f8c8d", font=("Arial", 8))

        summary = f"--- RESUMEN ---\nAviones totales: {len(self.aviones_actuales)}\nUmbral actual: {self.umbral_var.get():.1f} px\nAlertas detectadas: {count_alertas}\n{'-'*20}\n"
        self.lista_resultados.insert(tk.END, summary + resultados_texto)

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazRadar(root)
    root.mainloop()