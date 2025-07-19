

# main.py
# --------Aca inicia todo el juego-------- #


#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🎮 GUERRA POSAPOCALÍPTICA: PARAGUAY VS URSS
🧨 Un juego de supervivencia en consola con mapas de 30x30

Autor: [Tu nombre]
Fecha: Julio 2025
"""

import os
import sys
from clases.juego import Juego

def limpiar_pantalla():
    """Limpia la pantalla según el sistema operativo"""
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_intro():
    """Muestra la introducción épica del juego"""
    limpiar_pantalla()
    
    intro = """
    ╔═══════════════════════════════════════════════════════════════╗
    ║                    🧨 GUERRA POSAPOCALÍPTICA 🧨                ║
    ║                                                               ║
    ║          Paraguay vs URSS - El Fin del Mundo ha llegado      ║
    ║                                                               ║
    ║  🏙️ Asunción está en ruinas...                                ║
    ║  ☢️  La radiación se extiende por todo el continente...      ║
    ║  🔥 Solo los más valientes sobrevivirán...                   ║
    ║                                                               ║
    ║  Tu misión: Conseguir las 3 llaves sagradas y escapar        ║
    ║  del laberinto final antes de que sea demasiado tarde.       ║
    ║                                                               ║
    ║                    ¡La supervivencia está en tus manos!      ║
    ╚═══════════════════════════════════════════════════════════════╝
    
    🎮 CONTROLES:
    • W/A/S/D - Movimiento
    • E - Interactuar con NPCs
    • Q - Salir del juego
    
    💡 TIP: Acércate a los NPCs (🤖) para recibir misiones e información.
    
    """
    print(intro)
    input("Presiona ENTER para comenzar tu aventura... ")

def mostrar_creditos():
    """Muestra los créditos finales"""
    limpiar_pantalla()
    creditos = """
    ╔═══════════════════════════════════════════════════════════════╗
    ║                         🏆 ¡FELICITACIONES! 🏆                ║
    ║                                                               ║
    ║        Has sobrevivido al apocalipsis y salvado Paraguay      ║
    ║                                                               ║
    ║                    🎖️  ERES UN HÉROE  🎖️                     ║
    ║                                                               ║
    ║                         Créditos del Juego:                  ║
    ║                    Desarrollado en Python 🐍                 ║
    ║                     Hackathon - Julio 2025                   ║
    ║                                                               ║
    ║            Gracias por jugar Guerra Posapocalíptica           ║
    ╚═══════════════════════════════════════════════════════════════╝
    """
    print(creditos)
    input("\nPresiona ENTER para salir...")

def main():
    """Función principal del juego"""
    try:
        # Mostrar introducción
        mostrar_intro()
        
        # Crear instancia del juego
        juego = Juego()
        
        print("🎯 Inicializando el mundo posapocalíptico...")
        print("⚡ Cargando escenarios de destrucción...")
        print("🤖 Activando NPCs supervivientes...")
        
        input("\nPresiona ENTER cuando estés listo para empezar...")
        
        # Ejecutar el bucle principal del juego
        resultado = juego.ejecutar()
        
        # Mostrar resultado final
        limpiar_pantalla()
        
        if resultado == "victoria":
            print("🎉 ¡VICTORIA! Has completado tu misión y salvado Paraguay del apocalipsis.")
            mostrar_creditos()
            
        elif resultado == "derrota":
            print("💀 GAME OVER - Has perdido todas tus vidas en el apocalipsis...")
            print("🔄 El mundo ha caído en la oscuridad eterna.")
            print("\n💡 TIP: ¡Inténtalo de nuevo! La práctica hace al maestro.")
            
        elif resultado == "abandono":
            print("🚪 Has abandonado la misión...")
            print("🌍 El destino del mundo queda en el aire...")
            
        else:
            print("🤔 Final inesperado... ¿Qué habrá pasado?")
            
    except KeyboardInterrupt:
        print("\n\n🛑 Juego interrumpido por el usuario.")
        print("👋 ¡Nos vemos en el próximo apocalipsis!")
        
    except Exception as e:
        print(f"\n❌ Error crítico en el sistema: {e}")
        print("🔧 Contacta al desarrollador si el problema persiste.")
        
    finally:
        print("\n🎮 Gracias por jugar Guerra Posapocalíptica.")
        print("📧 ¿Feedback? ¡Comparte tu experiencia!")

if __name__ == "__main__":
    main()


