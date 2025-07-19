# NPCs y enemigos


class NPC:
    def __init__(self, nombre, x, y, dialogo, presentacion):
        self.nombre = nombre
        self.x = x
        self.y = y
        self.dialogo = dialogo
        self.presentacion = presentacion
        self.acertijo_resuelto = False


    # solamente para presentarse.
    def presentarse(self):
        print(f"{self.nombre}: {self.presentacion}")
        if isinstance(self.presentacion, list):
            for frase in self.presentacion:
                print(frase)
        else:
            print(self.presentacion)    
            
    # Funcion de acertijo con el los dialogos y esperando la respuestas correctas
    def acertijo(self):
        if self.acertijo_resuelto:
            print(f"{self.nombre}: Lo resolviste, Toma")
            return
        
        print(f"{self.nombre}: Responde correctamente.")

        for pregunta, respuesta_acertada in self.dialogo.item():
            print(f"{self.nombre}: {pregunta}")
            respuesta = input("Tu respuesta: ").strip().lower()
            if respuesta_acertada == respuesta:
                print("ok")
            else:
                print(f"{self.nombre}: malmal bro")
                return
            
            
    def entregar_llave(self):

        pass

