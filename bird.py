import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 400, 600
PAUSE_BUTTON_SIZE = 64
BIRD_SIZE = 64
BORDER = 10

pause=False
pause_button=pygame.image.load("button_pause.png")
#création de la fenetre graphique 
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird Project")

clock = pygame.time.Clock()


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

while True:


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
    

    #couleur arriere plan 
    screen.fill((255,255,255))
    for i in range(len(birds)):
        birds[i].draw()
    screen.blit(pause_button,(WIDTH-PAUSE_BUTTON_SIZE - BORDER,BORDER))
    pygame.display.update()
    clock.tick(60)