import pygame
from player import Player

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

        # Création du joueur au centre de l'écran
        self.player = Player(
            x=self.screen_width // 2 - 25,
            y=self.screen_height // 2 - 25
        )

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
        self.player.handle_input()  # gestion des déplacements

    def draw(self):
        self.screen.fill((20, 30, 60))  # fond bleu foncé
        self.player.draw(self.screen)    # dessine le joueur
        pygame.display.flip()

