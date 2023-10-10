import pygame
import sys
import random
import time
from collections import namedtuple
import agent

pygame.init()

clock = pygame.time.Clock()
WIDTH, HEIGHT = 1200,800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Floppy cat")
WHITE = (255,255,255)

transparency_background = pygame.Surface((WIDTH,HEIGHT))
transparency_background.set_alpha(150)
transparency_background.fill((255,255,255))

PAUSE_BUTTON_SIZE = 64
BORDER = 10
MIN_HOLE_POSITION = HEIGHT-HEIGHT/2+100 # hauteur minimal du trou

t_const = namedtuple('TUYAUX', ['GAP', 'WIDTH','DISTANCE','COLOR','MIN_HEIGHT','SPEED']) # Dictionnaire de constante pour les tuyaux, accessible via le nom des champs
TUYAUX_CONST = t_const(250, 80, 400, (0, 255, 0), 50, 6) # Ecart entre tuyau du haut et du bas, Largeur d'un tuyau, Distance entre 2 tuyaux
b_const = namedtuple('BIRDS', ['INIT_Y','GRAVITY','SPEED','IMG_NEUTRAL', 'IMG_RISE','IMG_FALL','SIZE','COLORS']) # Dictionnaire de constante pour les oiseaux, accessible via le nom des champs
BIRDS_CONST = b_const(HEIGHT // 2, 0.8, -14, pygame.image.load("bird.png"), pygame.image.load("bird_rise.png"), pygame.image.load("bird_fall.png"),64,[(255,10,10),(10,255,10),(10,10,255)]) 

bg = pygame.image.load("background.jpg")
pause_button=pygame.image.load("button_pause.png")
bg_list = [[bg,0],[bg,WIDTH-10]]

font = pygame.font.Font('freesansbold.ttf', 64)
loose_text = font.render(" Vous avez perdu ", True, (10,10,10), (240,240,240)) # S'affiche quand tout les joueurs ont perdu
loose_textRect = loose_text.get_rect()
loose_textRect.center = (WIDTH // 2, HEIGHT // 2)
pause_text = font.render(" Pause ", True, (10,10,10), (240,240,240)) # S'affiche quand le jeu est en pause
pause_textRect = pause_text.get_rect()
pause_textRect.center = (WIDTH // 2, HEIGHT // 2)

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
    	self.top_size = random.randint(TUYAUX_CONST.MIN_HEIGHT, HEIGHT - TUYAUX_CONST.MIN_HEIGHT - TUYAUX_CONST.GAP) # Calcule la hauteur minimum des tuyaux en fonction de la taille de la fenêtre
    	self.top_tuyau = pygame.Rect((x,0),(TUYAUX_CONST.WIDTH,self.top_size))
    	self.bottom_tuyau = pygame.Rect((x,self.top_size + TUYAUX_CONST.GAP),(TUYAUX_CONST.WIDTH,HEIGHT - self.top_size - TUYAUX_CONST.GAP))

    def draw(self): # Dessine la partie haute et basse du tuyau
    	pygame.draw.rect(screen, TUYAUX_CONST.COLOR,self.top_tuyau)
    	pygame.draw.rect(screen, TUYAUX_CONST.COLOR, self.bottom_tuyau)

    def update(self): # Déplace les tuyaux
    	self.top_tuyau.x -= TUYAUX_CONST.SPEED
    	self.bottom_tuyau.x -= TUYAUX_CONST.SPEED

class Bird:
    def __init__(self,x,ind_color):
        self.x = x
        self.y = BIRDS_CONST.INIT_Y
        self.speed = 0
        self.gravity = BIRDS_CONST.GRAVITY
        self.rect_bird = pygame.Rect((self.x,self.y),((BIRDS_CONST.SIZE,BIRDS_CONST.SIZE))) # Crée un rectangle pour la collision de l'oiseau
        
        self.bird_neutre = self.changeColor(BIRDS_CONST.IMG_NEUTRAL.copy(),BIRDS_CONST.COLORS[ind_color])
        self.bird_vol = self.changeColor(BIRDS_CONST.IMG_RISE.copy(),BIRDS_CONST.COLORS[ind_color])
        self.bird_tombe = self.changeColor(BIRDS_CONST.IMG_FALL.copy(),BIRDS_CONST.COLORS[ind_color])
        self.bird_current=self.bird_neutre
    
    def changeColor(self,img_bird, new_color):
    	width_img, height_img = img_bird.get_size()
    	for x in range(width_img):
    		for y in range(height_img):
    			if img_bird.get_at((x,y))[1] > 120: # L'image n'est pas uniforme, donc pour savoir si un pixel est vert on regarde si vert > 120
    				img_bird.set_at((x,y), new_color)
    	return img_bird

    def flap(self):
        self.speed = BIRDS_CONST.SPEED

    def update(self):
        self.speed += BIRDS_CONST.GRAVITY
        self.y += self.speed
        self.rect_bird.y = self.y # Update rect position
        if self.speed < -5:
            self.bird_current=self.bird_vol
        elif self.speed > 5 :
            self.bird_current=self.bird_tombe
        else :
            self.bird_current=self.bird_neutre

    def draw(self):
        screen.blit(self.bird_current,(self.x, int(self.y)))

birds = [Bird(100,0),Bird(200,1)]#,Bird(300,2)]
birds_event = [pygame.K_SPACE,pygame.K_p]
pipes = [Pipe(TUYAUX_CONST.DISTANCE*i+WIDTH) for i in range(4)] # Les premiers tuyaux arrivent de l'extérieur de la fenêtre


indice_prochain_tuyau = 0 # Prochain tuyau rencontré par l'agent (initialement à 0)
agent = agent.Agent(0, BIRDS_CONST,pipes[indice_prochain_tuyau].top_tuyau.height, TUYAUX_CONST.GAP, 15) # # L'oiseau d'indice 1 dans le tableau de Bird est celui contrôlé par l'agent


perdu = False

while True:
	if pause :
		screen.blit(pause_button,(WIDTH-PAUSE_BUTTON_SIZE - BORDER,BORDER))
		screen.blit(pause_text, pause_textRect)
		pygame.display.update()
		for event in pygame.event.get():
			if switchPause(event):
				pause = not pause
			fermeture(event)
		continue
	elif perdu :
		for event in pygame.event.get():
			fermeture(event)
		continue
		
	for event in pygame.event.get():
		if switchPause(event):
			pause = not pause
	
        #gestion fermeture fenetre
		fermeture(event)
		if event.type == pygame.KEYDOWN:
			for i in range(len(birds_event)):
				if event.key == birds_event[i]: # Tous les event concernent des oiseaux qui ne sont pas controlés par l'agent
					if i < agent.indice:
						birds[i].flap() # L'event d'indice i correspond à l'oiseau d'indice 1
					else:
						birds[i+1].flap()# On décale de 1 pour avoir le bon oiseau
	
	if birds[agent.indice].x > pipes[indice_prochain_tuyau].top_tuyau.x + TUYAUX_CONST.WIDTH : # L'oiseau a passé un tuyau
		indice_prochain_tuyau+=1
					
	if agent.update(birds[agent.indice].y,pipes[indice_prochain_tuyau].top_tuyau.height):
		birds[agent.indice].flap()
	
	
	
	screen.fill(WHITE)
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
	if pipes[0].top_tuyau.x < -TUYAUX_CONST.WIDTH:
		indice_prochain_tuyau -= 1
		pipes.pop(0)
		
	if pipes[len(pipes)-1].top_tuyau.x <= WIDTH-TUYAUX_CONST.DISTANCE :
		pipes.append(Pipe(WIDTH))
	
	# Dessiner les oiseaux
	for i in range(len(birds)):
		birds[i].update()
		#pygame.draw.rect(screen, (240,20,20), birds[i].rect_bird)
		birds[i].draw()
		
		for pipe in pipes :
			if pygame.Rect.colliderect(birds[i].rect_bird,pipe.top_tuyau) or pygame.Rect.colliderect(birds[i].rect_bird,pipe.bottom_tuyau) :
				perdu = True
				screen.blit(transparency_background, (0,0))
				screen.blit(loose_text, loose_textRect)
	
	screen.blit(pause_button,(WIDTH-PAUSE_BUTTON_SIZE - BORDER,BORDER))
	pygame.display.update()
	clock.tick(60)
