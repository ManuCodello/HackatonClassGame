# Sistema de mapas
# class Mapa:
# def init(self, nombre, grid, npcs, items):
# self.nombre = nombre
# self.grid = grid # Matriz 2D
# self.npcs = npcs
# self.items = items
# self.conexiones = {} # Mapas conectados

## Prueba 1: Estructura basica del mapa, lograr que se vea.
### Por decision del team lead, el mapa sera 30x30

class Mapa:
    def __init__(self, nombre_mapa):
        self.nombre = nombre_mapa
        self.grid = [['.' for _ in range(30)] for _ in range(30)]
        self.npcs = []
        self.items = []
        self.conexiones_mapas = {1: '2do Mapa', 2: '3er Mapa', 3:'4to Mapa', 4:'Fin'}

    def mostrar(self):
        for x in self.grid:
            print(' '.join(x))
        print()

mapa1 = Mapa('Inicio')
mapa1.mostrar()