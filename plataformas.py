import pygame  
import random  

from pygame.examples.stars import move_stars  # importa ejemplo de pygame (no se usa en este código)

from personaje import Personaje


class Plataforma:
    def __init__(self, x, y, ancho, alto, tipo="normal",
                 img_normal=None, img_nivel=None):

        ajuste_y = 20  # ajuste vertical para alinear mejor la hitbox con la imagen

        self.rect = pygame.Rect(  # crea la hitbox de la plataforma
            x,
            y + ajuste_y,  # desplaza la hitbox hacia abajo para ajustarla visualmente
            ancho,
            alto - ajuste_y  # reduce altura de la hitbox respecto a la imagen
        )

        if tipo == "nivel":  # si la plataforma es de tipo nivel
            img = img_nivel  # usa imagen de nivel
        else:
            img = img_normal  # si no, usa imagen normal

        self.imagen = pygame.transform.scale(img, (ancho, alto))  # escala la imagen al tamaño de la plataforma

        # Guardar dónde dibujar la imagen
        self.x_imagen = x  # guarda posición X de dibujo
        self.y_imagen = y  # guarda posición Y de dibujo

    def dibujar(self, pantalla, offset):

        pos_pantalla = (self.x_imagen - offset.x, self.y_imagen - offset.y)  # aplica cámara (offset)
        pantalla.blit(self.imagen, pos_pantalla)  # dibuja la imagen en pantalla
        
        if mostrar_hitbox:  # si está activado el debug de hitbox
            pygame.draw.rect(pantalla, (255, 0, 0), self.rect, 2)  # dibuja contorno rojo de la colisión


class Piso:
    def __init__(self, x, y, ancho, alto, imagen):
        self.imagen = pygame.transform.scale(imagen, (ancho, alto))  # escala la imagen del piso
        self.rect = pygame.Rect(x, y, ancho, alto)  # crea la hitbox del piso
        self.x_imagen = x  # guarda posición X de dibujo
        self.y_imagen = y  # guarda posición Y de dibujo

        # Reemplaza la imagen heredada por la imagen específica del piso
        self.imagen = pygame.transform.scale(imagen, (ancho, alto))  # vuelve a escalar la imagen (redundante)

    def dibujar(self, pantalla, offset):

        pos_pantalla = (self.x_imagen - offset.x, self.y_imagen - offset.y)  # aplica desplazamiento de cámara
        # Muestra en pantalla la imagen del piso
        pantalla.blit(self.imagen, pos_pantalla)  # dibuja el piso
        
        # Lo mismo que antes para la hitbox
        if mostrar_hitbox:  # si está activado debug
            pygame.draw.rect(pantalla, (255, 0, 0), self.rect, 2)  # dibuja hitbox en rojo


def dificultad_por_altura(y):
    # cuanto más arriba, más difícil (pero lento)
    if y < 0:  # solo aplica dificultad si está por encima del origen
        return min(1.0, (abs(y) / 25000) ** 0.8)  # aumenta dificultad progresivamente
    return 0.0  # sin dificultad en zonas bajas





# Carga la imagen de la plataforma conservando la transparencia
imagen_plataforma = pygame.image.load("imagenes/plataforma.png")  # carga imagen con alfa

# Estas 2 lineas son para que la imagen de la plataforma se ajuste a la hitbox de la plataforma
rect_real = imagen_plataforma.get_bounding_rect()  # obtiene área visible real de la imagen
imagen_plataforma = imagen_plataforma.subsurface(rect_real).copy()  # recorta bordes transparentes

mostrar_hitbox = False  # activa/desactiva visualización de hitbox

def generar_plataformas(ultima_y, ancho_pantalla, carriles, plataformas, altura_max, imagen_plataforma, imagen_plataforma2):
    # genera una separación aleatoria en Y entre la última plataforma y la nueva
    separacion_y = random.randint(60, 200)
    
    # calcula la nueva posición Y restando la separación (se genera más arriba)
    y = ultima_y - separacion_y

    # elige un carril aleatorio (posición X posible para la plataforma)
    x = random.choice(carriles)
    
    # evita que dos plataformas seguidas aparezcan en el mismo carril
    while plataformas and plataformas[-1].rect.x == x:
        x = random.choice(carriles)
    
    # calcula la dificultad en base a la altura (cuanto más alto, más difícil)
    d = dificultad_por_altura(y)
    
    # ancho mínimo y máximo posibles de la plataforma
    ancho_min = 180
    ancho_max = 280
    
    
    d = min(d,3.0) # suaviza la curva de dificultad
    d = d**2
    
    # reduce el ancho de la plataforma según la dificultad
    ancho = int(ancho_max - (ancho_max - ancho_min) * d)

    ancho = max(ancho, ancho_min)  # límite mínimo
    
    # altura fija de la plataforma
    alto = 75

    
    # define el tipo de plataforma según el progreso del jugador

    if d < 0.9:
        tipo = "normal"
    else:
        tipo = "nivel"
    
     # crea la plataforma ya como sprite con sus parámetros finales
    plataforma = Plataforma(
    x,
    y,
    ancho,
    alto,
    tipo,
    imagen_plataforma,
    imagen_plataforma2
    )

    return plataforma, y


