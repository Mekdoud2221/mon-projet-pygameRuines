import pygame
from player import Player
from room import Room

class Game:
    def __init__(self):
        pygame.init()
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height)
        )
        pygame.display.set_caption("Ruines des Anciens")

        self.clock = pygame.time.Clock()
        self.running = True

        # Création du joueur au centre
        self.player = Player(
            x=self.screen_width // 2 - 25,
            y=self.screen_height // 2 - 25
        )

        # Création d'une salle
        self.room = Room(self.screen_width, self.screen_height)
        # Ajouter quelques murs pour tester
        self.room.add_wall(100, 100, 200, 20)
        self.room.add_wall(400, 300, 20, 200)

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        self.player.handle_input()
        self.handle_collisions()

    def handle_collisions(self):
        # Simple collision avec les murs de la salle
        for wall in self.room.walls:
            if self.player.rect.colliderect(wall):
                # très simple : bloque le joueur en arrière
                if self.player.rect.right > wall.left and self.player.rect.left < wall.left:
                    self.player.rect.right = wall.left
                if self.player.rect.left < wall.right and self.player.rect.right > wall.right:
                    self.player.rect.left = wall.right
                if self.player.rect.bottom > wall.top and self.player.rect.top < wall.top:
                    self.player.rect.bottom = wall.top
                if self.player.rect.top < wall.bottom and self.player.rect.bottom > wall.bottom:
                    self.player.rect.top = wall.bottom

    def draw(self):
        self.room.draw(self.screen)
        self.player.draw(self.screen)
        pygame.display.flip()


