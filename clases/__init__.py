# Inicializador del paquete clases
# clases/__init__.py

# Este archivo hace que la carpeta 'clases' sea un paquete de Python
# Permite importar las clases desde otros archivos

from .jugador import Jugador
from .mapa import Mapa
from .npc import NPC
from .minijuegos import MiniJuegos
from .juego import Juego

__all__ = ['Jugador', 'Mapa', 'NPC', 'MiniJuegos', 'Juego']