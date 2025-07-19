# juego.py - Versión Corregida

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
        
        # Control de minijuegos para portales - NUEVO
        self.minijuegos_completados = set()  # Almacena qué minijuegos ya se completaron
        self.minijuegos_disponibles = {
            1: "codigo_secreto",
            2: "numerico_magico", 
            3: "memoria_visual"
        }
        
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
                "objetivo": "Habla con Santi Penna y usa el portal",
                "emoji_especial": "🏠",
                "tipo": "base"
            },
            2: {
                "nombre": "🏢 Sector Central - Zona de Combate",
                "descripcion": "Ruinas del centro de la ciudad, lleno de peligros",
                "objetivo": "Encuentra a Sebastian Canoso y completa su desafío",
                "emoji_especial": "⚡",
                "tipo": "ciudad"
            },
            3: {
                "nombre": "🏥 Sector Médico - Hospital en Ruinas",
                "descripcion": "Antiguos hospitales convertidos en fortalezas",
                "objetivo": "Busca a Jorge Molina jr. y ayúdalo con el pendrive",
                "emoji_especial": "💊",
                "tipo": "ciudad"
            },
            4: {
                "nombre": "🏭 Sector Industrial - Puerto Destruido",
                "descripcion": "Zona industrial con recursos valiosos",  # CORREGIDO: era 'descripción' con tilde
                "objetivo": "Encuentra a Francesco y supera su prueba de memoria",
                "emoji_especial": "🛠️",
                "tipo": "ciudad"
            },
            5: {
                "nombre": "🌀 Laberinto del Apocalipsis - Escape Final",
                "descripcion": "El laberinto final que lleva a la salvación",
                "objetivo": "Encuentra al Hacker y escapa por la salida 🌀",
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
        print(f"║ 🎮 Minijuegos: {len(self.minijuegos_completados)}/3 │ 🗝️  Llaves: {self.jugador.llaves}/3 ║")
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
        
        # Cargar NPCs específicos según el mapa
        self.crear_npc_para_mapa(numero_mapa)
        
        # Mensaje de transición
        print(f"\n🌍 Entrando a: {stage_info['nombre']}")
        print(f"📋 {stage_info['descripcion']}")
        print(f"🎯 {stage_info['objetivo']}")
        print("\n💡 Muévete con WASD, busca NPCs (🤖) y portales (🌀)")
        input("Presiona ENTER para continuar...")
    
    def crear_npc_para_mapa(self, numero_mapa):
        """Crea NPCs específicos para cada mapa con los personajes requeridos"""
        if numero_mapa == 1:
            # Santi Penna en el mapa base
            npc = NPC(
                "Santi Penna",
                {"¿Estás listo para la misión?": "si"},
                [
                    "¿Vos sos el nuevo? Te esperábamos.",
                    "Las calles están más tranquilas que de costumbre... demasiado tranquilas.",
                    "El hacker fue capturado cerca del río. Pero antes envió una señal.",
                    "Sebastián Canoso tiene la primera pista. Buscalo en la ciudad."
                ]
            )
            
        elif numero_mapa == 2:
            # Sebastian Canoso
            npc = NPC(
                "Sebastian Canoso",
                {"¿Cuál es la capital de Paraguay?": "asuncion"},
                [
                    "Santi me avisó que vendrías.",
                    "La señal que mandó no la pudimos descifrar por completo, ayudanos a descifrar el codigo secreto adivinando lo siguiente"
                ]
            )
            
        elif numero_mapa == 3:
            # Jorge Molina jr.
            npc = NPC(
                "Jorge Molina jr.",
                {"¿Cuántos bits tiene un byte?": "8"},
                [
                    "¿Vos venís por la señal?",
                    "Los rusos dejaron bombas por todas partes ayudame a modificar este pendrive, porque yo no lo pude entender."
                ]
            )
            
        elif numero_mapa == 4:
            # Francesco Solono Virgolini
            npc = NPC(
                "Francesco Solono Virgolini",
                {"¿En qué año fue la Guerra del Chaco?": "1932"},
                [
                    "Shhh… bajá la voz. Están por todas partes.",
                    "Solo te dejaré pasar si sé que no morirás como los niños 200 años atrás.",
                    "Memorizate estas palabras, y si escuchás a alguien gritar ya sabés que hacer..."
                ]
            )
            
        elif numero_mapa == 5:
            # El Hacker
            npc = NPC(
                "El Hacker",
                {"¿Estás listo para escapar?": "si"},
                [
                    "...¿Hola?... ¿Me escuchás?",
                    "Gracias por venir.",
                    "Ahora que ya podemos enfocarnos en esta guerra nuevamente (cof.. cof...).",
                    "Apurate. Tupã está esperando tu llamado final."
                ]
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
        """Procesa el uso de un portal - AHORA REQUIERE MINIJUEGO OBLIGATORIO"""
        if self.stage_actual < 5:
            # Verificar si necesita hacer minijuego para avanzar
            if self.stage_actual in self.minijuegos_disponibles:
                minijuego_tipo = self.minijuegos_disponibles[self.stage_actual]
                
                # Si ya completó este minijuego, puede pasar
                if minijuego_tipo in self.minijuegos_completados:
                    print(f"✅ Ya completaste el minijuego de este sector.")
                else:
                    # Debe completar el minijuego para usar el portal
                    print(f"🔒 Portal bloqueado. Debes completar el minijuego para avanzar.")
                    print(f"🎮 Iniciando minijuego obligatorio...")
                    input("Presiona ENTER para comenzar...")
                    
                    exitoso = self.ejecutar_minijuego_especifico(minijuego_tipo)
                    
                    if exitoso:
                        print("🎉 ¡Minijuego completado! Portal desbloqueado.")
                        self.minijuegos_completados.add(minijuego_tipo)
                        self.jugador.llaves += 1
                        input("Presiona ENTER para usar el portal...")
                    else:
                        print("💔 Minijuego fallado. Portal sigue bloqueado.")
                        self.vidas -= 1
                        print(f"Vidas restantes: {self.vidas}")
                        
                        if self.vidas <= 0:
                            self.juego_terminado = True
                            self.resultado_final = "derrota"
                        
                        input("Presiona ENTER para continuar...")
                        return
            
            # Si llegó aquí, puede avanzar al siguiente mapa
            print(f"🌀 ¡Portal activado! Avanzando al mapa {self.stage_actual + 1}...")
            input("Presiona ENTER para continuar...")
            self.cargar_mapa(self.stage_actual + 1)
        else:
            # Victoria en el laberinto final
            self.juego_terminado = True
            self.resultado_final = "victoria"
    
    def ejecutar_minijuego_especifico(self, tipo_minijuego):
        """Ejecuta un minijuego específico"""
        if tipo_minijuego == "codigo_secreto":
            return self.minijuegos.juego_codigo_secreto()
        elif tipo_minijuego == "numerico_magico":
            return self.minijuegos.juego_numerico_magico()
        elif tipo_minijuego == "memoria_visual":
            return self.minijuegos.juego_memoria_visual()
        else:
            return False
    
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
        """Procesa los minijuegos extras opcionales"""
        print("🎮 ¡Desafío especial desbloqueado!")
        
        # Mostrar solo minijuegos no completados
        opciones_disponibles = []
        print("Minijuegos disponibles:")
        
        if "codigo_secreto" not in self.minijuegos_completados:
            opciones_disponibles.append(("1", "codigo_secreto", "Código Secreto"))
            print("1. Código Secreto")
            
        if "numerico_magico" not in self.minijuegos_completados:
            opciones_disponibles.append(("2", "numerico_magico", "Número Mágico"))
            print("2. Número Mágico")
            
        if "memoria_visual" not in self.minijuegos_completados:
            opciones_disponibles.append(("3", "memoria_visual", "Memoria Visual"))
            print("3. Memoria Visual")
        
        if not opciones_disponibles:
            print("🏆 ¡Ya completaste todos los minijuegos!")
            input("Presiona ENTER para continuar...")
            return
        
        while True:
            opcion = input("Elige tu desafío: ").strip()
            minijuego_seleccionado = None
            
            for num, tipo, nombre in opciones_disponibles:
                if opcion == num:
                    minijuego_seleccionado = tipo
                    break
            
            if minijuego_seleccionado:
                break
            else:
                print("Opción inválida. Intenta de nuevo.")
        
        exitoso = self.ejecutar_minijuego_especifico(minijuego_seleccionado)
        
        if exitoso:
            print("🎉 ¡Excelente! Minijuego completado.")
            print("🎁 Recuperas una vida extra!")
            self.minijuegos_completados.add(minijuego_seleccionado)
            self.vidas = min(self.vidas + 1, self.vidas_maximas)
            self.jugador.llaves += 1
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