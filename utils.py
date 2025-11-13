import math

def distancia(a, b):
    return math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)

def ordenar_por_x(puntos):
    return sorted(puntos, key=lambda p: p.x)

def ordenar_por_y(puntos):
    return sorted(puntos, key=lambda p: p.y)
