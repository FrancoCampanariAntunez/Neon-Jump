import pygame

class Personaje:
    def __init__(self):
        
        #Parametros de imagen
        
        self.x = 620
        self.y = 678    #Posicion del personaje #spawn

        self.ancho = 100     #Tamaño del personaje
        self.alto = 100
  
        #Ponemos la imagen del personaje
        
        self.caminar_derecha = [
        pygame.image.load("assets/caminar_1.png"),
        pygame.image.load("assets/caminar_2.png"),
        pygame.image.load("assets/caminar_3.png")
        ]

        for i in range(len(self.caminar_derecha)):              #Reduzco lineas de codigo con un for
            self.caminar_derecha[i] = pygame.transform.scale( 
            self.caminar_derecha[i],
            (self.ancho, self.alto)
            )

        self.caminar_izquierda = []
        
        for imagen in self.caminar_derecha:
            self.caminar_izquierda.append(
            pygame.transform.flip(imagen, True, False)
            )
        
        self.imagen_frente = pygame.image.load("assets/personaje_de_frente.png")
        self.imagen_frente = pygame.transform.scale(self.imagen_frente,(self.ancho, self.alto)) #Ajustamos medida Cualquiera cosa cambiar ancho y alto


        self.imagen_animacion_salto = pygame.image.load("assets/personaje_estrella_salto.png")
        self.imagen_animacion_salto = pygame.transform.scale(self.imagen_animacion_salto,(self.ancho, self.alto))
        
        self.estado_imagen = "frente"

        self.tiempo_quieto = 0

        self.frame_actual = 0               #Para caminar animacion
        
        self.contador_animacion = 0   # contador_animacion funciona como un temporizador.
        # Evita que la animación cambie de imagen demasiado rápido.
        
        #Animacion para el super salto

        self.animacion_salto = False

        self.angulo = 0

        self.velocidad_giro = 20

        #Mecanicas velocidades etc

        self.velocidad_x = 0.0

        self.velocidad_movimiento = 1
        
        self.velocidad_maxima = 15
        
        self.velocidad_y = 0
        
        self.fuerza_salto = -20 #Altura alcanzada               
        
        self.fuerza_salto_int = -25
        
        self.fuerza_salto_max = -30 #Altura maxima alcanzada con velocidad

        self.en_suelo = True #Condicion para no poder volvar
    
        # Desplazamiento de la hitbox respecto de la imagen
        self.offset_x = 42
        self.offset_y = 10                                 # catalano

        # Hitbox del personaje
        self.rect = pygame.Rect(self.x + self.offset_x,self.y + self.offset_y,45,100) # catalano
    
    def limitar_movimiento(self, ancho_pantalla):
        if  self.x <-21:
            self.x = -21
            self.velocidad_x = 0

    # Limite derecho
        elif self.x > ancho_pantalla - self.ancho:
             self.x = ancho_pantalla - self.ancho
             self.velocidad_x = 0
    
    def gravedad(self):
        self.velocidad_y += 0.8

    def actualizar_pos(self):
        self.y += self.velocidad_y
        
        if self.y > 678:
            
            self.y = 678        #PISO (por asi decirlo)
            self.velocidad_y = 0
            self.en_suelo = True       #todo esto esta comentado para que tome como piso original el piso de las plataformas (catalano)
        
        self.x += self.velocidad_x
        if self.velocidad_x > 0:
            self.velocidad_x -= 0.5   #Friccion

        elif self.velocidad_x < 0:
            self.velocidad_x += 0.5 

        # Actualizar la hitbox
        self.rect.topleft = (self.x + self.offset_x,self.y + self.offset_y) # catalano

        if self.animacion_salto == True:
                 
            if not self.en_suelo:
                self.angulo = (self.angulo + self.velocidad_giro) % 360

            else:
                self.animacion_salto = False
                self.angulo = 0

    
    def saltar(self):
        if abs(self.velocidad_x) >= 13:                      #Si va mas rapido salta mas alto
            self.velocidad_y = self.fuerza_salto_max    
            
            self.animacion_salto = True  #Animacion para el salto
            
            self.angulo = 0
            
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
            
            self.contador_animacion += 1

            if self.contador_animacion >= 6:           #Para la animacion de caminar
                self.contador_animacion = 0
                self.frame_actual += 1

            if self.frame_actual >= 3:
                self.frame_actual = 0
        
        elif teclas[pygame.K_d]:
            if self.velocidad_x < self.velocidad_maxima:
                self.velocidad_x += self.velocidad_movimiento
            
            self.estado_imagen = "derecha"                      #Delay para la imagen de cuando queda de frente
            self.tiempo_quieto = 8

            self.contador_animacion += 1
            
            if self.contador_animacion >= 6:                   #Para la animacion de caminar
                self.contador_animacion = 0
                self.frame_actual += 1

            if self.frame_actual >= 3:
                self.frame_actual = 0


        else:
                if self.tiempo_quieto > 0:
                    self.tiempo_quieto -= 1
                else:
                    self.estado_imagen = "frente"
                    self.frame_actual = 0
                    self.contador_animacion = 0
        
        if teclas[pygame.K_SPACE] and self.en_suelo == True:
            self.saltar()


    def dibujar(self, pantalla, offset=None):

            if offset is None:
                pos_pantalla = (self.x, self.y)
        
            else:
                pos_pantalla = (
                self.x - offset.x,
                self.y - offset.y
            )
        
            if self.animacion_salto:

                imagen_rotada = pygame.transform.rotate(         #Para animacion salto rota la imagen
                self.imagen_animacion_salto,
                self.angulo                                                    #Rota la imagen con el angulo que va rotando
                )

                rect = imagen_rotada.get_rect(
                center=(
                pos_pantalla[0] + self.ancho // 2,
                pos_pantalla[1] + self.alto // 2
                )
                )

                pantalla.blit(imagen_rotada, rect.topleft)

                return
        
            if self.estado_imagen == "frente":
                pantalla.blit(self.imagen_frente,pos_pantalla    
                )      #Dibujamos con condicion 
       
            elif self.estado_imagen == "derecha":
                pantalla.blit(
                self.caminar_derecha[self.frame_actual],
                pos_pantalla
                )
            else:
                pantalla.blit(
                self.caminar_izquierda[self.frame_actual],
                pos_pantalla
                )

            #Dibujar la hitbox si mostrar_hitbox=True
            if mostrar_hitbox:
                pygame.draw.rect(pantalla, (0, 255, 0), self.rect, 2) # catalano
    




pygame.init()

clock = pygame.time.Clock()

pantalla = pygame.display.set_mode((1366, 768))  #Resolucion del juego

personaje = Personaje()

mostrar_hitbox = False

corriendo = True

while corriendo:

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

    pantalla.fill((0,0,0))

    personaje.mover()
    personaje.gravedad()
    personaje.actualizar_pos()
    personaje.limitar_movimiento(1386)
    personaje.dibujar(pantalla)


    pygame.display.flip()
    clock.tick(60)      #FPS LIMIT

pygame.quit()