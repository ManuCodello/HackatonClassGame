# Archivo de variables globales

# globals.py - ARCHIVO COMPARTIDO ENTRE TODOS


""" 
        Reparto de Responsabilidades
LÍDER (Tú) - Clase Juego + Integración
Responsabilidades:

clases/juego.py - Clase principal del juego
main.py - Punto de entrada
globals.py - Variables globales compartidas
Integración final y coordinación
Game loop y estados del juego

COMPAÑERO 1 - Clase Jugador + Sistema de Input
Responsabilidades:

clases/jugador.py - Clase Jugador completa
utils/input_handler.py - Manejo de teclas y comandos
utils/display.py - Funciones de renderizado en consola
Sistema de inventario y stats del jugador

COMPAÑERO 2 - Clase Mapa + Datos de Mapas
Responsabilidades:

clases/mapa.py - Clase Mapa completa
datos/mapas_data.py - Todos los mapas hardcodeados en Python
Sistema de navegación entre mapas
Renderizado de mapas en consola

COMPAÑERO 3 - Clase NPC + MiniJuegos + Datos NPCs
Responsabilidades:

clases/npc.py - Clase NPC completa
clases/minijuegos.py - Todos los mini-juegos
datos/npcs_data.py - Todos los NPCs y diálogos hardcodeados
Sistema de interacciones y combate básico


Variables Globales Compartidas (globals.py)
python# globals.py - ARCHIVO COMPARTIDO ENTRE TODOS
# ============================================

# CONFIGURACIÓN DEL JUEGO
ANCHO_CONSOLA = 80
ALTO_CONSOLA = 24
ANCHO_MAPA = 20
ALTO_MAPA = 15
FPS = 60

# SÍMBOLOS DEL JUEGO (Para renderizado ASCII)
SIMBOLOS = {
    'jugador': 'P',
    'npc_aliado': 'A',
    'npc_enemigo': 'E',
    'npc_neutral': 'N',
    'pared': '#',
    'suelo': '.',
    'puerta': 'D',
    'item': 'I',
    'salida': 'S',
    'entrada': 'O'
}

# COMANDOS DE ENTRADA
COMANDOS_MOVIMIENTO = ['w', 's', 'a', 'd', 'W', 'S', 'A', 'D']
COMANDO_INTERACTUAR = ['e', 'E']
COMANDO_INVENTARIO = ['i', 'I']
COMANDO_SALIR = ['q', 'Q']
COMANDO_AYUDA = ['h', 'H']

# TIPOS DE NPC
TIPO_ALIADO_PARAGUAY = 'aliado_py'
TIPO_ALIADO_URSS = 'aliado_urss'
TIPO_ENEMIGO_PARAGUAY = 'enemigo_py'
TIPO_ENEMIGO_URSS = 'enemigo_urss'
TIPO_NEUTRAL = 'neutral'
TIPO_COMERCIANTE = 'comerciante'

# TIPOS DE MINIJUEGOS
MINIJUEGO_MEMORIA = 'memoria'
MINIJUEGO_MATEMATICAS = 'matematicas'
MINIJUEGO_ADIVINANZA = 'adivinanza'
MINIJUEGO_COMBATE = 'combate'

# ESTADOS DEL JUEGO
ESTADO_MENU = 'menu'
ESTADO_JUGANDO = 'jugando'
ESTADO_DIALOGO = 'dialogo'
ESTADO_INVENTARIO = 'inventario'
ESTADO_MINIJUEGO = 'minijuego'
ESTADO_GAME_OVER = 'game_over'
ESTADO_VICTORIA = 'victoria'

# DIRECCIONES DE MOVIMIENTO
DIRECCION_ARRIBA = (0, -1)
DIRECCION_ABAJO = (0, 1)
DIRECCION_IZQUIERDA = (-1, 0)
DIRECCION_DERECHA = (1, 0)

DIRECCIONES = {
    'w': DIRECCION_ARRIBA,
    'W': DIRECCION_ARRIBA,
    's': DIRECCION_ABAJO,
    'S': DIRECCION_ABAJO,
    'a': DIRECCION_IZQUIERDA,
    'A': DIRECCION_IZQUIERDA,
    'd': DIRECCION_DERECHA,
    'D': DIRECCION_DERECHA
}

# MAPAS DISPONIBLES (IDs)
MAPA_BUNKER = 'bunker_paraguay'
MAPA_RUINAS = 'ruinas_asuncion'
MAPA_BASE_SOVIETICA = 'base_sovietica'
MAPA_TIERRA_NADIE = 'tierra_nadie'
MAPA_REACTOR = 'reactor_nuclear'

MAPAS_ORDEN = [MAPA_BUNKER, MAPA_RUINAS, MAPA_BASE_SOVIETICA, MAPA_TIERRA_NADIE, MAPA_REACTOR]

# ITEMS DEL JUEGO
ITEM_ARMA = 'arma'
ITEM_MEDICINA = 'medicina'
ITEM_LLAVE = 'llave'
ITEM_DOCUMENTO = 'documento'
ITEM_COMIDA = 'comida'

# STATS INICIALES DEL JUGADOR
VIDA_INICIAL = 100
VIDA_MAXIMA = 100
EXPERIENCIA_INICIAL = 0
NIVEL_INICIAL = 1
FUERZA_INICIAL = 10
DEFENSA_INICIAL = 5

# CONFIGURACIÓN DE COMBATE
DAÑO_BASE_JUGADOR = 15
DAÑO_BASE_NPC = 10
PROBABILIDAD_CRITICO = 0.15
MULTIPLICADOR_CRITICO = 2.0

# MENSAJES DEL SISTEMA
MSG_BIENVENIDA = "¡Bienvenido al fin del mundo! Paraguay vs URSS"
MSG_GAME_OVER = "¡Has muerto! El mundo está condenado..."
MSG_VICTORIA = "¡Has salvado el mundo! Paraguay prevaleció sobre la URSS"
MSG_INVENTARIO_VACIO = "Tu inventario está vacío"
MSG_NO_PUEDES_MOVER = "No puedes moverte en esa dirección"
MSG_COMANDO_INVALIDO = "Comando inválido. Presiona 'h' para ayuda"

# AYUDA DEL JUEGO
TEXTO_AYUDA = """
"""=== CONTROLES ===
WASD - Mover
E - Interactuar
I - Inventario
H - Ayuda
Q - Salir

=== OBJETIVO ===
Navega por los mapas, habla con NPCs,
completa mini-juegos y salva el mundo
de la guerra Paraguay vs URSS"""
"""

Variables Compartidas Entre Clases
Estado Global del Juego (Estas las lee/modifica cada clase)
python# Estado actual del juego
estado_juego_actual = ESTADO_MENU
juego_corriendo = True

# Posición del jugador (CRÍTICO - todos la necesitan)
jugador_x = 1
jugador_y = 1
jugador_vida = VIDA_INICIAL
jugador_nivel = NIVEL_INICIAL
jugador_experiencia = EXPERIENCIA_INICIAL
jugador_inventario = []
jugador_faccion = "Paraguay"  # o "URSS"

# Estado del mapa actual
mapa_actual_id = MAPA_BUNKER
mapa_actual_grid = []  # Se llena desde mapas_data.py
mapa_ancho = ANCHO_MAPA
mapa_alto = ALTO_MAPA

# NPCs en el mapa actual
npcs_en_mapa_actual = {}  # {id: objeto_npc}
npc_interactuando = None  # Con qué NPC está hablando el jugador

# Estado de diálogo
en_dialogo = False
dialogo_actual = ""
dialogo_opciones = []

# Estado de mini-juego
en_minijuego = False
tipo_minijuego_actual = None
resultado_minijuego = None  # True/False/None


Protocolos de Comunicación Entre Clases
    1. Cómo Acceder a Variables Globales
    python# En CADA archivo de clase, al principio:
    import globals as g

    # Para leer una variable:
    vida_actual = g.jugador_vida

    # Para modificar una variable (SOLO la clase responsable):
    g.jugador_vida = nueva_vida
    2. Qué Variables Puede Modificar Cada Clase
Clase Jugador (Compañero 1):
    PUEDE MODIFICAR:

    g.jugador_x, g.jugador_y (movimiento)
    g.jugador_vida, g.jugador_experiencia
    g.jugador_inventario
    g.jugador_nivel

Clase Mapa (Compañero 2):
    PUEDE MODIFICAR:

    g.mapa_actual_id
    g.mapa_actual_grid
    g.mapa_ancho, g.mapa_alto

Clase NPC (Compañero 3):
    PUEDE MODIFICAR:

    g.npcs_en_mapa_actual
    g.npc_interactuando
    g.en_dialogo
    g.dialogo_actual
    g.en_minijuego, g.tipo_minijuego_actual

Clase Juego (Líder):
    PUEDE MODIFICAR:

    g.estado_juego_actual
    g.juego_corriendo
    Cualquier variable en emergencias

3. Métodos Mínimos Obligatorios
Clase Juego (Líder):
    pythondef _init_(self)
    def iniciar_juego(self)
    def game_loop(self)
    def actualizar(self)
    def renderizar(self)
    def procesar_input(self)
    def cambiar_estado(self, nuevo_estado)
Clase Jugador (Compañero 1):
    pythondef _init_(self)
    def mover(self, direccion)
    def get_posicion(self)
    def interactuar(self)
    def agregar_item(self, item)
    def usar_item(self, item)
    def recibir_daño(self, cantidad)
    def esta_vivo(self)
Clase Mapa (Compañero 2):
    pythondef _init_(self, id_mapa)
    def cargar_mapa(self, id_mapa)
    def es_posicion_valida(self, x, y)
    def get_simbolo_en(self, x, y)
    def renderizar_mapa(self)
    def cambiar_mapa(self, nuevo_id)
Clase NPC (Compañero 3):
    pythondef _init_(self, id, tipo, x, y, nombre)
    def hablar(self, jugador)
    def iniciar_combate(self, jugador)
    def dar_mision(self, jugador)
    def esta_en_posicion(self, x, y)
    def cargar_npcs_para_mapa(self, id_mapa)
    
"""
    