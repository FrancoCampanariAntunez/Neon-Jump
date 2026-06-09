import pygame

class Personaje:
    def __init__(self):
        self.x = 400
        self.y = 100    #Posicion del personaje

        self.ancho = 120     #Tamaño del personaje
        self.alto = 120    

        self.velocidad_movimiento = 10
        self.velocidad_y = 0
        
        self.fuerza_salto = -15 #Velocidad de salto

        self.imagen = pygame.image.load("assets/personaje.png.png")                 #Ponemos la imagen del personaje
        self.imagen = pygame.transform.scale(self.imagen,(self.ancho, self.alto))   #Ajustamos medida Cualquiera cosa cambiar ancho y alto

        self.en_suelo = True #Condicion para no poder volvar
    
        self.rect = True #Esto hablarlo con franco
    
    def limitar_movimiento(self, ancho_pantalla):
        pass
    
    def gravedad(self):
        self.velocidad_y += 1
        

    def actualizar_pos(self):
        self.y += self.velocidad_y
        if self.y > 490:
            self.y = 490        #PISO (por asi decirlo)
            self.velocidad_y = 0
            self.en_suelo = True

    def saltar(self):
        self.velocidad_y = self.fuerza_salto #Velocidad de salto (En algun momento tiene que disminuir)
        self.en_suelo = False

    def mover(self):
        teclas = pygame.key.get_pressed()

        if teclas[pygame.K_a]:
            self.x -= self.velocidad_movimiento #Movimiento horizontal

        if teclas[pygame.K_d]:
            self.x += self.velocidad_movimiento

        if teclas[pygame.K_SPACE] and self.en_suelo == True:
            self.saltar()


    def dibujar(self, pantalla):
        pantalla.blit(self.imagen,      #Insertamos personaje
        (self.x, self.y, self.ancho, self.alto))    #Parametros del personaje

    




pygame.init()

clock = pygame.time.Clock()

pantalla = pygame.display.set_mode((800, 600))  #Resolucion del juego

personaje = Personaje()

corriendo = True

while corriendo:

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

    pantalla.fill((0,0,0))

    personaje.mover()
    personaje.gravedad()
    personaje.actualizar_pos()
    personaje.dibujar(pantalla)


    pygame.display.flip()
    clock.tick(60)      #FPS LIMIT

pygame.quit()