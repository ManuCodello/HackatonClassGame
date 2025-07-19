class NPC:
    def __init__(self, nombre, x, y, dialogo, presentacion):
        self.nombre = nombre
        self.x = x
        self.y = y
        self.dialogo = dialogo
        self.presentacion = presentacion

    def presentarse(self, jugador):
        pass

    def acertijo(self, jugador):
        pass

    def entregar_llave(self, jugador):
        pass

