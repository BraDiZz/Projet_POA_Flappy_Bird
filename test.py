import pygame
import sys
import random

pygame.init()

# constantes des tuyaux
WIDTH, HEIGHT = 600, 800
WHITE = (255, 255, 255)

# Création de la fenêtre
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Floppy cat")




class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = 0
        self.width = 20 #épaisseur du tuyau
        self.gap = 150 #écart entre tuyau du haut et du bas
        self.top_height = random.randint(50, HEIGHT-HEIGHT/4) #calcule la hauteur minimum des tuyaux en fonction de la taille de la fenêtre
        self.bottom_height = HEIGHT - self.top_height - self.gap #calcule la hauteur du tuyau du bas

    def draw(self): #dessine la partie haute et basse du tuyau
        pygame.draw.rect(screen, (0, 255, 0), (self.x, 0, self.width, self.top_height))
        pygame.draw.rect(screen, (0, 255, 0), (self.x, HEIGHT - self.bottom_height, self.width, self.bottom_height))

pipes = [Pipe(100),Pipe(300),Pipe(500),Pipe(700)]

while True: #gère la partie
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(WHITE)

    # dessiner les tuyaux
    for pipe in pipes:
        pipe.draw()

    pygame.display.update()