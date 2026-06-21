import pygame

class GameOver:
    def __init__(self):
        self.activo = False

        self.fuente_titulo = pygame.font.Font("fuentes/Orbitron Medium 500.ttf", 80)
        self.fuente_texto = pygame.font.Font("fuentes/Orbitron Medium 500.ttf", 30)

    def activar(self):
        self.activo = True

    def dibujar(self, pantalla, ancho, alto, puntos):
        titulo = self.fuente_titulo.render("GAME OVER", True, (255, 0, 0))
        score = self.fuente_texto.render(f"Puntos: {puntos}", True, (255, 255, 255))

        pantalla.blit(
            titulo,
            (ancho//2 - titulo.get_width()//2, alto//2 - 100)
        )

        pantalla.blit(
            score,
            (ancho//2 - score.get_width()//2, alto//2)
        )