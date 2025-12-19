import pygame

class Room:
    def __init__(self, width, height, color=(50,50,100)):
        self.width = width
        self.height = height
        self.color = color
        self.walls = []       # murs / obstacles
        self.puzzles = []     # puzzles
        self.artifacts = []   # artefacts
        self.neighbors = {}   # salles connectées

    def add_wall(self, x, y, w, h):
        wall = pygame.Rect(x, y, w, h)
        self.walls.append(wall)

    def add_puzzle(self, puzzle):
        self.puzzles.append(puzzle)

    def add_artifact(self, artifact):
        self.artifacts.append(artifact)

    def add_neighbor(self, direction, room):
        self.neighbors[direction] = room

    def draw(self, screen):
        screen.fill(self.color)
        for wall in self.walls:
            pygame.draw.rect(screen, (100,100,100), wall)
        for puzzle in self.puzzles:
            puzzle.draw(screen)
        for artifact in self.artifacts:
            artifact.draw(screen)

        # ===== Portes visibles =====
        door_color = (180, 120, 40)

        if "right" in self.neighbors:
          pygame.draw.rect(screen, door_color, (self.width - 10, self.height//2 - 40, 10, 80))

        if "left" in self.neighbors:
          pygame.draw.rect(screen, door_color, (0, self.height//2 - 40, 10, 80))

        if "up" in self.neighbors:
          pygame.draw.rect(screen, door_color, (self.width//2 - 40, 0, 80, 10))

        if "down" in self.neighbors:
          pygame.draw.rect(screen, door_color, (self.width//2 - 40, self.height - 10, 80, 10))

