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
        
        #Ponemos la imagen del personaje
        
        self.imagen_frente = pygame.image.load("assets/personaje_de_frente.png")
        self.imagen_frente = pygame.transform.scale(self.imagen_frente,(self.ancho, self.alto)) #Ajustamos medida Cualquiera cosa cambiar ancho y alto

        self.imagen_derecha = pygame.image.load("assets/personaje_de_costado.png")
        self.imagen_derecha = pygame.transform.scale(self.imagen_derecha,(self.ancho, self.alto))
        
        self.imagen_izquierda = pygame.transform.flip(self.imagen_derecha,True,False)
        self.imagen_izquierda = pygame.transform.scale(self.imagen_izquierda,(self.ancho, self.alto))
        
        self.estado_imagen = "frente"

        self.en_suelo = True #Condicion para no poder volvar
    
        self.rect = True #Esto hablarlo con franco (PLATAFORMAS)
    
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
        self.velocidad_y = self.fuerza_salto    #Velocidad de salto (En algun momento tiene que disminuir)
        self.en_suelo = False

    def mover(self):
        teclas = pygame.key.get_pressed()

        if teclas[pygame.K_a]:
            self.x -= self.velocidad_movimiento     #Movimiento horizontal
            self.estado_imagen = "izquierda"
        
        elif teclas[pygame.K_d]:
            self.x += self.velocidad_movimiento
            self.estado_imagen = "derecha"
        
        else:
            self.estado_imagen = "frente"
        
        if teclas[pygame.K_SPACE] and self.en_suelo == True:
            self.saltar()


    def dibujar(self, pantalla):
        if self.estado_imagen == "frente":
            pantalla.blit(self.imagen_frente,      
            (self.x, self.y, self.ancho, self.alto))           #Dibujamos con condicion 
        elif self.estado_imagen == "derecha":
            pantalla.blit(self.imagen_derecha,      
            (self.x, self.y, self.ancho, self.alto))
        else:
            pantalla.blit(self.imagen_izquierda,      
            (self.x, self.y, self.ancho, self.alto))

    




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