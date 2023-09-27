import pygame
import sys
import random

pygame.init()

# Constants
WIDTH, HEIGHT = 400, 600
WHITE = (255, 255, 255)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird Clone")

clock = pygame.time.Clock()

class Bird:
    def __init__(self):
        self.x = 100
        self.y = HEIGHT // 2
        self.velocity = 0
        self.gravity = 0.5

    def flap(self):
        self.velocity = -10

    def update(self):
        self.velocity += self.gravity
        self.y += self.velocity

    def draw(self):
        pygame.draw.circle(screen, (255, 0, 0), (self.x, int(self.y)), 20)

class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = 0
        self.gap = 200
        self.top_height = random.randint(50, 300)
        self.bottom_height = HEIGHT - self.top_height - self.gap

    def update(self):
        self.x -= 2

    def collides_with_bird(self, bird):
        if bird.x + 20 > self.x and bird.x - 20 < self.x + 50:
            if bird.y - 20 < self.top_height or bird.y + 20 > HEIGHT - self.bottom_height:
                return True
        return False

    def draw(self):
        pygame.draw.rect(screen, (0, 255, 0), (self.x, 0, 50, self.top_height))
        pygame.draw.rect(screen, (0, 255, 0), (self.x, HEIGHT - self.bottom_height, 50, self.bottom_height))

bird = Bird()
pipes = [Pipe(WIDTH + i * 200) for i in range(4)]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird.flap()

    bird.update()

    # Check for collisions
    for pipe in pipes:
        if pipe.collides_with_bird(bird):
            pygame.quit()
            sys.exit()

    # Remove off-screen pipes
    if pipes[0].x < -50:
        pipes.pop(0)
        pipes.append(Pipe(pipes[-1].x + 200))

    # Generate new pipes
    if pipes[-1].x < WIDTH - 200:
        pipes.append(Pipe(WIDTH))

    # Clear the screen
    screen.fill(WHITE)

    # Draw objects
    for pipe in pipes:
        pipe.update()
        pipe.draw()

    bird.draw()

    pygame.display.update()
    clock.tick(60)
