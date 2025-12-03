from utils import distancia, ordenar_por_x, ordenar_por_y

class DetectorColisiones:
    def __init__(self, aviones):
        # Almacenamos la referencia a la lista de aviones.
        self.aviones = aviones

    # --- Mantenemos _par_mas_cercano (Lógica Core) ---
    def _par_mas_cercano(self, puntos):
        """
        Implementación del algoritmo 'Divide y Vencerás'.
        Complejidad: O(n log n).
        Divide el conjunto de puntos recursivamente para reducir el número de comparaciones.
        """
        n = len(puntos)
        
        # 1. CASO BASE (Fuerza Bruta)
        # Si hay pocos puntos (<= 3), es más rápido compararlos todos contra todos
        # que seguir dividiendo. Complejidad local: O(1).
        if n <= 3:
            pares = [(puntos[i], puntos[j], distancia(puntos[i], puntos[j]))
                     for i in range(n) for j in range(i + 1, n)]
            return sorted(pares, key=lambda x: x[2])

        # 2. FASE DE DIVISIÓN (Divide)
        # Encontramos el punto medio para partir el plano en dos mitades (Izquierda/Derecha).
        mid = n // 2
        mitad_izq = puntos[:mid]
        mitad_der = puntos[mid:]

        # 3. LLAMADAS RECURSIVAS
        # Resolvemos el subproblema para cada mitad.
        pares_izq = self._par_mas_cercano(mitad_izq)
        pares_der = self._par_mas_cercano(mitad_der)

        # 4. FASE DE CONQUISTA/COMBINACIÓN (Conquer)
        # Determinamos cuál es la distancia mínima encontrada en los subgrupos (delta).
        # Esto nos sirve para limitar la búsqueda en la frontera.
        min_izq = pares_izq[0][2] if pares_izq else float('inf')
        min_der = pares_der[0][2] if pares_der else float('inf')
        mejor_dist = min(min_izq, min_der)
        
        # Juntamos los candidatos encontrados hasta ahora.
        mejores = pares_izq + pares_der

        # Creación de la "Banda" (Strip):
        # Solo nos importan los puntos que están muy cerca de la línea divisoria (mid_x).
        mid_x = puntos[mid].x
        banda = [p for p in puntos if abs(p.x - mid_x) < mejor_dist]
        
        # Ordenamos la banda por coordenada Y para la optimización geométrica.
        banda = ordenar_por_y(banda)

        # Búsqueda en la banda:
        # Propiedad geométrica clave: Solo es necesario comparar cada punto con los
        # siguientes 7 puntos en el orden Y. Esto mantiene la complejidad lineal en esta fase.
        for i in range(len(banda)):
            for j in range(i + 1, min(i + 7, len(banda))):
                d = distancia(banda[i], banda[j])
                mejores.append((banda[i], banda[j], d))

        # Retornamos los candidatos ordenados por distancia.
        return sorted(mejores, key=lambda x: x[2])

    # --- NUEVO MÉTODO PRINCIPAL (Interfaz pública) ---
    def obtener_pares_bajo_umbral(self, umbral_distancia):
        """
        Ejecuta el algoritmo y filtra para devolver solo los pares
        cuya distancia es menor al umbral especificado.
        Elimina duplicados (A-B vs B-A).
        """
        if len(self.aviones) < 2:
            return []

        # PRE-PROCESAMIENTO: Ordenar por X es obligatorio para el algoritmo Divide y Vencerás.
        # Complejidad: O(n log n).
        puntos_ordenados = ordenar_por_x(self.aviones)
        
        # Llamada inicial al algoritmo recursivo.
        todos_candidatos = self._par_mas_cercano(puntos_ordenados)

        # 1. FILTRADO (Lógica de Negocio)
        # Descartamos los pares que están lejos y no representan peligro.
        pares_riesgo = [(a1, a2, d) for (a1, a2, d) in todos_candidatos if d <= umbral_distancia]

        # 2. ORDENAMIENTO
        # Mostramos primero las colisiones inminentes (menor distancia).
        pares_riesgo.sort(key=lambda x: x[2])

        # 3. DEDUPLICACIÓN
        # El algoritmo recursivo puede reportar el mismo par dos veces o en orden inverso.
        # Usamos un Set y IDs ordenados para garantizar unicidad.
        pares_unicos = []
        vistos = set()
        for a1, a2, d in pares_riesgo:
            # Creamos una 'firma' única para el par, ej: (1, 2) es igual a (2, 1).
            pair_id = tuple(sorted((a1.id, a2.id)))
            if pair_id not in vistos:
                pares_unicos.append((a1, a2, d))
                vistos.add(pair_id)

        return pares_unicos