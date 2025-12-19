import pygame
from player import Player
from room import Room
from puzzle import Puzzle
from artifact import Artifact
from storage import save_game, load_game

class Game:
    def __init__(self):
        pygame.init()
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Ruines des Anciens")

        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.SysFont(None, 24)

        # Joueur
        self.player = Player(380, 280)

        # Salles
        self.rooms = {}
        self.create_rooms()
        self.current_room = self.rooms["room1"]

        # Inventaire
        self.inventory = []
        self.victory = False

        # Chargement sauvegarde
        inv, rooms_data = load_game()
        self.inventory = inv

        for room_id, room in self.rooms.items():
            if room_id in rooms_data:
                data = rooms_data[room_id]
                for i, p in enumerate(room.puzzles):
                    if i < len(data.get("puzzles", [])):
                        p.solved = data["puzzles"][i]
                for i, a in enumerate(room.artifacts):
                    if i < len(data.get("artifacts", [])):
                        a.collected = data["artifacts"][i]

    # ==================================================

    def create_rooms(self):
        """Création des salles avec labyrinthes et portes"""

        # ================= SALLE 1 =================
        r1 = Room(self.screen_width, self.screen_height, (30, 30, 80))

        # Murs extérieurs AVEC portes
        r1.add_wall(0, 0, 800, 20)          # haut
        r1.add_wall(0, 580, 300, 20)        # bas gauche
        r1.add_wall(400, 580, 400, 20)      # bas droite
        r1.add_wall(0, 0, 20, 600)          # gauche
        r1.add_wall(780, 0, 20, 250)        # droite haut
        r1.add_wall(780, 350, 20, 250)      # droite bas

        # Labyrinthe intérieur
        r1.add_wall(100, 50, 20, 400)
        r1.add_wall(200, 150, 20, 400)
        r1.add_wall(300, 0, 20, 300)
        r1.add_wall(400, 250, 20, 300)
        r1.add_wall(500, 50, 20, 400)

        r1.add_artifact(Artifact(60, 520, "Amulette", "amulette.png"))
        r1.add_puzzle(Puzzle(700, 500))

        # ================= SALLE 2 =================
        r2 = Room(self.screen_width, self.screen_height, (70, 40, 60))

        # Murs extérieurs
        r2.add_wall(0, 0, 800, 20)      # haut
        r2.add_wall(0, 580, 350, 20)    # bas gauche
        r2.add_wall(450, 580, 350, 20)  # bas droite, laisse ouverture entre 350-450 pour sortie bas
        r2.add_wall(0, 0, 20, 250)      # gauche haut
        r2.add_wall(0, 350, 20, 250)    # gauche bas
        r2.add_wall(780, 0, 20, 600)    # droite (ok car sortie bas est en bas, joueur n’est pas bloqué)

        # Labyrinthe intérieur
        r2.add_wall(150, 100, 300, 20)
        r2.add_wall(300, 200, 20, 300)
        r2.add_wall(450, 50, 20, 400)

        r2.add_artifact(Artifact(700, 100, "Masque ancien", "masque.png"))
        r2.add_puzzle(Puzzle(350, 350))

        # ================= SALLE 3 =================
        r3 = Room(self.screen_width, self.screen_height, (30, 80, 50))

        # Mur haut AVEC sortie
        r3.add_wall(0, 0, 300, 20)
        r3.add_wall(400, 0, 400, 20)

        # Autres murs
        r3.add_wall(0, 580, 800, 20)
        r3.add_wall(0, 0, 20, 600)
        r3.add_wall(780, 0, 20, 600)

        # Labyrinthe
        r3.add_wall(100, 100, 20, 400)
        r3.add_wall(200, 200, 20, 400)
        r3.add_wall(300, 100, 20, 300)
        r3.add_wall(400, 250, 20, 250)

        r3.add_puzzle(Puzzle(350, 250))

        # Connexions
        r1.add_neighbor("right", r2)
        r2.add_neighbor("left", r1)
        r2.add_neighbor("down", r3)
        r3.add_neighbor("up", r2)

        self.rooms["room1"] = r1
        self.rooms["room2"] = r2
        self.rooms["room3"] = r3

    # ==================================================

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        pygame.quit()

    # ==================================================

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    rooms_data = {}
                    for room_id, room in self.rooms.items():
                        rooms_data[room_id] = {
                            "puzzles": [p.solved for p in room.puzzles],
                            "artifacts": [a.collected for a in room.artifacts]
                        }
                    save_game(self.inventory, rooms_data)

    # ==================================================

    def update(self):
        self.player.handle_input()
        self.handle_collisions()

        for puzzle in self.current_room.puzzles:
            puzzle.interact(self.player.rect)

        for artifact in self.current_room.artifacts:
            artifact.collect(self.player.rect, self.inventory)

        # Condition de victoire
        if self.current_room == self.rooms["room3"]:
            for puzzle in self.current_room.puzzles:
                if puzzle.solved:
                    self.victory = True

        self.check_room_transition()

    # ==================================================

    def handle_collisions(self):
        for wall in self.current_room.walls:
            if self.player.rect.colliderect(wall):
                if self.player.rect.right > wall.left and self.player.rect.left < wall.left:
                    self.player.rect.right = wall.left
                if self.player.rect.left < wall.right and self.player.rect.right > wall.right:
                    self.player.rect.left = wall.right
                if self.player.rect.bottom > wall.top and self.player.rect.top < wall.top:
                    self.player.rect.bottom = wall.top
                if self.player.rect.top < wall.bottom and self.player.rect.bottom > wall.bottom:
                    self.player.rect.top = wall.bottom

    # ==================================================

    def check_room_transition(self):
        if self.player.rect.right > self.current_room.width:
            if "right" in self.current_room.neighbors:
                self.current_room = self.current_room.neighbors["right"]
                self.player.rect.left = 0

        elif self.player.rect.left < 0:
            if "left" in self.current_room.neighbors:
                self.current_room = self.current_room.neighbors["left"]
                self.player.rect.right = self.current_room.width

        elif self.player.rect.top < 0:
            if "up" in self.current_room.neighbors:
                self.current_room = self.current_room.neighbors["up"]
                self.player.rect.bottom = self.current_room.height

        elif self.player.rect.bottom > self.current_room.height:
            if "down" in self.current_room.neighbors:
                self.current_room = self.current_room.neighbors["down"]
                self.player.rect.top = 0

    # ==================================================

    def draw(self):
        self.screen.fill(self.current_room.color)  # Fill with room color

        if self.victory:
            # Draw victory message
            text = self.font.render(
                "VICTOIRE ! Vous avez percé les secrets des ruines",
                True,
                (255, 215, 0)
            )
            self.screen.blit(text, (80, 300))
        else:
            # Draw the room and player
            self.current_room.draw(self.screen)
            self.player.draw(self.screen)

            # Draw inventory
            x = 10
            for item in self.inventory:
                txt = self.font.render(item, True, (255, 255, 0))
                self.screen.blit(txt, (x, 10))
                x += txt.get_width() + 10

        pygame.display.flip()
