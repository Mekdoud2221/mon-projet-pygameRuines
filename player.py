import pygame

class Player:
    def __init__(self, x, y, width=50, height=50, color=(255, 255, 255)):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.speed = 5  # pixels par frame

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
        pygame.draw.rect(screen, self.color, self.rect)
