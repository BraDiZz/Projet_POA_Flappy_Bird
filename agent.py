class Agent:
    def __init__(self, indice, BIRDS_CONST, next_tuyau, gap_tuyau, nb_frame_interval):
    	self.nb_frame_interval = nb_frame_interval
    	self.compteur = nb_frame_interval # Nombre de frame avant de pouvoir faire une action
    	self.indice = indice
    	self.bird_y = BIRDS_CONST.INIT_Y
    	self.bird_size = BIRDS_CONST.SIZE
    	self.max_speed = BIRDS_CONST.SPEED # speed quand l'agent déclenche l'action de voler (ATTENTION : ici < 0 pour que l'oiseau monte sur la fenêtre, càd y diminue)
    	self.gravite = BIRDS_CONST.GRAVITY
    	self.next_tuyau = next_tuyau # Coordonnée y du point en bas à gauche du tuyau du haut (seule info à avoir sur un tuyaux)
    	self.gap_tuyau = gap_tuyau
    	
    	self.jump_length = self.getJumpLength()
    	
    def getJumpLength(self):
    	res = 0
    	tmp = self.max_speed
    	while (tmp < 0):
    		res += tmp
    		tmp += self.gravite
    	return abs(res)
    
    def setInfo(self,bird_y, next_tuyau): # Le main envoie les infos nécessaires qui doivent être mises à jour du côté de l'agent
    	self.bird_y = bird_y
    	self.next_tuyau = next_tuyau
		
    def update(self, bird_y, next_tuyau):
    	self.setInfo(bird_y, next_tuyau)
    	if self.bird_y + self.bird_size > self.next_tuyau + self.gap_tuyau : # L'oiseau est trop bas, il doit monter
    		if self.compteur < 0:
    			self.compteur = self.nb_frame_interval
    			return True
    		else:
    			self.compteur -= 1
    			return False
    	elif self.bird_y < self.next_tuyau + self.jump_length :  # L'oiseau est trop haut, il doit se laisser tomber (attention à bien prendre en compte la hauteur du saut)
    		self.compteur -= 1
    		return False
    	else : # L'oiseau doit rester au même niveau
    		if self.compteur < 0:
    			self.compteur = self.nb_frame_interval
    			return True
    		else:
    			self.compteur -= 1
    			return False
    	
