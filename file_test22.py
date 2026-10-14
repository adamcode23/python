import pygame_ce
import sys

pygame.init()
screen = pygame.display.set_mode((400, 400))
clock = pygame.time.Clock()

# Position de départ du carré
x, y = 200, 200
vitesse = 5

while True:
    screen.fill((0, 0, 0)) # Fond noir
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    # Détection des touches du clavier
    touches = pygame.key.get_pressed()
    if touches[pygame.K_LEFT]:  x -= vitesse
    if touches[pygame.K_RIGHT]: x += vitesse
    if touches[pygame.K_UP]:    y -= vitesse
    if touches[pygame.K_DOWN]:  y += vitesse
    
    # Dessiner le joueur (un carré blanc)
    pygame.draw.rect(screen, (255, 255, 255), (x, y, 30, 30))
    
    pygame.display.flip()
    clock.tick(60)
