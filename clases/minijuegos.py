# Mini-juegos
import time
import os

class MiniJuegos:
    def __init__(self):
        self.puntaje_total = 0

    def limpiar_pantalla(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def juego_codigo_secreto(self):
        print(' Nivel 1: Código Secreto')
        print('Tenes que decifrar\nSi G=7, U=21, E=5, R=18, A=1 ¿Cuál es la suma del valor de las letras en la palabra ‘GUERRA’?\n(Pista: suma los valores de cada letra segun A=1, B=2, C=3)')
        print("a) 70\nb) 65\nc) 73")
        ingreso = input('Tu respuesta: ').lower()
        if ingreso == 'a':
            print('Correcto')
            self.puntaje_total += 1
            return True
        else:
            print('Incorrecto fin del juego')
            return False

    def juego_numerico_magico(self):
        print('\n Nivel 2: numero magico')
        numero_secreto = 7
        intentos_maximos = 3
        intentos_usados = 0

        while intentos_usados < intentos_maximos:
            try:
                intento = int(input('Estas en guerra, y tenes que salvar tu base. Desconecta la bomba adivinando el nuero de cable a desconectar. (de 1 al 10)'))
            except ValueError:
                print('Por favor ingresa el numero valido')
                continue

            if intento == numero_secreto:
                print('adivinaste')
                self.puntaje_total += 1
                return True
            elif intento > numero_secreto:
                print('el numero es mas chicos')
            else:
                print(' el numero es mas grande')

            intentos_usados += 1

        print(f' Te quedaste sin intentos. El numero era {numero_secreto}\n Fin del juego.')
        return False

    def juego_memoria_visual(self):
        print('\n Nivel 3: Memoria Visual')
        palabras = ['tanque', 'misil', 'avion', 'radar', 'trinchera']
        print('memoriza estas palabras')
        print(palabras)
        time.sleep(4)
        self.limpiar_pantalla()

        print(' Escribí las palabras que recordas (una por una). Escribí "fin" para terminar.')
        palabras_recordadas = []
        while True:
            palabra = input('Palabra: ').strip().lower()
            if palabra == 'fin':
                break
            palabras_recordadas.append(palabra)

        puntaje = sum(1 for palabra in palabras_recordadas if palabra in palabras)
        self.puntaje_total += puntaje

        print(f' Palabras correctas: {puntaje} de {len(palabras)}')
        if puntaje >= 3:
            print(' ganaste')
            return True
        else:
            print(' No recordaste suficientes palabras. Fin del juego.')
            return False

    def jugar(self):
        print(' Bienvenido al Juego de los 3 Niveles\n')

        if not self.juego_codigo_secreto():
            return
        if not self.juego_numerico_magico():
            return
        if not self.juego_memoria_visual():
            return

        print(f'\n  Completaste todos los niveles con {self.puntaje_total} puntos.')


if __name__ == "__main__":
    juego = MiniJuegos()
    juego.jugar()
