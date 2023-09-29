import pygame
import sys
import random
import time
from collections import namedtuple

clock = pygame.time.Clock()
WIDTH, HEIGHT = 1200,800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Floppy cat")
WHITE = (255,255,255)
PAUSE_BUTTON_SIZE = 64
BORDER = 10
MIN_HOLE_POSITION = HEIGHT-HEIGHT/2+100 # hauteur minimal du trou

t_const = namedtuple('TUYAUX', ['GAP', 'WIDTH','DISTANCE','COLOR','MIN_HEIGHT','SPEED']) # Dictionnaire de constante pour les tuyaux, accessible via le nom des champs
TUYAUX_CONST = t_const(250, 80, 400, (0, 255, 0), 50, 6) # Ecart entre tuyau du haut et du bas, Largeur d'un tuyau, Distance entre 2 tuyaux
b_const = namedtuple('BIRDS', ['INIT_Y','GRAVITY','SPEED','IMG_NEUTRAL', 'IMG_RISE','IMG_FALL']) # Dictionnaire de constante pour les oiseaux, accessible via le nom des champs
BIRDS_CONST = b_const(HEIGHT // 2, 0.5, -9, pygame.image.load("bird.png"), pygame.image.load("bird_rise.png"), pygame.image.load("bird_fall.png")) 

bg = pygame.image.load("background.jpg")
pause_button=pygame.image.load("button_pause.png")
bg_list = [[bg,0],[bg,WIDTH-10]]

pause = False

def switchPause(event):
	if event.type == pygame.MOUSEBUTTONDOWN:
		mouse_pos=pygame.mouse.get_pos()
		return WIDTH-BORDER>mouse_pos[0]>WIDTH-PAUSE_BUTTON_SIZE-BORDER and BORDER+PAUSE_BUTTON_SIZE>mouse_pos[1]>BORDER 
		
def fermeture(event):
	if event.type == pygame.QUIT:
		pygame.quit()
		sys.exit()

class Pipe:
    def __init__(self, x):
    	self.x = x
    	self.top_size = random.randint(TUYAUX_CONST.MIN_HEIGHT, HEIGHT - TUYAUX_CONST.MIN_HEIGHT - TUYAUX_CONST.GAP) # Calcule la hauteur minimum des tuyaux en fonction de la taille de la fenêtre

    def draw(self): # Dessine la partie haute et basse du tuyau
    	pygame.draw.rect(screen, TUYAUX_CONST.COLOR, (self.x, 0, TUYAUX_CONST.WIDTH, self.top_size))
    	pygame.draw.rect(screen, TUYAUX_CONST.COLOR, (self.x, self.top_size + TUYAUX_CONST.GAP, TUYAUX_CONST.WIDTH, HEIGHT - self.top_size - TUYAUX_CONST.GAP))

    def update(self): # Déplace les tuyaux
    	self.x -= TUYAUX_CONST.SPEED

class Bird:
    def __init__(self,x):
        self.x = x
        self.y = BIRDS_CONST.INIT_Y
        self.speed = 0
        self.gravity = BIRDS_CONST.GRAVITY
        self.bird_current=BIRDS_CONST.IMG_NEUTRAL

    def flap(self):
        self.speed = BIRDS_CONST.SPEED

    def update(self):
        self.speed += BIRDS_CONST.GRAVITY
        self.y += self.speed
        if self.speed < -5:
            self.bird_current=BIRDS_CONST.IMG_RISE
        elif self.speed > 5 :
            self.bird_current=BIRDS_CONST.IMG_FALL
        else :
            self.bird_current=BIRDS_CONST.IMG_NEUTRAL

    def draw(self):
        screen.blit(self.bird_current,(self.x, int(self.y)))

birds = [Bird(100),Bird(200)]
birds_event = [pygame.K_SPACE,pygame.K_p]
pipes = [Pipe(TUYAUX_CONST.DISTANCE*i+WIDTH) for i in range(4)] # Les premiers tuyaux arrivent de l'extérieur de la fenêtre

while True:
	screen.fill(WHITE)
	if pause :
		for event in pygame.event.get():
			if switchPause(event):
				pause = not pause
			fermeture(event)
		continue
	for event in pygame.event.get():
		if switchPause(event):
			pause = not pause
	
        #gestion fermeture fenetre
		fermeture(event)
		if event.type == pygame.KEYDOWN:
			for i in range(len(birds_event)):
				if event.key == birds_event[i]:
					birds[i].flap()
	
	for i in range(len(bg_list)): # Le background se déplace vers la gauche
		bg_list[i][1] -= 4
		screen.blit(bg_list[i][0],(bg_list[i][1],0))
	if bg_list[0][1] <= -WIDTH:
		bg_list.reverse()
		bg_list[1][1] = bg_list[0][1]+WIDTH
		
	# Dessiner les tuyaux
	for pipe in pipes:
		pipe.update()
		pipe.draw()
	
	# Retirer les tuyaux et en ajouter de nouveaux
	if pipes[0].x < -TUYAUX_CONST.WIDTH:
		pipes.pop(0)
		
	if pipes[len(pipes)-1].x <= WIDTH-TUYAUX_CONST.DISTANCE :
		pipes.append(Pipe(WIDTH))
		
	# Dessiner les oiseaux
	for i in range(len(birds)):
		birds[i].update()
		birds[i].draw()
	
	screen.blit(pause_button,(WIDTH-PAUSE_BUTTON_SIZE - BORDER,BORDER))
	pygame.display.update()
	clock.tick(60)
