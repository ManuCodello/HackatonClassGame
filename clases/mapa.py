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

## Variables globales - Configuracion del Juego
ANCHO_CONSOLA = 80
ALTO_CONSOLA = 24
ANCHO_MAPA = 30
ALTO_MAPA = 30
FPS = 60

# MAPAS DISPONIBLES (IDs)
MAPA_BUNKER = 'bunker_paraguay'
MAPA_RUINAS = 'ruinas_asuncion'
MAPA_BASE_SOVIETICA = 'base_sovietica'
MAPA_TIERRA_NADIE = 'tierra_nadie'
MAPA_REACTOR = 'reactor_nuclear'

MAPAS_ORDEN = [MAPA_BUNKER, MAPA_RUINAS, MAPA_BASE_SOVIETICA, MAPA_TIERRA_NADIE, MAPA_REACTOR]

# Estado del mapa actual
mapa_actual_id = MAPA_BUNKER
mapa_actual_grid = []  # Se llena desde mapas_data.py
mapa_ancho = ANCHO_MAPA
mapa_alto = ALTO_MAPA

import random

class Mapa ():
#PUEDE MODIFICAR:

    '''
    g.mapa_actual_id
    g.mapa_actual_grid
    g.mapa_ancho, g.mapa_alto
    '''

# CLASE Mapa:
#     MÉTODO __init__(nombre, grid, lista_npcs, lista_items):
#         guardar nombre del mapa
#         guardar la matriz del mapa (grid 2D con símbolos)
#         guardar lista de NPCs
#         guardar lista de items
#         inicializar conexiones a otros mapas (diccionario)
class Mapa:
    def __init__(self, id_mapa, tipo = 'base'):
        self.nombre = id_mapa
        self.grid = [['⬜' for _ in range(30)] for _ in range(30)]
        self.npcs = []
        self.items = []
        self.jugador_pos = (1,6)
        self.conexiones_mapas = {}   # Portales
        self.tipo = tipo  # 'base', 'ciudad', 'laberinto'
        self.portal_visible = tipo == 'base'  # Solo se ve en el mapa base
        self.generar_mapa()

#     MÉTODO mostrar():
#         recorrer la matriz y mostrarla (consola o visual)
#         puede incluir íconos de jugador, NPCs, ítems
    def mostrar(self):
        for x in self.grid:
            print(' '.join(x))

#     MÉTODO es_posicion_valida(x, y):
#         devolver TRUE si:
#             - las coordenadas están dentro de los límites
#             - la casilla no es un obstáculo
#         si no, devolver FALSE
    def es_posicion_valida(self, x, y):
        return 0 <= x < ALTO_MAPA and 0 <= y < ANCHO_MAPA and self.grid[x][y] != '🚧'

#     METODO Inicializar mapas
    def generar_mapa(self):
        for i in range(ANCHO_MAPA):
            self.grid[i][0] = '🚧'
            self.grid[i][ANCHO_MAPA-1] = '🚧'

        for i in range(30):
            self.grid[0] [i] = '🚧'
            self.grid[ALTO_MAPA-1] [i] = '🚧'

        # logica de generación según tipo de mapa
        if self.tipo == 'base':
            self.generar_calles()
            self.colocar_jugador()
            self.colocar_portal()
        elif self.tipo == 'ciudad':
            self.generar_calles()
            self.colocar_jugador()
            self.colocar_portal()
            self.colocar_npc()
        elif self.tipo == 'laberinto':
            self.generar_laberinto()

    ## 
    def colocar_portal(self):
    # Limpiar portal previo si existe
        for i in range(1, ALTO_MAPA - 1):
            for j in range(1, ANCHO_MAPA - 1):
                if self.grid[i][j] == '🌀':
                    self.grid[i][j] = '⬛'
        
        # Buscar la última celda negra desde el final (de abajo hacia arriba, derecha a izquierda)
        for i in range(ALTO_MAPA - 2, 0, -1):
            for j in range(ANCHO_MAPA - 2, 0, -1):
                if self.grid[i][j] == '⬛':
                    self.grid[i][j] = '🌀'
                    self.conexiones_mapas['siguiente'] = f"mapa_{int(self.nombre[-1]) + 1}"
                    return


    def colocar_npc(self):
        # NPC en una posición aleatoria que no sea muro ni jugador
        while True:
            x = random.randint(5, ALTO_MAPA-5)
            y = random.randint(5, ANCHO_MAPA-5)
            if self.grid[x][y] == '⬛':
                self.grid[x][y] = '🤖'
                self.npcs.append({'pos': (x, y), 'vencido': False})
                break

    def generar_calles(self):
        # Dibuja un par de calles horizontales y verticales aleatorias
        for _ in range(5):
            fila = random.randint(3, ALTO_MAPA-4)
            for col in range(1, ANCHO_MAPA-1):
                self.grid[fila][col] = '⬛'

        for _ in range(5):
            col = random.randint(3, ANCHO_MAPA-4)
            for fila in range(1, ALTO_MAPA-1):
                self.grid[fila][col] = '⬛'
    
    def mostrar_portal_si_npc_vencido(self):
        # Mostrar portal solo si el NPC ha sido vencido
        if any(npc['vencido'] for npc in self.npcs):
            self.colocar_portal(ALTO_MAPA-2, ANCHO_MAPA-2)


    def generar_laberinto(self):
        # Inicializar todo el mapa como paredes
        self.grid = [['🚧' for _ in range(ANCHO_MAPA)] for _ in range(ALTO_MAPA)]

        # Crear camino fijo garantizado desde (1,1) hasta (ALTO-2, ANCHO-2)
        x, y = 1, 1
        self.grid[x][y] = '⬛'
        # Paso horizontal hacia la derecha
        while y < ANCHO_MAPA - 2:
            y += 1
            self.grid[x][y] = '⬛'

        # Paso vertical hacia abajo
        while x < ALTO_MAPA - 2:
            x += 1
            self.grid[x][y] = '⬛'

        self.grid[x][y] = '🌀'  # Salida
        self.grid[1][1] = '🧍'


        # Agregar obstáculos al azar en las otras celdas que no formen parte del camino
        for i in range(1, ALTO_MAPA - 1):
            for j in range(1, ANCHO_MAPA - 1):
                if self.grid[i][j] == '⬛' or self.grid[i][j] in ['🧍', '🌀']:
                    continue  # No tocar el camino
                if random.random() < 0.2:
                    self.grid[i][j] = '🚧'
                else:
                    self.grid[i][j] = '⬛'

    def colocar_jugador(self):
        # Limpiar jugador previo si existe
        for i in range(1, ALTO_MAPA - 1):
            for j in range(1, ANCHO_MAPA - 1):
                if self.grid[i][j] == '🧍':
                    self.grid[i][j] = '⬛'
    # Intenta poner el jugador en una celda negra libre
        for i in range(1, ALTO_MAPA - 1):
            for j in range(1, ANCHO_MAPA - 1):
                if self.grid[i][j] == '⬛':
                    self.jugador_pos = (i, j)
                    self.grid[i][j] = '🧍'
                    return
                
mapa = Mapa('mapa_1', tipo='base')
mapa.generar_mapa()
mapa.mostrar()
print()
mapa2 = Mapa('mapa_2', tipo='ciudad')
mapa2.generar_mapa()
mapa2.mostrar()
print()
mapa3 = Mapa('mapa_3', tipo='ciudad')
mapa3.generar_mapa()
mapa3.mostrar()
print()
mapa4 = Mapa('mapa_4', tipo='ciudad')
mapa4.generar_mapa()
mapa4.mostrar()
print()
mapa5 = Mapa('mapa_5', tipo='laberinto')
mapa5.generar_mapa()
mapa5.mostrar()
print()

# mapas = [
#     Mapa('mapa_1', tipo='base'),
#     Mapa('mapa_2', tipo='ciudad'),
#     Mapa('mapa_3', tipo='ciudad'),
#     Mapa('mapa_4', tipo='ciudad'),
#     Mapa('mapa_5', tipo='laberinto')
# ]


# Mostrar todos los mapas
# for mapa in mapas:
#     print(f"\n===== {mapa.nombre.upper()} ({mapa.tipo}) =====")
#     mapa.mostrar()

#mapa.inicializar_mapas()












