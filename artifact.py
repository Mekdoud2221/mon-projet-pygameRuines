import pygame

class Artifact:
    def __init__(self, x, y, width=30, height=30, color=(0, 255, 0), name="Artefact"):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.name = name
        self.collected = False

    def collect(self, player_rect, inventory):
        """
        Vérifie si le joueur touche l'artefact.
        Si oui, l'ajoute à l'inventaire et marque comme collecté.
        """
        if self.rect.colliderect(player_rect) and not self.collected:
            self.collected = True
            inventory.append(self.name)
            print(f"Artefact collecté : {self.name}")

    def draw(self, screen):
        if not self.collected:
            pygame.draw.rect(screen, self.color, self.rect)
