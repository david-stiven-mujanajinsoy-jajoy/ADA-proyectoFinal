from utils import distancia, ordenar_por_x, ordenar_por_y

class DetectorColisiones:
    def __init__(self, aviones):
        self.aviones = aviones

    def _par_mas_cercano(self, puntos):
        n = len(puntos)
        if n <= 3:
            pares = [(puntos[i], puntos[j], distancia(puntos[i], puntos[j]))
                     for i in range(n) for j in range(i + 1, n)]
            return sorted(pares, key=lambda x: x[2])

        mid = n // 2
        mitad_izq = puntos[:mid]
        mitad_der = puntos[mid:]

        pares_izq = self._par_mas_cercano(mitad_izq)
        pares_der = self._par_mas_cercano(mitad_der)

        mejor_dist = min(pares_izq[0][2], pares_der[0][2])
        mejores = pares_izq + pares_der

        mid_x = puntos[mid].x
        banda = [p for p in puntos if abs(p.x - mid_x) < mejor_dist]
        banda = ordenar_por_y(banda)

        for i in range(len(banda)):
            for j in range(i + 1, min(i + 7, len(banda))):
                d = distancia(banda[i], banda[j])
                mejores.append((banda[i], banda[j], d))

        return sorted(mejores, key=lambda x: x[2])

    def obtener_pares_mas_cercanos(self, cantidad=100):
        puntos_ordenados = ordenar_por_x(self.aviones)
        pares = self._par_mas_cercano(puntos_ordenados)
        return pares[:cantidad]
