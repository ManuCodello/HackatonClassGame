# Jugador principal

# Constantes de dirección


DIRECCION_ARRIBA = (0, -1)
DIRECCION_ABAJO = (0, 1)
DIRECCION_IZQUIERDA = (-1, 0)
DIRECCION_DERECHA = (1, 0)


class Jugador:
    def __init__(self, x_inicial=0, y_inicial=0):
        # Posición inicial en la matriz
        self.x = x_inicial
        self.y = y_inicial

        # Progreso del juego
        self.llaves = 0
        self.llaves_necesarias = 3

        # Mapa actual
        self.mapa_actual = "inicial"

        # Estado del jugador (evita que le jugador se mueva mientras juega)
        # vivo es para terminar el juego si es que gana o pierde
        self.vivo = True
        self.en_minijuego = False

    def mover(self, direccion, mapa):
        if not self.vivo or self.en_minijuego:
            return False

        direccion_x = 0
        direccion_y = 0

        if direccion == "w" or direccion == "W":
            direccion_x = DIRECCION_ARRIBA[0]
            direccion_y = DIRECCION_ARRIBA[1]
        elif direccion == "s" or direccion == "S":
            direccion_x = DIRECCION_ABAJO[0]
            direccion_y = DIRECCION_ABAJO[1]
        elif direccion == "d" or direccion == "D":
            direccion_x = DIRECCION_DERECHA[0]
            direccion_y = DIRECCION_DERECHA[1]
        elif direccion == "a" or direccion == "A":
            direccion_x = DIRECCION_IZQUIERDA[0]
            direccion_y = DIRECCION_IZQUIERDA[1]
        else:
            return False

        # Calculo de nueva posición
        nuevo_x = self.x + direccion_x
        nuevo_y = self.y + direccion_y

        # Verificamos los límites
        if not (0 <= nuevo_x < 30) or not (0 <= nuevo_y < 30):
            return False

        # Verificar obstáculos
        if mapa[self.x][self.y] != ".":
            print("Probemos por otro lugar, no podemos pasar por ahí!!")

        self.x = nuevo_x
        self.y = nuevo_y
        return True

    def obtener_posicion(self):
        return (self.x, self.y)

    def iniciar_minijuego(self):
        self.en_minijuego = True

    def terminar_minijuego(self, exitoso):
        self.en_minijuego = False
        if exitoso:
            self.llaves = self.llaves + 1
            print(f"¡Minijuego completado! Llaves: {self.llaves}/3")
        else:
            print("Minijuego fallado. Volverá 3 casillas para atrás")
