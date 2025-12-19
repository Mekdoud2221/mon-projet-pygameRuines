import pygame

class Puzzle:
    def __init__(self, x, y, width=50, height=50, color=(255, 215, 0)):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.solved = False

    def interact(self, player_rect):
        """
        Vérifie si le joueur est sur le puzzle.
        Si oui, résout le puzzle.
        """
        if self.rect.colliderect(player_rect) and not self.solved:
            self.solved = True
            print("Puzzle résolu !")  # Placeholder, peut déclencher autre chose

    def draw(self, screen):
        if not self.solved:
            pygame.draw.rect(screen, self.color, self.rect)
