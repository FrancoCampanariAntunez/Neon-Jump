import pygame  
import random  

from pygame.examples.stars import move_stars  # importa ejemplo de pygame (no se usa en este código)

from personaje import Personaje

from plataformas import *

from gameover import GameOver


pygame.init()
#Creacion de la ventana
ANCHO = 1366
ALTO = 768
screen = pygame.display.set_mode((ANCHO, ALTO))
en_menu = True
clock = pygame.time.Clock()

mostrar_hitbox = False

pygame.mixer.init()

from menu import *


pygame.mixer.music.load("sonido/musicaintro3.mp3")
pygame.mixer.music.set_volume(0.0)  # volumen (0.0 a 1.0)
pygame.mixer.music.play(-1)  # -1 = loop infinito

fondo = pygame.image.load("imagenes\ciudad.WEBP")
# Ajusta el fondo al tamaño de la ventana
fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))
# Carga la imagen de la plataforma conservando la transparencia
imagen_plataforma = pygame.image.load("imagenes\plataforma.png").convert_alpha()
imagen_plataforma2 = pygame.image.load("imagenes\plataforma2.png").convert_alpha()

#Estas 2 lineas son para que la imagen de la plataforma se ajuste a la hitbox de la plataforma
rect_real = imagen_plataforma.get_bounding_rect()
imagen_plataforma = imagen_plataforma.subsurface(rect_real).copy()

imagen_piso = pygame.image.load("imagenes\piso.png")
# Ajusta la imagen del piso al ancho de la pantalla
imagen_piso = pygame.transform.scale(imagen_piso, (ANCHO, 40))

# CARRILES (para la generacion de plataformas)
# Posiciones posibles en X donde pueden aparecer las plataformas
carriles = [100, 250, 400, 550, 700, 850, 1000]

# PLATAFORMAS
#Lista donde se almacenaran las plataformas generadas
plataformas = []

ultima_y = ALTO - 40 - 50

font = pygame.font.Font("fuentes/Orbitron Medium 500.ttf", 30)

piso = Piso(0,ALTO - 40,ANCHO,40,imagen_piso)

altura_max = 0

for i in range(10):
    nueva, ultima_y = generar_plataformas(
        ultima_y,
        ANCHO,
        carriles,
        plataformas,
        altura_max,
        imagen_plataforma,
        imagen_plataforma2
    )
    plataformas.append(nueva)



player = Personaje()

game_over = GameOver()

altura_inicial = player.rect.y - 40

altura_max = 0
puntos = 0

class Offset:
    def __init__(self):
        self.x = 0
        self.y = 0

offset = Offset()
# -----------------------------------------------------------------------------------------------------------------------
corriendo = True

camara_activa = False


def reiniciar_juego():
    global player
    global plataformas
    global ultima_y
    global altura_max
    global altura_inicial
    global puntos
    global offset
    global camara_activa
    global game_over
    global piso

    player = Personaje()

    plataformas = []

    ultima_y = ALTO - 40 - 50

    altura_max = 0
    puntos = 0

    altura_inicial = player.rect.y - 40

    offset.x = 0
    offset.y = 0

    piso = Piso(0, ALTO - 40, ANCHO, 40, imagen_piso)
    
    camara_activa = False


    game_over.activo = False

    for i in range(10):
        nueva, ultima_y = generar_plataformas(
            ultima_y,
            ANCHO,
            carriles,
            plataformas,
            altura_max,
            imagen_plataforma,
            imagen_plataforma2
        )
        plataformas.append(nueva)
    
    pygame.mixer.music.stop()
    pygame.mixer.music.play(-1)
while corriendo:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            corriendo = False

        if en_menu:
            accion = actualizar_menu(event)

            if accion == "JUGAR":
                en_menu = False

            elif accion == "SALIR":
                corriendo = False
                
                pygame.mixer.music.load("musica/cancionfondo.mp3")
                pygame.mixer.music.set_volume(0.1)
                pygame.mixer.music.play(-1)
                
                en_menu = False

    if en_menu:

        dibujar_menu(screen)

        pygame.display.flip()
        clock.tick(60)

        continue
    
    
    screen.fill((0,0,0))
    screen.blit(fondo,(0,0))

    if game_over.activo:
        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_RETURN:
                reiniciar_juego()
            
            elif event.key == pygame.K_ESCAPE:
                reiniciar_juego()
                en_menu = True
        
        game_over.dibujar(screen, ANCHO, ALTO, puntos)

        pygame.display.flip()
        clock.tick(60)
        
        continue

    # Movimiento
    player.mover()

    if not player.en_suelo:
        player.gravedad()

    player.actualizar_pos()
    player.limitar_movimiento(ANCHO)

    # Por defecto suponemos que NO está apoyado
    player.en_suelo = False

    # ---------- COLISIONES CON PLATAFORMAS ----------
    for plataforma in plataformas:

        if (
            player.velocidad_y >= 0 and
            player.rect.bottom >= plataforma.rect.top and
            player.rect.bottom <= plataforma.rect.top + 20 and
            player.rect.right > plataforma.rect.left and
            player.rect.left < plataforma.rect.right
        ):

            player.rect.bottom = plataforma.rect.top
            player.y = player.rect.y - player.offset_y

            player.rect.topleft = (
                player.x + player.offset_x,
                player.y + player.offset_y
            )

            player.velocidad_y = 0
            player.en_suelo = True

            break

    # ---------- PISO ----------
    if not player.en_suelo:

        if player.rect.bottom >= piso.rect.top:

            player.rect.bottom = piso.rect.top
            player.y = player.rect.y - player.offset_y

            player.rect.topleft = (
                player.x + player.offset_x,
                player.y + player.offset_y
            )

            player.velocidad_y = 0
            player.en_suelo = True

    altura_actual = max(0, altura_inicial - player.rect.y)
    altura_max = max(altura_max, altura_actual)

    puntos = int(altura_max / 10)

    # ---------------- CAMARA ----------------

    # activar cámara cuando el jugador empieza a subir
    if player.rect.top < ALTO * 0.6:
     camara_activa = True

    # posición inicial fija
    if not camara_activa:
     offset.y = 0

    else:
     # velocidad base muy lenta al inicio
     velocidad_actual = 0.5 + (altura_max / 5000)
     velocidad_actual = min(velocidad_actual, 3)

     # suavizado extra
     velocidad_actual = velocidad_actual * 0.8 + 0.6

     # límite máximo
     velocidad_actual = min(6, velocidad_actual)

     offset.y -= velocidad_actual

     # posición del jugador en el mundo (NO pantalla)
     posicion_relativa = player.y - offset.y

     objetivo = ALTO * 0.2

     if posicion_relativa < objetivo:
        offset.y -= (objetivo - posicion_relativa) * 0.05

    #----------Game over---------------
    if player.rect.top - offset.y > ALTO:
        game_over.activar()

    # Eliminar plataformas viejas
    for plataforma in plataformas[:]:
     if plataforma.rect.top > offset.y + ALTO + 500:
        plataformas.remove(plataforma)

    # Generar plataformas nuevas
    while ultima_y > offset.y - 3000:
        nueva, ultima_y = generar_plataformas(
        ultima_y,
        ANCHO,
        carriles,
        plataformas,
        altura_max,
        imagen_plataforma,
        imagen_plataforma2
    )
        plataformas.append(nueva)


    for plataforma in plataformas:
        plataforma.dibujar(screen, offset)

    piso.dibujar(screen, offset)
    player.dibujar(screen, offset)

    texto = font.render(f"Puntos: {puntos}", True, (255, 255, 255))
    screen.blit(texto, (20, 20))

    pygame.display.flip()
    clock.tick(60)

   