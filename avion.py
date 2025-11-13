import random

class Avion:
    def __init__(self, id_avion, x, y):
        self.id = id_avion
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Avion({self.id}, x={self.x:.2f}, y={self.y:.2f})"

    @staticmethod
    def generar_aleatorios(n, rango=800):
        """Genera n aviones con coordenadas aleatorias"""
        return [Avion(i, random.uniform(0, rango), random.uniform(0, rango)) for i in range(n)]
