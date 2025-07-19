# NPCs y enemigos
# NPCs y enemigos

class NPC:
    def __init__(self, nombre, dialogo, presentacion):
        self.nombre = nombre
        self.dialogo = dialogo  # diccionario: {pregunta: respuesta, pregunta: respuesta}
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
            print(f"{self.nombre}: Ya resolviste. Bien hecho! continua...")
            return
        
        print(f"{self.nombre}: Responde correctamente...")
        for pregunta, respuesta_acertada in self.dialogo.items():
            print(f"{self.nombre}: {pregunta}")
            respuesta = input("Tu respuesta: ").strip().lower()
            if respuesta_acertada == respuesta:
                print(f"{self.nombre}: Correcto")
            else:
                print(f"{self.nombre}: malmal bro")
                return
        print(f"{self.nombre}: Muy bien! Has superado el desafio.")
        self.acertijo_resuelto = True