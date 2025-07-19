# minijuegos.py


import time
import os

class MiniJuegos:
    def __init__(self):
        self.puntaje_total = 0

    def limpiar_pantalla(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def juego_codigo_secreto(self):
        print('🔐 Nivel 1: Código Secreto')
        print('Tenes que decifrar')
        print('Si G=7, U=21, E=5, R=18, A=1 ¿Cuál es la suma del valor de las letras en la palabra \'GUERRA\'?')
        print('(Pista: suma los valores de cada letra segun A=1, B=2, C=3)')
        print("a) 70\nb) 65\nc) 73")

        while True:
            ingreso = input('Tu respuesta: ').lower()
            if ingreso not in ['a', 'b', 'c']:
                print('tenes que ingresar ( A, B, o C )')
                continue
            elif ingreso == 'a':
                print('🎉 ¡Correcto!')
                self.puntaje_total += 1
                return True
            else:
                print('❌ Incorrecto - fin del juego')
                return False

    def juego_numerico_magico(self):
        print('\n🎯 Nivel 2: Numero Magico')
        numero_secreto = 7
        intentos_maximos = 5
        intentos_usados = 0

        print('Estas en guerra, y tenes que salvar tu base.')
        print('Desconecta la bomba adivinando el numero de cable a desconectar.')

        while intentos_usados < intentos_maximos:
            try:
                intento = int(input(f'Ingresa un numero del 1 al 10 (intento {intentos_usados + 1}/{intentos_maximos}): '))
                if intento < 1 or intento > 10:
                    print('El numero debe estar entre 1 y 10')
                    continue
            except ValueError:
                print('Por favor ingresa un numero valido')
                continue

            if intento == numero_secreto:
                print('🎉 ¡Adivinaste! Bomba desactivada.')
                self.puntaje_total += 1
                return True
            elif intento > numero_secreto:
                print('🔽 El numero es mas chico')
            else:
                print('🔼 El numero es mas grande')

            intentos_usados += 1

        print(f'💥 Te quedaste sin intentos. El numero era {numero_secreto}')
        print('La bomba exploto... Fin del juego.')
        return False

    def juego_memoria_visual(self):
        print('\n🧠 Nivel 3: Memoria Visual')
        palabras = ['tanque', 'misil', 'avion', 'radar', 'trinchera']

        print('Memoriza estas palabras de guerra:')
        print('📝 ' + ' | '.join(palabras))
        print('\nTienes 5 segundos para memorizarlas...')

        for i in range(5, 0, -1):
            print(f'⏰ {i}...')
            time.sleep(1)

        self.limpiar_pantalla()

        print('🎯 Escribí las palabras que recordas (una por una).')
        print('📝 Escribí "fin" cuando termines.')

        palabras_recordadas = []
        while True:
            palabra = input('Palabra: ').strip().lower()
            if palabra == 'fin':
                break
            if palabra not in palabras_recordadas:  # Evitar duplicados
                palabras_recordadas.append(palabra)

        puntaje = sum(1 for palabra in palabras_recordadas if palabra in palabras)
        self.puntaje_total += puntaje

        print(f'\n📊 Palabras correctas: {puntaje} de {len(palabras)}')
        print(f'📝 Recordaste: {", ".join(palabras_recordadas)}')
        print(f'✅ Correctas: {[p for p in palabras_recordadas if p in palabras]}')

        if puntaje >= 3:
            print('🎉 ¡Ganaste! Excelente memoria.')
            return True
        else:
            print('❌ No recordaste suficientes palabras. Fin del juego.')
            return False