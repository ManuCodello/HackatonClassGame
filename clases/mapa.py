# mapa.py

import random

# Variables globales - Configuración del Juego
ANCHO_CONSOLA = 80
ALTO_CONSOLA = 24
ANCHO_MAPA = 30
ALTO_MAPA = 30

class Mapa:
    def __init__(self, id_mapa, tipo='base'):
        self.nombre = id_mapa
        self.grid = [['⬛' for _ in range(30)] for _ in range(30)]  # Inicializar con espacios vacíos
        self.npcs = []
        self.items = []
        self.jugador_pos = (1, 6)
        self.conexiones_mapas = {}   # Portales
        self.tipo = tipo  # 'base', 'ciudad', 'laberinto'
        self.portal_visible = False
        self.generar_mapa()

    def mostrar(self):
        """Muestra el mapa en consola"""
        for fila in self.grid:
            print(' '.join(fila))

    def es_posicion_valida(self, x, y):
        """Verifica si una posición es válida para moverse"""
        return (0 <= x < ALTO_MAPA and 
                0 <= y < ANCHO_MAPA and 
                self.grid[x][y] != '🚧')

    def generar_mapa(self):
        """Genera el mapa según su tipo"""
        # Crear bordes del mapa
        for i in range(ANCHO_MAPA):
            self.grid[0][i] = '🚧'  # Borde superior
            self.grid[ALTO_MAPA-1][i] = '🚧'  # Borde inferior

        for i in range(ALTO_MAPA):
            self.grid[i][0] = '🚧'  # Borde izquierdo
            self.grid[i][ANCHO_MAPA-1] = '🚧'  # Borde derecho

        # Generar contenido según tipo de mapa
        if self.tipo == 'base':
            self.generar_calles()
            self.colocar_jugador()
            self.colocar_portal()
        elif self.tipo == 'ciudad':
            self.generar_calles()
            self.colocar_edificios_destruidos()
            self.colocar_jugador()
            self.colocar_npc()
            # Portal se mostrará después de vencer NPC
        elif self.tipo == 'laberinto':
            self.generar_laberinto()

    def colocar_portal(self):
        """Coloca un portal en el mapa"""
        # Limpiar portales previos
        for i in range(1, ALTO_MAPA - 1):
            for j in range(1, ANCHO_MAPA - 1):
                if self.grid[i][j] == '🌀':
                    self.grid[i][j] = '⬛'
        
        # Buscar posición para el portal (esquina inferior derecha disponible)
        for i in range(ALTO_MAPA - 2, 0, -1):
            for j in range(ANCHO_MAPA - 2, 0, -1):
                if self.grid[i][j] == '⬛':
                    self.grid[i][j] = '🌀'
                    return

    def colocar_npc(self):
        """Coloca un NPC en el mapa"""
        intentos = 0
        while intentos < 50:  # Limitar intentos para evitar bucle infinito
            x = random.randint(5, ALTO_MAPA-5)
            y = random.randint(5, ANCHO_MAPA-5)
            if self.grid[x][y] == '⬛':
                self.grid[x][y] = '🤖'
                self.npcs.append({'pos': (x, y), 'vencido': False})
                break
            intentos += 1

    def generar_calles(self):
        """Genera calles en el mapa"""
        # Crear calles horizontales
        for _ in range(3):
            fila = random.randint(3, ALTO_MAPA-4)
            for col in range(1, ANCHO_MAPA-1):
                if self.grid[fila][col] != '🚧':
                    self.grid[fila][col] = '⬛'

        # Crear calles verticales
        for _ in range(3):
            col = random.randint(3, ANCHO_MAPA-4)
            for fila in range(1, ALTO_MAPA-1):
                if self.grid[fila][col] != '🚧':
                    self.grid[fila][col] = '⬛'

    def colocar_edificios_destruidos(self):
        """Añade edificios destruidos y obstáculos"""
        obstaculos = ['🏢', '💥', '🔥', '🚗', '⚡']
        
        for _ in range(15):  # Colocar varios obstáculos
            x = random.randint(2, ALTO_MAPA-3)
            y = random.randint(2, ANCHO_MAPA-3)
            if self.grid[x][y] == '⬜':  # Solo en espacios no utilizados
                self.grid[x][y] = random.choice(obstaculos)

    def mostrar_portal_si_npc_vencido(self):
        """Muestra portal solo si el NPC ha sido vencido"""
        if any(npc['vencido'] for npc in self.npcs):
            self.colocar_portal()

    def generar_laberinto(self):
        """Genera un laberinto para el mapa final"""
        # Inicializar todo como paredes
        self.grid = [['🚧' for _ in range(ANCHO_MAPA)] for _ in range(ALTO_MAPA)]

        # Crear camino garantizado desde inicio hasta salida
        x, y = 1, 1
        self.grid[x][y] = '⬛'
        self.jugador_pos = (x, y)

        # Camino en zigzag hacia la salida
        # Ir hacia la derecha
        while y < ANCHO_MAPA - 3:
            y += 1
            self.grid[x][y] = '⬛'

        # Ir hacia abajo
        while x < ALTO_MAPA - 3:
            x += 1
            self.grid[x][y] = '⬛'

        # Colocar salida
        self.grid[ALTO_MAPA-2][ANCHO_MAPA-2] = '🌀'

        # Añadir algunos caminos adicionales para hacer el laberinto más interesante
        for _ in range(10):
            start_x = random.randint(1, ALTO_MAPA-2)
            start_y = random.randint(1, ANCHO_MAPA-2)
            length = random.randint(3, 8)
            
            # Camino horizontal o vertical aleatorio
            if random.choice([True, False]):  # Horizontal
                for i in range(length):
                    if start_y + i < ANCHO_MAPA - 1:
                        self.grid[start_x][start_y + i] = '⬛'
            else:  # Vertical
                for i in range(length):
                    if start_x + i < ALTO_MAPA - 1:
                        self.grid[start_x + i][start_y] = '⬛'

    def colocar_jugador(self):
        """Establece la posición inicial del jugador"""
        # Buscar primera posición libre para el jugador
        for i in range(1, ALTO_MAPA - 1):
            for j in range(1, ANCHO_MAPA - 1):
                if self.grid[i][j] == '⬛':
                    self.jugador_pos = (i, j)
                    return







