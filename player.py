import pygame
import os

class Player:
    def __init__(self, x=100, y=100, width=70, height=50):
        # Rectangle pour gérer collisions et position
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = 5

        # Charger l'image du joueur
        try:
            self.image = pygame.image.load(os.path.join("assets", "player.png")).convert_alpha()
            self.image = pygame.transform.scale(self.image, (width, height))  # redimensionner si nécessaire
        except:
            print("⚠️ Impossible de charger player.png dans assets/ !")
            self.image = pygame.Surface((width, height))
            self.image.fill((255, 255, 255))  # fallback : carré blanc

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

    def draw(self, screen):
        # Affiche l'image à la position du joueur
        screen.blit(self.image, self.rect.topleft)

