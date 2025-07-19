#
# juego.py

"""
Clase principal del juego que gestiona toda la lógica de flujo,
transiciones entre mapas usando portales, interacciones y el estado general.
"""

import os
import time
from .jugador import Jugador
from .mapa import Mapa
from .npc import NPC
from .minijuegos import MiniJuegos

class Juego:
    def __init__(self):
        # Configuración inicial del juego
        self.jugador = Jugador(1, 1)  # Posición inicial
        self.mapa_actual = None
        self.npcs_actuales = []
        self.minijuegos = MiniJuegos()
        
        # Sistema de vidas y progreso
        self.vidas = 3
        self.vidas_maximas = 3
        self.stage_actual = 1  # Empezamos en mapa_1
        self.mapa_maximo_desbloqueado = 1
        
        # Control de juego
        self.juego_terminado = False
        self.resultado_final = None
        
        # Límites de pasos por mapa
        self.pasos_por_mapa = {
            1: 100,  # mapa_1 - base inicial
            2: 80,   # mapa_2 - ciudad
            3: 70,   # mapa_3 - ciudad
            4: 60,   # mapa_4 - ciudad
            5: 150   # mapa_5 - laberinto final
        }
        self.pasos_actuales = 0
        
        # Configuración de stages
        self.configurar_stages()
        
    def configurar_stages(self):
        """Configura la información de cada mapa del juego"""
        self.info_stages = {
            1: {
                "nombre": "🏠 Base Paraguaya - Punto de Partida",
                "descripcion": "Tu base de operaciones en las ruinas de Asunción",
                "objetivo": "Explora y encuentra el portal al siguiente sector",
                "emoji_especial": "🏠",
                "tipo": "base"
            },
            2: {
                "nombre": "🏢 Sector Central - Zona de Combate",
                "descripcion": "Ruinas del centro de la ciudad, lleno de peligros",
                "objetivo": "Derrota al NPC y activa el portal",
                "emoji_especial": "⚡",
                "tipo": "ciudad"
            },
            3: {
                "nombre": "🏥 Sector Médico - Hospital en Ruinas",
                "descripcion": "Antiguos hospitales convertidos en fortalezas",
                "objetivo": "Supera el desafío del superviviente médico",
                "emoji_especial": "💊",
                "tipo": "ciudad"
            },
            4: {
                "nombre": "🏭 Sector Industrial - Puerto Destruido",
                "descripción": "Zona industrial con recursos valiosos",
                "objetivo": "Último desafío antes del laberinto final",
                "emoji_especial": "🛠️",
                "tipo": "ciudad"
            },
            5: {
                "nombre": "🌀 Laberinto del Apocalipsis - Escape Final",
                "descripcion": "El laberinto final que lleva a la salvación",
                "objetivo": "Encuentra la salida 🌀 antes de que se agote el tiempo",
                "emoji_especial": "🗝️",
                "tipo": "laberinto"
            }
        }
    
    def limpiar_pantalla(self):
        """Limpia la pantalla de la consola"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def mostrar_hud(self):
        """Muestra la información del jugador (HUD)"""
        stage_info = self.info_stages[self.stage_actual]
        
        print("╔" + "═" * 78 + "╗")
        print(f"║ {stage_info['emoji_especial']} {stage_info['nombre']:<70} ║")
        print("╠" + "═" * 78 + "╣")
        print(f"║ ❤️  Vidas: {self.vidas}/{self.vidas_maximas} │ 🎯 Mapa: {self.stage_actual}/5 │ 👟 Pasos: {self.pasos_actuales}/{self.pasos_por_mapa[self.stage_actual]} ║")
        print(f"║ 📍 Posición: ({self.jugador.x}, {self.jugador.y}) │ 🎲 Objetivo: {stage_info['objetivo'][:35]}... ║")
        print("╚" + "═" * 78 + "╝")
        print()
    
    def mostrar_mapa(self):
        """Renderiza el mapa actual tal como viene del sistema de mapa"""
        if not self.mapa_actual:
            return
            
        # Crear una copia de la matriz para no modificar la original
        matriz_display = [fila[:] for fila in self.mapa_actual.grid]
        
        # Colocar el jugador en su posición actual (sobrescribe lo que esté ahí)
        matriz_display[self.jugador.x][self.jugador.y] = "🦸"
        
        # Renderizar el mapa
        for fila in matriz_display:
            print(' '.join(fila))
    
    def cargar_mapa(self, numero_mapa):
        """Carga un mapa específico usando el sistema de Mapa"""
        self.stage_actual = numero_mapa
        self.pasos_actuales = 0
        
        # Obtener información del stage
        stage_info = self.info_stages[numero_mapa]
        tipo_mapa = stage_info["tipo"]
        
        # Crear el mapa usando el sistema existente
        self.mapa_actual = Mapa(f'mapa_{numero_mapa}', tipo=tipo_mapa)
        
        # Ajustar posición inicial del jugador
        if hasattr(self.mapa_actual, 'jugador_pos'):
            self.jugador.x, self.jugador.y = self.mapa_actual.jugador_pos
        else:
            # Buscar primera posición libre si no se definió jugador_pos
            for i in range(1, 29):
                for j in range(1, 29):
                    if self.mapa_actual.grid[i][j] == '⬛':
                        self.jugador.x, self.jugador.y = i, j
                        break
                if self.mapa_actual.grid[i][j] == '⬛':
                    break
        
        # Cargar NPCs si es un mapa de ciudad
        if tipo_mapa == "ciudad":
            self.crear_npc_para_mapa(numero_mapa)
        
        # Mensaje de transición
        print(f"\n🌍 Entrando a: {stage_info['nombre']}")
        print(f"📋 {stage_info['descripcion']}")
        print(f"🎯 {stage_info['objetivo']}")
        print("\n💡 Muévete con WASD, busca NPCs (🤖) y portales (🌀)")
        input("Presiona ENTER para continuar...")
    
    def crear_npc_para_mapa(self, numero_mapa):
        """Crea NPCs específicos para cada mapa"""
        if numero_mapa == 2:
            npc = NPC(
                "Soldado Superviviente",
                {"¿Cuál fue el primer presidente de Paraguay?": "carlos antonio lopez"},
                "¡Alto! Soy el guardián de este sector. Responde mi pregunta para continuar."
            )
            
        elif numero_mapa == 3:
            npc = NPC(
                "Doctor de Guerra",
                {"¿Qué órgano bombea la sangre?": "corazon"},
                "Necesito verificar tus conocimientos médicos básicos antes de dejarte pasar."
            )
            
        elif numero_mapa == 4:
            npc = NPC(
                "Ingeniero Industrial", 
                {"¿Cuál es el metal más común en la industria?": "hierro"},
                "Este sector industrial requiere conocimientos técnicos. Demuestra que sabes."
            )
        else:
            return
            
        # El NPC ya está posicionado en el mapa por la clase Mapa
        self.npcs_actuales = [npc]
    
    def verificar_interaccion_npc(self):
        """Verifica si el jugador está en la misma posición que un NPC"""
        if not self.npcs_actuales:
            return None
            
        # Verificar si hay un NPC en la posición actual del jugador
        pos_jugador = (self.jugador.x, self.jugador.y)
        
        # Verificar en las posiciones de NPCs del mapa
        for npc_info in self.mapa_actual.npcs:
            if npc_info['pos'] == pos_jugador and not npc_info['vencido']:
                return self.npcs_actuales[0]  # Retorna el primer NPC disponible
                
        return None
    
    def procesar_interaccion_npc(self, npc):
        """Maneja la interacción con un NPC"""
        self.limpiar_pantalla()
        print("="*60)
        npc.presentarse()
        print("="*60)
        
        respuesta = input("\n¿Quieres enfrentar el desafío? (s/n): ").lower().strip()
        
        if respuesta != 's':
            print("🔄 Puedes volver cuando estés listo.")
            input("Presiona ENTER para continuar...")
            return False
            
        # Realizar el acertijo del NPC
        print(f"\n🎮 ¡Iniciando desafío con {npc.nombre}!")
        npc.acertijo()
        
        # Verificar si se resolvió el acertijo
        if npc.acertijo_resuelto:
            print("🎉 ¡Excelente! Has superado el desafío.")
            
            # Marcar NPC como vencido en el mapa
            for npc_info in self.mapa_actual.npcs:
                if npc_info['pos'] == (self.jugador.x, self.jugador.y):
                    npc_info['vencido'] = True
                    break
            
            # Mostrar portal después de vencer NPC
            self.mapa_actual.mostrar_portal_si_npc_vencido()
            print("🌀 ¡El portal al siguiente sector se ha activado!")
            input("Presiona ENTER para continuar...")
            return True
        else:
            print("💔 Has fallado el desafío.")
            self.vidas -= 1
            print(f"Vidas restantes: {self.vidas}")
            
            if self.vidas <= 0:
                self.juego_terminado = True
                self.resultado_final = "derrota"
                return False
                
            input("Presiona ENTER para continuar...")
            return False
    
    def verificar_portal(self):
        """Verifica si el jugador está en un portal"""
        pos_jugador = (self.jugador.x, self.jugador.y)
        
        if self.mapa_actual.grid[pos_jugador[0]][pos_jugador[1]] == '🌀':
            return True
        return False
    
    def procesar_portal(self):
        """Procesa el uso de un portal"""
        if self.stage_actual < 5:
            # Avanzar al siguiente mapa
            print(f"🌀 ¡Portal activado! Avanzando al mapa {self.stage_actual + 1}...")
            input("Presiona ENTER para continuar...")
            self.cargar_mapa(self.stage_actual + 1)
        else:
            # Victoria en el laberinto final
            self.juego_terminado = True
            self.resultado_final = "victoria"
    
    def verificar_limites_pasos(self):
        """Verifica si el jugador ha excedido el límite de pasos"""
        if self.pasos_actuales >= self.pasos_por_mapa[self.stage_actual]:
            print("⏰ ¡Te has quedado sin pasos en este mapa!")
            self.vidas -= 1
            print(f"💔 Perdiste una vida. Vidas restantes: {self.vidas}")
            
            if self.vidas <= 0:
                self.juego_terminado = True
                self.resultado_final = "derrota"
                return "game_over"
            else:
                print("🔄 Reiniciando el mapa actual...")
                self.cargar_mapa(self.stage_actual)
                return "reiniciar_mapa"
                
        return None
    
    def procesar_movimiento(self, direccion):
        """Procesa el movimiento del jugador usando el sistema de mapa"""
        if self.jugador.mover(direccion, self.mapa_actual):
            self.pasos_actuales += 1
            
            # Verificar si está en un portal
            if self.verificar_portal():
                print("🌀 Estás en un portal. Presiona P para usarlo.")
                
            # Verificar si hay un NPC en la posición actual
            npc = self.verificar_interaccion_npc()
            if npc:
                print(f"🤖 ¡Has encontrado a {npc.nombre}! Presiona E para interactuar.")
            
            return self.verificar_limites_pasos()
        else:
            print("🚫 No puedes moverte en esa dirección.")
            
        return None
    
    def procesar_minijuego_extra(self):
        """Procesa los minijuegos especiales del sistema MiniJuegos"""
        print("🎮 ¡Desafío especial desbloqueado!")
        print("Selecciona tu desafío:")
        print("1. Código Secreto")
        print("2. Número Mágico") 
        print("3. Memoria Visual")
        
        while True:
            try:
                opcion = int(input("Elige tu desafío (1-3): "))
                if 1 <= opcion <= 3:
                    break
                else:
                    print("Opción inválida. Elige 1, 2 o 3.")
            except ValueError:
                print("Por favor ingresa un número válido.")
        
        exitoso = False
        if opcion == 1:
            exitoso = self.minijuegos.juego_codigo_secreto()
        elif opcion == 2:
            exitoso = self.minijuegos.juego_numerico_magico()
        elif opcion == 3:
            exitoso = self.minijuegos.juego_memoria_visual()
        
        if exitoso:
            print("🎉 ¡Excelente! Bonus completado.")
            print("🎁 Recuperas una vida extra!")
            self.vidas = min(self.vidas + 1, self.vidas_maximas)
        else:
            print("💔 Minijuego fallado, pero puedes continuar.")
            
        input("Presiona ENTER para continuar...")
    
    def ejecutar(self):
        """Bucle principal del juego"""
        print("🎮 ¡Bienvenido a Guerra Posapocalíptica!")
        
        # Cargar el primer mapa
        self.cargar_mapa(1)
        
        while not self.juego_terminado:
            self.limpiar_pantalla()
            self.mostrar_hud()
            self.mostrar_mapa()
            
            # Obtener entrada del usuario
            print("\n🎮 Controles:")
            print("W(arriba) A(izquierda) S(abajo) D(derecha) - Movimiento")
            print("E(interactuar) P(usar portal) M(minijuego extra) Q(salir)")
            entrada = input("🕹️  Ingresa tu comando: ").lower().strip()
            
            if entrada == 'q':
                self.juego_terminado = True
                self.resultado_final = "abandono"
                break
                
            elif entrada in ['w', 'a', 's', 'd']:
                resultado = self.procesar_movimiento(entrada)
                if resultado == "game_over":
                    break
                elif resultado == "reiniciar_mapa":
                    continue
                    
            elif entrada == 'e':
                npc = self.verificar_interaccion_npc()
                if npc:
                    self.procesar_interaccion_npc(npc)
                else:
                    print("🤷 No hay ningún NPC aquí para interactuar.")
                    input("Presiona ENTER para continuar...")
                    
            elif entrada == 'p':
                if self.verificar_portal():
                    self.procesar_portal()
                else:
                    print("🚫 No estás en un portal.")
                    input("Presiona ENTER para continuar...")
                    
            elif entrada == 'm':
                self.procesar_minijuego_extra()
                    
            else:
                print("❌ Comando no válido.")
                input("Presiona ENTER para continuar...")
        
        return self.resultado_final