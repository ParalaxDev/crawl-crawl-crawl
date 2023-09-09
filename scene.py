import pygame
from wall import Wall
from floor import Floor
from player import Player
from spawn_enemy import Enemy
from levels import ROOMS

from ui import UI

start = (336, 624)
top = (336, 0)
right = (672, 336)
bottom = (336, 672)
left = (0, 336)


class Scene:
    def __init__(self, screen):
        self.screen = screen
        #  sprite groups (whether they are interactable and/or visible etc.)
        #  sprite groups will be passed into a class as a list becuase sprites can have more than one
        self.sprite = pygame.sprite.Group()
        self.obstruction = pygame.sprite.Group()
        self.environment = pygame.sprite.Group()
        self.entity = pygame.sprite.Group()

        self.generate()
        self.ui = UI()


    #  makes a numerical grid from an array
    def generate(self):
        enemies = []
        for y, row in enumerate(ROOMS[0]):
            y *= 48
            for x, col in enumerate(row):
                x *= 48
                if col == 'W':
                    Wall((x, y), [self.obstruction, self.sprite])
                else:
                    Floor((x, y), [self.environment, self.sprite])
                if col == 'S':
                    enemies.append([(x, y), 'slime'])
                elif col == 'Z':
                    enemies.append([(x, y), 'zombie'])
                elif col == 'K':
                    enemies.append([(x, y), 'skeleton'])
                elif col == 'B':
                    enemies.append([(x, y), 'vampire'])

        self.player = Player(start, [self.sprite], self.obstruction)

        for i in enemies:
            self.enemy = (Enemy(i[0], [self.sprite], i[1], self.obstruction))

    def run(self):
        self.time = self.time = pygame.time.get_ticks()
        self.sprite.draw(self.screen)
        self.sprite.update(self.player, self.enemy)
        self.ui.show(self.player.health, self.player.shield, self.time)