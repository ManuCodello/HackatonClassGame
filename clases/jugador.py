# jugador.py

class Jugador:
    def __init__(self, x_inicial=1, y_inicial=1):
        # Posición inicial en la matriz (corregido: x es fila, y es columna)
        self.x = x_inicial
        self.y = y_inicial

        # Progreso del juego
        self.llaves = 0
        self.llaves_necesarias = 3

        # Mapa actual
        self.mapa_actual = "inicial"

        # Estado del jugador
        self.vivo = True
        self.en_minijuego = False

    def mover(self, direccion, mapa):
        """Mueve al jugador en la dirección especificada"""
        if not self.vivo or self.en_minijuego:
            return False

        # Calcular nueva posición basada en la dirección
        nuevo_x = self.x
        nuevo_y = self.y

        if direccion.lower() == "w":  # Arriba
            nuevo_x = self.x - 1
        elif direccion.lower() == "s":  # Abajo
            nuevo_x = self.x + 1
        elif direccion.lower() == "a":  # Izquierda
            nuevo_y = self.y - 1
        elif direccion.lower() == "d":  # Derecha
            nuevo_y = self.y + 1
        else:
            return False

        # Verificar límites del mapa (30x30)
        if not (0 <= nuevo_x < 30) or not (0 <= nuevo_y < 30):
            return False

        # Verificar si la posición es válida usando el método del mapa
        if not mapa.es_posicion_valida(nuevo_x, nuevo_y):
            return False

        # Verificar que la casilla de destino no sea un obstáculo
        casilla_destino = mapa.grid[nuevo_x][nuevo_y]
        if casilla_destino == '🚧':  # Obstáculo
            return False

        # Mover el jugador
        self.x = nuevo_x
        self.y = nuevo_y
        return True

    def obtener_posicion(self):
        """Retorna la posición actual del jugador"""
        return (self.x, self.y)

    def iniciar_minijuego(self):
        """Marca que el jugador está en un minijuego"""
        self.en_minijuego = True

    def terminar_minijuego(self, exitoso):
        """Termina el minijuego y actualiza el estado"""
        self.en_minijuego = False
        if exitoso:
            self.llaves += 1
            print(f"¡Minijuego completado! Llaves: {self.llaves}/3")
        else:
            print("Minijuego fallado.")

    def tiene_llaves_suficientes(self):
        """Verifica si tiene las 3 llaves necesarias"""
        return self.llaves >= self.llaves_necesarias

    def morir(self):
        """Mata al jugador"""
        self.vivo = False

    def resetear_posicion(self, x, y):
        """Resetea la posición del jugador"""
        self.x = x
        self.y = y