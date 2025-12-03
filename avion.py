import random  # Librería estándar para generar números pseudoaleatorios (necesaria para la simulación de coordenadas).

class Avion:
    """
    Clase que representa un punto en el plano 2D (el avión).
    Complejidad espacial: O(1) por objeto, ya que solo guarda 3 atributos escalares.
    """
    def __init__(self, id_avion, x, y):
        # Constructor: Inicializa el estado del objeto.
        # Recibe un ID único y las coordenadas cartesianas (x, y).
        # Complejidad temporal: O(1).
        self.id = id_avion
        self.x = x
        self.y = y

    def __repr__(self):
        # Método mágico para representación de cadena.
        # Permite ver los valores reales del objeto al imprimir listas o depurar,
        # en lugar de ver la dirección de memoria. Formatea a 2 decimales para legibilidad.
        return f"Avion({self.id}, x={self.x:.2f}, y={self.y:.2f})"

    @staticmethod
    def generar_aleatorios(n, rango=800):
        """
        Genera un conjunto de datos de prueba (Dataset).
        
        Parámetros:
        - n: Cantidad de aviones (tamaño del problema N).
        - rango: Límite del plano cartesiano (el canvas de la interfaz).
        
        Funcionamiento:
        - Usa 'random.uniform' para obtener flotantes (precisión decimal),
          simulando posiciones reales en un radar continuo, no discreto.
        - Utiliza una 'list comprehension' (comprensión de lista) de Python
          para crear la lista de forma optimizada en una sola línea.
        
        Complejidad temporal: O(n), ya que debe iterar n veces para crear n objetos.
        """
        return [Avion(i, random.uniform(0, rango), random.uniform(0, rango)) for i in range(n)]