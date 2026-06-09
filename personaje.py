import pygame

class Personaje:
    def __init__(self):
        self.x = 400
        self.y = 200    #Posicion del personaje

        self.ancho = 50     #Tamaño del personaje
        self.alto = 50    

        self.velocidad_movimiento = 1
        
    
    
    def mover(self):
        teclas = pygame.key.get_pressed()

        if teclas[pygame.K_a]:
            self.x -= self.velocidad_movimiento

        if teclas[pygame.K_d]:
            self.x += self.velocidad_movimiento


    def dibujar(self, pantalla):
        pygame.draw.rect(pantalla,(255,0,0),      #En donde voy a dibujar y su color(255,0,0) es rojo
        (self.x, self.y, self.ancho, self.alto))    #Parametros del personaje

    




pygame.init()

pantalla = pygame.display.set_mode((800, 600))

personaje = Personaje()

corriendo = True

while corriendo:

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

    pantalla.fill((0,0,0))

    personaje.mover()
    personaje.dibujar(pantalla)


    pygame.display.flip()

pygame.quit()