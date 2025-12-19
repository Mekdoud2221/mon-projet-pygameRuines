import pygame

class Room:
    def __init__(self, width, height, color=(50, 50, 100)):
        self.width = width
        self.height = height
        self.color = color
        self.walls = []  # liste de pygame.Rect pour les murs/obstacles

    def add_wall(self, x, y, w, h):
        """Ajoute un mur/obstacle dans la salle"""
        wall = pygame.Rect(x, y, w, h)
        self.walls.append(wall)

    def draw(self, screen):
        # fond de la salle
        screen.fill(self.color)
        # dessiner les murs
        for wall in self.walls:
            pygame.draw.rect(screen, (150, 150, 150), wall)
