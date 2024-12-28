import pygame

class Pong:

    def ___init__(self):      #un constructor
        pygame.init()
        self.pantalla = pygame.display.set_mode((800, 600))


    def jugar(self):           # Bucle principal 
        salir = False
        cont = 0 
        while not salir:
            # bucle principal (main loop)
            cont = cont+1
            print(cont)
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    print('Se ha cerrado la ventana')
                    salir = True
                
                print('Se ha producido un evento del tipo:', evento)

            # renderizar mis objetos
            
            
            # En la linea de arriba los 3 numeros son los 3 colores rojo, verde y azul  que da la pantalla de ordenador.
            # eliges que cantidad de cada uno dar RGB  Red94 , Green68, BLue158 
            
            # 1. borrar la pantalla
            pygame.draw.rect(self.pantalla, (0,0,0), ((0,0), (800, 600)))

            # 2. pitar los objetos en su nueva posicion
            
            rectangulo = pygame.Rect(50, 50, 300, 150)  # Aqui elijo la posicion de la pantalla pixeles
            pygame.draw.rect(self.pantalla, (cont % 94, 68, 158), rectangulo)   # aqui los colores

            # mostrar los cambios en la pantalla
            pygame.display.flip()

        

        pygame.quit()


if __name__ == '__main__':      # Ejecutar desde linea de comandos
    juego = Pong()
    juego.jugar()







    