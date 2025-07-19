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
ANCHO_MAPA = 20
ALTO_MAPA = 15
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
    def __init__(self, id_mapa):
        self.nombre = id_mapa
        self.grid = [[' ' for _ in range(ANCHO_MAPA)] for _ in range(ALTO_MAPA)]
        self.npcs = []
        self.items = []
        self.conexiones_mapas = {1: '2do Mapa', 2: '3er Mapa', 3:'4to Mapa', 4:'Fin'}   # Portales

#     MÉTODO mostrar():
#         recorrer la matriz y mostrarla (consola o visual)
#         puede incluir íconos de jugador, NPCs, ítems
    def mostrar(self):
        for x in self.grid:
            for y in x:
                if y == 'J':
                    print('J', end=' ')
                elif y == 'N':  # NPC
                    print('N', end=' ')
                elif y == 'K':  # LLAVE
                    print('K', end=' ')
                elif y == 'X':
                    print('🚧', end=' ')
                else:
                    print('.', end=' ')
            print()


#     MÉTODO es_posicion_valida(x, y):
#         devolver TRUE si:
#             - las coordenadas están dentro de los límites
#             - la casilla no es un obstáculo
#         si no, devolver FALSE
    def es_posicion_valida(self, x, y):
        pass

#     MÉTODO colocar_objeto_en_grid(objeto, x, y):
#         modificar la matriz para reflejar la presencia de un NPC o ítem
    def colocar_objeto_en_grid(self, objeto, x, y):
        pass
    
#     MÉTODO obtener_npc_en(x, y):
#         recorrer la lista de NPCs
#         si alguno está en esa posición, devolverlo
#         si no, devolver None
    def obtener_npc_en(self, x, y):
        pass

#     MÉTODO agregar_conexion(direccion, mapa_destino):
#         en el diccionario de conexiones, agregar:
#             dirección : mapa_destino
    def cambiar_mapa(self, nuevo_id):
        pass

#     MÉTODO obtener_mapa_conectado(direccion):
#         devolver el mapa vinculado a esa dirección
    def obtener_mapa_conectado(self, direccion):
        pass

#     MÉTODO eliminar_objeto_de_grid(x, y):
#         quitar símbolo de NPC o ítem del grid
    def eliminar_objeto_de_grid(self, x, y):
        pass

#     MÉTODO hay_portal_en(x, y):
#         verificar si la posición actual es un portal
#         si es así, devolver el mapa de destino
    def hay_portal_en(self,x,y):
        pass

mapa1 = Mapa('Inicio')
mapa1.mostrar()


    








