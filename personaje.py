import pygame

class Personaje:
    def __init__(self):
        
        #Parametros de imagen
        
        self.x = 683
        self.y = 100    #Posicion del personaje

        self.ancho = 120     #Tamaño del personaje
        self.alto = 120    

            
        #Ponemos la imagen del personaje
        
        self.imagen_frente = pygame.image.load("assets/personaje_de_frente.png")
        self.imagen_frente = pygame.transform.scale(self.imagen_frente,(self.ancho, self.alto)) #Ajustamos medida Cualquiera cosa cambiar ancho y alto

        self.imagen_derecha = pygame.image.load("assets/personaje_de_costado.png")
        self.imagen_derecha = pygame.transform.scale(self.imagen_derecha,(self.ancho, self.alto))
        
        self.imagen_izquierda = pygame.transform.flip(self.imagen_derecha,True,False)

        
        self.estado_imagen = "frente"

        self.tiempo_quieto = 0

        #Mecanicas velocidades etc

        self.velocidad_x = 0.0

        self.velocidad_movimiento = 1
        
        self.velocidad_maxima = 15
        
        self.velocidad_y = 0
        
        self.fuerza_salto = -20 #Altura alcanzada               
        
        self.fuerza_salto_int = -25
        
        self.fuerza_salto_max = -35 #Altura maxima alcanzada con velocidad

        self.en_suelo = True #Condicion para no poder volvar
    
        self.rect = True #Esto hablarlo con franco (PLATAFORMAS)
    
    def limitar_movimiento(self, ancho_pantalla):
        pass
    
    def gravedad(self):
        self.velocidad_y += 1

    def actualizar_pos(self):
        self.y += self.velocidad_y
        
        if self.y > 658:
            
            self.y = 658        #PISO (por asi decirlo)
            self.velocidad_y = 0
            self.en_suelo = True
        
        self.x += self.velocidad_x
        if self.velocidad_x > 0:
            self.velocidad_x -= 0.5   #Friccion

        elif self.velocidad_x < 0:
            self.velocidad_x += 0.5 
    
    def saltar(self):
        if abs(self.velocidad_x) >= 13:                      #Si va mas rapido salta mas alto
            self.velocidad_y = self.fuerza_salto_max    
            self.en_suelo = False
        elif abs(self.velocidad_x) >= 7:
            self.velocidad_y = self.fuerza_salto_int   #Velocidad de salto (En algun momento tiene que disminuir)
            self.en_suelo = False
        else:
            self.velocidad_y = self.fuerza_salto
            self.en_suelo = False                       #Llamo saltar desde mover

    def mover(self):
        teclas = pygame.key.get_pressed()

        if teclas[pygame.K_a]:
            
            #Movimiento horizontal
            
            if self.velocidad_x > -self.velocidad_maxima:
                self.velocidad_x -= self.velocidad_movimiento
            
            self.estado_imagen = "izquierda"        #Para la imagen
            self.tiempo_quieto = 8
        
        elif teclas[pygame.K_d]:
            if self.velocidad_x < self.velocidad_maxima:
                self.velocidad_x += self.velocidad_movimiento
            
            self.estado_imagen = "derecha"
            self.tiempo_quieto = 8
        
        else:
                if self.tiempo_quieto > 0:
                    self.tiempo_quieto -= 1
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

pantalla = pygame.display.set_mode((1366, 768))  #Resolucion del juego

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