import pygame
import constantes


CELESTE      = (82, 164, 209)
AZUL         = (33, 101, 138)
AMARILLO     = (255, 255,   0)
AMARILLO_OSC = (180, 180,   0)
HUESO        = (193, 214, 207)
BLANCO       = (255, 255, 255)
VIOLETA       = (113, 33, 163)
GRIS         = ( 80,  80,  80)

fuente_titulo = pygame.font.Font("assets/04B_30__.TTF", 70) # TITULO fuente 
fuente_grande = pygame.font.Font("assets/04B_30__.TTF", 35) # PONER EN CONSTANTES
fuente_chica = pygame.font.Font("assets/04B_30__.TTF", 22)  # PONER EN CONSTANTES

fondo = pygame.image.load("imagenes/ciudad.webp")
fondo = pygame.transform.scale(fondo, (constantes.ANCHO_VENTANA, constantes.ALTO_VENTANA))


boton_ancho, boton_alto = 260, 60
boton_x = constantes.ANCHO_VENTANA // 2 - boton_ancho // 2
boton_y = constantes.ALTO_VENTANA  // 2 - 60
boton_jugar_rect = pygame.Rect(boton_x, boton_y, boton_ancho, boton_alto)
boton_opciones_rect = pygame.Rect(boton_x, boton_y + 100, boton_ancho, boton_alto)
boton_salir_rect = pygame.Rect(boton_x,boton_y + 200,boton_ancho,boton_alto)


# ── Barra de volumen ───────────────────────────────────────────
arrastrando  = False
barra_ancho  = 260
barra_alto   = 10
barra_x = boton_opciones_rect.right + 40
barra_y = boton_opciones_rect.top + 80
barra_rect   = pygame.Rect(barra_x, barra_y, barra_ancho, barra_alto)


opciones_abiertas = False

menu_opciones_rect = pygame.Rect(
    boton_opciones_rect.right + 20,
    boton_opciones_rect.top,
    300,
    120
)

def get_perilla_rect():
    px = barra_x + int(constantes.volumen * barra_ancho) - 8
    py = barra_y - 8
    return pygame.Rect(px, py, 16, 26)

def dibujar_boton(screen,hover, rect, texto):
    color     = CELESTE     if hover else AZUL
    color_borde = BLANCO     if hover else HUESO
    # sombra retro (desplazada 4px)
    pygame.draw.rect(screen, VIOLETA, rect.move(4, 4))
    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, color_borde, rect, 3)
    texto = fuente_grande.render(texto, True, VIOLETA)
    screen.blit(texto, texto.get_rect(center=rect.center))


def dibujar_volumen(screen):

    # volumen
    label = fuente_chica.render("VOLUMEN", True, BLANCO)
    screen.blit(label, (barra_x, barra_y - 30))

    # vacío
    pygame.draw.rect(screen, GRIS, barra_rect)

    # relleno
    relleno = pygame.Rect(
        barra_x,
        barra_y,
        int(constantes.volumen * barra_ancho),
        barra_alto
    )

    pygame.draw.rect(screen, VIOLETA, relleno)

    # Borde
    pygame.draw.rect(screen, BLANCO, barra_rect, 2)

    # Perilla
    pygame.draw.rect(screen, BLANCO, get_perilla_rect())
    pygame.draw.rect(screen, VIOLETA, get_perilla_rect(), 2)
    # Porcentaje
    pct = fuente_chica.render(
        f"{int(constantes.volumen * 100)}%",
        True,
        BLANCO
    )

    screen.blit(
        pct,
        (barra_x + barra_ancho + 12, barra_y - 6)
    )
def dibujar_menu_opciones(screen):

    panel_x = boton_opciones_rect.right + 20
    panel_y = boton_opciones_rect.top
    pygame.draw.rect(
        screen,
        AZUL,
        (panel_x, panel_y, 360, 120)
    )
    pygame.draw.rect(
        screen,
        BLANCO,
        (panel_x, panel_y, 360, 120),
        3
    )
    dibujar_volumen(screen)

def guardar_volumen():

    with open("constantes.py", "r", encoding="utf-8") as f:
        lineas = f.readlines()

    with open("constantes.py", "w", encoding="utf-8") as f:

        for linea in lineas:

            if linea.startswith("volumen ="):
                f.write(f"volumen = {constantes.volumen}\n")
            else:
                f.write(linea)    

def dibujar_menu(screen):

    screen.blit(fondo, (0, 0))

    mouse = pygame.mouse.get_pos()

    sombra = fuente_titulo.render("NEON JUMP", True, VIOLETA)

    screen.blit(sombra,sombra.get_rect(center=(constantes.ANCHO_VENTANA // 2 + 4, 154)))
    
    
    titulo = fuente_titulo.render("NEON JUMP", True, BLANCO)

    screen.blit(titulo,titulo.get_rect(center=(constantes.ANCHO_VENTANA // 2, 150)))
    
    hover_jugar = boton_jugar_rect.collidepoint(mouse)
    hover_opciones = boton_opciones_rect.collidepoint(mouse)
    hover_salir = boton_salir_rect.collidepoint(mouse)
    
    dibujar_boton(screen, hover_jugar, boton_jugar_rect, "JUGAR")
    dibujar_boton(screen, hover_opciones, boton_opciones_rect, "OPCIONES")
    dibujar_boton(screen, hover_salir, boton_salir_rect, "SALIR")
    
    if opciones_abiertas:
        dibujar_menu_opciones(screen)



def actualizar_menu(event):

    global opciones_abiertas
    global arrastrando

    # El usuario tocó el mouse
    if event.type == pygame.MOUSEBUTTONDOWN:

        # Botón JUGAR
        if boton_jugar_rect.collidepoint(event.pos):
            return "JUGAR"

        # Botón OPCIONES
        if boton_opciones_rect.collidepoint(event.pos):
            opciones_abiertas = not opciones_abiertas

        if boton_salir_rect.collidepoint(event.pos):
            return "SALIR"

        # Empezar a mover la perilla
        if opciones_abiertas and get_perilla_rect().collidepoint(event.pos):
            arrastrando = True

    # Soltó el mouse
    elif event.type == pygame.MOUSEBUTTONUP:

        arrastrando = False
        guardar_volumen()

    # Arrastra la perilla
    elif event.type == pygame.MOUSEMOTION and arrastrando:

        x = max(barra_x, min(event.pos[0], barra_x + barra_ancho))

        constantes.volumen = (x - barra_x) / barra_ancho

        pygame.mixer.music.set_volume(constantes.volumen)

    return None



