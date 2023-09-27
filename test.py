import pygame
import sys
import random

pygame.init()

pause=False
pause_button=pygame.image.load("button_pause.png")

clock = pygame.time.Clock()

# constantes

WIDTH, HEIGHT = 800, 800 # taille fenêtre
WHITE = (255, 255, 255)

GROUND_HEIGHT = 30 # taille sol

MIN = HEIGHT-HEIGHT/2+100 # hauteur minimal du trou

DISTANCE = 210 # distance entre les tuyaux

PAUSE_BUTTON_SIZE = 64
BIRD_SIZE = 64
BORDER = 10

# Création de la fenêtre
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Floppy cat")




class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = 0
        self.width = 40 #épaisseur du tuyau
        self.gap = 150 #écart entre tuyau du haut et du bas
        self.top_height = random.randint(50, MIN) #calcule la hauteur minimum des tuyaux en fonction de la taille de la fenêtre
        self.bottom_height = HEIGHT - self.top_height - self.gap #calcule la hauteur du tuyau du bas

    def draw(self): #dessine la partie haute et basse du tuyau
        pygame.draw.rect(screen, (0, 255, 0), (self.x, 0, self.width, self.top_height))
        pygame.draw.rect(screen, (0, 255, 0), (self.x, HEIGHT - self.bottom_height, self.width, self.bottom_height))

    def update(self): # déplace les tuyaux
        self.x = self.x-2

class Bird:
    def __init__(self,x):
        self.x = x
        self.y = HEIGHT // 2
        self.speed = 0
        self.gravity = 0.5
        self.appa=pygame.image.load("bird.png")
        self.bird_rise=pygame.image.load("bird_rise.png")
        self.bird_fall=pygame.image.load("bird_fall.png")
        self.bird_current=self.appa

    def flap(self):
        self.speed = -9

    def update(self):
        self.speed += self.gravity
        self.y += self.speed
        if self.speed < -5:
            self.bird_current=self.bird_rise
        elif self.speed > 5 :
            self.bird_current=self.bird_fall
        else :
            self.bird_current=self.appa

    def draw(self):
        screen.blit(self.bird_current,(self.x, int(self.y)))

birds = [Bird(100),Bird(200)]
birds_event = [pygame.K_SPACE,pygame.K_p]



pipes = [Pipe(DISTANCE*i+DISTANCE) for i in range(4)]


while True:
    screen.fill((255,255,255))
    for event in pygame.event.get():
        #gestion fermeture fenetre
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos=pygame.mouse.get_pos()
            if WIDTH-BORDER>mouse_pos[0]>WIDTH-PAUSE_BUTTON_SIZE-BORDER and BORDER+PAUSE_BUTTON_SIZE>mouse_pos[1]>BORDER:
                pause=not(pause)    
        #gestion saut 
        if event.type == pygame.KEYDOWN and not pause:
            for i in range(len(birds_event)):
                if event.key == birds_event[i]:
                    birds[i].flap()
    
    if not pause :
        for i in range(len(birds)):
            birds[i].update()

    

    # Remove off-screen pipes
    # if pipes[0].x < -50:
    #     pipes.pop(0)
    #     pipes.append(Pipe(pipes[-1].x + 200))

# retirer les tuyaux et en ajouter de nouveaux
    if pipes[0].x < -pipes[0].width :
        pipes.pop(0)
    
    if pipes[3].x == WIDTH-DISTANCE :
        pipes.append(Pipe(WIDTH))

    # dessiner les tuyaux
    for pipe in pipes:
        pipe.update()
        pipe.draw()
        pygame.draw.rect(screen, (255, 125 , 0), (0, HEIGHT-GROUND_HEIGHT, WIDTH, GROUND_HEIGHT))

    #couleur arriere plan 
    for i in range(len(birds)):
        birds[i].draw()
    screen.blit(pause_button,(WIDTH-PAUSE_BUTTON_SIZE - BORDER,BORDER))

    
    pygame.display.update()
    clock.tick(60)
    