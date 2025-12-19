import pygame
import os

class Artifact:
    def __init__(self, x, y, name, image_file=None):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.name = name
        self.collected = False
        self.image = None
        if image_file:
            path = os.path.join("assets", image_file)
            if os.path.exists(path):
                self.image = pygame.image.load(path).convert_alpha()
                self.image = pygame.transform.scale(self.image, (50, 50))

    def collect(self, player_rect, inventory):
        if not self.collected and self.rect.colliderect(player_rect):
            self.collected = True
            if self.name not in inventory:
                inventory.append(self.name)

    def draw(self, screen):
        if not self.collected:
            if self.image:
                screen.blit(self.image, self.rect.topleft)
            else:
                pygame.draw.rect(screen, (255, 215, 0), self.rect)  # fallback jaune
