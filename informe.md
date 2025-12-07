# Informe Técnico: Sistema de Detección de Posibles Colisiones Aéreas

## Proyecto Final - Análisis y Diseño de Algoritmos I
**Ing. Mateo Echeverry Correa**  
**Periodo: 2025-II**

---

## 1. Planteamiento Teórico del Problema

### 1.1 Descripción Formal del Problema

El problema central consiste en **identificar el par o los pares de aeronaves más cercanos entre sí** dentro de un espacio aéreo bidimensional, con el fin de prevenir posibles colisiones.

**Formulación matemática:**

Dado un conjunto **P** de **n** puntos en el plano cartesiano ℝ², donde cada punto representa una aeronave con coordenadas **(xᵢ, yᵢ)**:

```
P = {p₁, p₂, p₃, ..., pₙ} donde pᵢ = (xᵢ, yᵢ)
```

Se busca encontrar el par de puntos **(pᵢ, pⱼ)** tal que:

```
d(pᵢ, pⱼ) = min{ d(pₐ, pᵦ) | a ≠ b, 1 ≤ a,b ≤ n }
```

Donde la distancia euclidiana entre dos puntos se define como:

```
d(pᵢ, pⱼ) = √[(xᵢ - xⱼ)² + (yᵢ - yⱼ)²]
```

**Restricciones adicionales:**
- El sistema debe considerar un **umbral de distancia crítica** (δ), reportando todos los pares cuya distancia sea **d(pᵢ, pⱼ) ≤ δ**.
- La solución debe ser eficiente para conjuntos grandes de datos (n > 1000).
- Se requiere procesamiento en tiempo cuasi-real para aplicaciones prácticas.

### 1.2 Contexto del Problema

Este problema es una variante del clásico **"Closest Pair of Points Problem"**, un problema fundamental en geometría computacional con aplicaciones directas en:

- Sistemas de control de tráfico aéreo (ATC)
- Detección de colisiones en videojuegos y simulaciones físicas
- Agrupamiento de datos en machine learning (clustering)
- Diseño de circuitos VLSI (Very Large Scale Integration)

---

## 2. Justificación del Enfoque "Dividir y Vencer"

### 2.1 ¿Por qué NO usar Fuerza Bruta?

La solución trivial consiste en comparar cada par de puntos:

```python
def fuerza_bruta(puntos):
    n = len(puntos)
    min_dist = float('inf')
    for i in range(n):
        for j in range(i+1, n):
            d = distancia(puntos[i], puntos[j])
            if d < min_dist:
                min_dist = d
```

**Complejidad:** **O(n²)**

**Problema:** Para n = 5000 aviones → **12,497,500 comparaciones**. Inviable para tiempo real.

### 2.2 Ventajas del Paradigma "Dividir y Vencer"

El enfoque **Divide and Conquer** reduce drásticamente el número de comparaciones necesarias mediante:

1. **División espacial:** Particionar el conjunto de puntos en subconjuntos más pequeños.
2. **Resolución recursiva:** Resolver el problema en cada subconjunto independientemente.
3. **Combinación inteligente:** Integrar resultados considerando puntos en la frontera entre particiones.

**Resultado:** Complejidad **O(n log n)**, equivalente a algoritmos de ordenamiento óptimos.

### 2.3 Estrategia Implementada

El algoritmo sigue la estructura clásica del problema del par más cercano:

```
1. CASO BASE: Si n ≤ 3 → Comparar todos los pares (fuerza bruta local)
2. DIVIDIR: Separar los puntos en dos mitades (izquierda y derecha) por coordenada X
3. CONQUISTAR: Resolver recursivamente ambas mitades
4. COMBINAR: 
   a) Determinar la distancia mínima δ entre ambas mitades
   b) Construir una "banda" de puntos a distancia < δ de la línea divisoria
   c) Buscar pares en la banda (optimización: solo revisar 7 vecinos por punto)
```

**Fundamento geométrico clave:** Por propiedades de empaquetamiento en el plano, solo es necesario revisar un número constante de vecinos en la banda, manteniendo la complejidad logarítmica.

---

## 3. Análisis de Complejidad

### 3.1 Complejidad Temporal

#### Análisis por fases:

**a) Pre-procesamiento (ordenamiento inicial):**
```python
puntos_ordenados = ordenar_por_x(self.aviones)
```
- **Complejidad:** **O(n log n)**
- Se ejecuta una sola vez antes de la recursión.

**b) Función recursiva `_par_mas_cercano(puntos)`:**

La relación de recurrencia es:

```
T(n) = 2·T(n/2) + O(n)
```

Donde:
- **2·T(n/2):** Dos llamadas recursivas con mitad de datos cada una
- **O(n):** Trabajo lineal en la fase de combinación (construcción de banda + búsqueda)

**Aplicando el Teorema Maestro:**

Para recurrencias de la forma **T(n) = a·T(n/b) + f(n)**:

- a = 2 (dos subproblemas)
- b = 2 (tamaño dividido a la mitad)
- f(n) = O(n) (trabajo de combinación)

Comparación: **log₂(2) = 1** y **f(n) = Θ(n¹)**

**Caso 2 del Teorema:** f(n) = Θ(n^(log_b(a))) → **T(n) = Θ(n log n)**

**c) Post-procesamiento (filtrado y deduplicación):**
```python
pares_riesgo.sort(key=lambda x: x[2])  # Ordenamiento por distancia
```
- En el peor caso, todos los pares están bajo el umbral
- **Complejidad:** **O(k log k)** donde k ≤ n-1 (máximo número de pares cercanos)

#### Complejidad Total del Sistema:

```
T_total(n) = O(n log n) + O(n log n) + O(k log k)
           = O(n log n)  [domina el término]
```

**Conclusión:** El algoritmo tiene complejidad temporal **O(n log n)** en todos los casos (mejor, promedio y peor).

### 3.2 Complejidad Espacial

#### Análisis de memoria:

**a) Almacenamiento de datos de entrada:**
```python
self.aviones = aviones  # Lista de n objetos Avion
```
- **O(n)** para almacenar las aeronaves originales.

**b) Pila de recursión:**
- Profundidad máxima del árbol de recursión: **log₂(n)**
- En cada nivel se mantienen referencias a sublistas
- **O(log n)** espacio en la pila de llamadas

**c) Estructuras auxiliares:**
```python
banda = [p for p in puntos if abs(p.x - mid_x) < mejor_dist]
```
- En el peor caso, todos los puntos caen en la banda: **O(n)**
- Listas temporales `mejores`, `pares_izq`, `pares_der`: **O(n)** en total

**d) Listas de resultados:**
```python
pares_unicos = []  # Hasta O(n) pares en caso extremo
```

#### Complejidad Espacial Total:

```
S_total(n) = O(n) + O(log n) + O(n) + O(n)
           = O(n)  [términos lineales dominan]
```

**Conclusión:** El algoritmo requiere espacio auxiliar **O(n)**, con espacio de pila **O(log n)**.

---

## 4. Estructura Modular del Código

### 4.1 Arquitectura del Sistema

El proyecto sigue el patrón **MVC (Modelo-Vista-Controlador)** adaptado:

```
┌─────────────────────────────────────────┐
│         main.py (Punto de entrada)      │
└─────────────────────────────────────────┘
                    │
        ┌───────────┴───────────┐
        ▼                       ▼
┌───────────────┐       ┌──────────────────┐
│  MODELO       │       │  VISTA           │
│  - avion.py   │◄──────┤  - interfaz.py   │
│  - detector_  │       │  (InterfazRadar) │
│    colisiones │       └──────────────────┘
│    .py        │
│  - utils.py   │
└───────────────┘
```

### 4.2 Descripción de Módulos

#### **1. avion.py (Modelo de datos)**
```python
class Avion:
    def __init__(self, id_avion, x, y)
    @staticmethod
    def generar_aleatorios(n, rango=800)
```
- **Responsabilidad:** Representar puntos en el plano cartesiano.
- **Patrón de diseño:** Data class + Factory method (método estático generador).

#### **2. utils.py (Funciones auxiliares)**
```python
def distancia(a, b) -> float
def ordenar_por_x(puntos) -> List[Avion]
def ordenar_por_y(puntos) -> List[Avion]
```
- **Responsabilidad:** Operaciones matemáticas y de ordenamiento reutilizables.
- **Principio SOLID:** Single Responsibility Principle (SRP).

#### **3. detector_colisiones.py (Lógica algorítmica)**
```python
class DetectorColisiones:
    def _par_mas_cercano(self, puntos)  # Método privado (core recursivo)
    def obtener_pares_bajo_umbral(self, umbral_distancia)  # API pública
```
- **Responsabilidad:** Implementación del algoritmo Divide y Vencer.
- **Patrón de diseño:** Template Method (método público delega a privado).
- **Encapsulamiento:** Método `_par_mas_cercano` privado (prefijo `_`), API pública clara.

#### **4. interfaz.py (Capa de presentación)**
```python
class InterfazRadar:
    def __init__(self, root)
    def ejecutar_analisis(self)
    def dibujar_resultados(self, w, h)
```
- **Responsabilidad:** Interacción con el usuario y visualización.
- **Tecnología:** Tkinter (GUI nativa de Python).
- **Características:**
  - Panel de control con sliders para parámetros dinámicos
  - Canvas tipo radar con sistema de coordenadas centradas
  - Lista scrollable de alertas en tiempo real

#### **5. main.py (Punto de entrada)**
```python
if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazRadar(root)
    root.mainloop()
```
- **Responsabilidad:** Inicialización de la aplicación.

---

## 5. Detalles de Implementación Clave

### 5.1 Optimización Geométrica en la Banda

**Propiedad fundamental:** En la banda de ancho 2δ, solo es necesario revisar **7 vecinos** por punto:

```python
for i in range(len(banda)):
    for j in range(i + 1, min(i + 7, len(banda))):
        d = distancia(banda[i], banda[j])
```

**Justificación matemática:**
- Si dos puntos están a distancia < δ, y la banda tiene ancho 2δ, ambos puntos deben estar en celdas adyacentes de una cuadrícula de δ × δ.
- Por el principio del palomar, en una cuadrícula δ × δ solo pueden caber puntos en configuraciones geométricas limitadas.
- Revisando 7 vecinos (en orden Y) se garantiza cubrir todas las posibilidades.

### 5.2 Manejo de Duplicados

El algoritmo recursivo puede reportar el mismo par múltiples veces:

```python
vistos = set()
for a1, a2, d in pares_riesgo:
    pair_id = tuple(sorted((a1.id, a2.id)))
    if pair_id not in vistos:
        pares_unicos.append((a1, a2, d))
        vistos.add(pair_id)
```

**Estrategia:** Usar tuplas ordenadas como "firma única" para cada par, almacenadas en un conjunto (hash set) para verificación O(1).

### 5.3 Interfaz Visual: Sistema de Coordenadas

El canvas usa coordenadas centradas para simular un radar:

```python
center_offset_x = (w - (min(w,h)-50)) / 2
center_offset_y = (h - (min(w,h)-50)) / 2
```

Los aviones se generan en un rango [0, rango], pero se dibujan con offset para centrarlos visualmente.

---

## 6. Pruebas y Validación

### 6.1 Casos de Prueba Recomendados

| **Caso**              | **n** | **Umbral** | **Resultado Esperado**                     |
|-----------------------|-------|------------|--------------------------------------------|
| Mínimo                | 2     | 100        | 1 par detectado (única combinación)        |
| Pequeño               | 10    | 50         | Pocos pares, visualización clara           |
| Medio                 | 100   | 80         | Rendimiento fluido, múltiples alertas      |
| Grande                | 1000  | 30         | Algoritmo eficiente, sin lag               |
| Extremo               | 5000  | 50         | Stress test, validación O(n log n)         |
| Sin colisiones        | 50    | 5          | 0 alertas (puntos muy dispersos)           |
| Todas son colisiones  | 20    | 800        | Todas las combinaciones bajo umbral        |

### 6.2 Manejo de Casos Borde

```python
if len(self.aviones) < 2:
    return []  # No se pueden formar pares
```

```python
if n <= 3:
    # Caso base: fuerza bruta local
    pares = [(puntos[i], puntos[j], distancia(puntos[i], puntos[j]))
             for i in range(n) for j in range(i + 1, n)]
    return sorted(pares, key=lambda x: x[2])
```

---

## 7. Conclusiones

### 7.1 Logros del Proyecto

1. **Eficiencia algorítmica:** Implementación correcta de Divide y Vencer con complejidad **O(n log n)**.
2. **Modularidad:** Código bien estructurado siguiendo principios SOLID y patrones de diseño.
3. **Usabilidad:** Interfaz gráfica intuitiva con controles dinámicos y visualización tipo radar.
4. **Escalabilidad:** Capaz de procesar miles de aeronaves en tiempo razonable.

### 7.2 Aplicaciones Reales

Este sistema puede extenderse para:
- **Integración con APIs de tráfico aéreo real** (FlightRadar24, ADS-B).
- **Simulaciones 3D** agregando coordenada Z (altitud).
- **Predicción de trayectorias** usando vectores de velocidad.
- **Sistemas de alerta temprana** con comunicación a torres de control.

### 7.3 Trabajo Futuro

Posibles mejoras:
- Implementar **estructuras de datos espaciales** (K-D Trees, Quadtrees) para consultas dinámicas.
- Agregar **seguimiento temporal** (múltiples frames) para detectar tendencias de acercamiento.
- Optimizar con **paralelización** (multithreading) para datasets masivos.
- Exportar reportes en formatos estándar (JSON, CSV, PDF).

---

## 8. Referencias Técnicas

1. **Cormen, T. H., et al.** (2009). *Introduction to Algorithms* (3rd ed.). MIT Press.
   - Capítulo 33: Geometría Computacional.

2. **Preparata, F. P., & Shamos, M. I.** (1985). *Computational Geometry: An Introduction*. Springer.
   - Algoritmo del par más cercano (páginas 192-203).

3. **Sedgewick, R., & Wayne, K.** (2011). *Algorithms* (4th ed.). Addison-Wesley.
   - Sección sobre Divide y Vencer.

4. **Documentación oficial de Python:**
   - Tkinter: https://docs.python.org/3/library/tkinter.html
   - Math: https://docs.python.org/3/library/math.html

---

## Anexos

### A. Requisitos del Sistema

```
Python >= 3.8
Librerías:
  - tkinter (incluida en Python estándar)
  - PIL (Pillow) >= 8.0
  - math (librería estándar)
  - random (librería estándar)
```

### B. Instrucciones de Ejecución

```bash
# 1. Clonar o descomprimir el proyecto
cd proyecto_colisiones_aereas/

# 2. Instalar dependencias (solo Pillow requiere instalación)
pip install Pillow

# 3. Ejecutar el programa
python main.py

# 4. Uso:
#    - Ajustar cantidad de aviones (2-5000)
#    - Ajustar umbral de riesgo con slider
#    - Presionar "ANALIZAR ESPACIO AÉREO"
#    - Observar visualización y alertas
```

### C. Estructura de Archivos

```
proyecto_colisiones_aereas/
│
├── main.py                    # Punto de entrada
├── avion.py                   # Clase Avion (modelo)
├── detector_colisiones.py     # Algoritmo Divide y Vencer
├── utils.py                   # Funciones auxiliares
├── interfaz.py                # GUI con Tkinter
├── avion.png                  # Ícono de avión (opcional)
└── README.md                  # Documentación de usuario
```

---

**Fecha de elaboración:** Diciembre 2025  
**Lenguaje de implementación:** Python 3.x  
**Paradigma algorítmico:** Dividir y Vencer (Divide and Conquer)  
**Complejidad temporal:** O(n log n)  
**Complejidad espacial:** O(n)