import pygame 
from random import randint
from time import *

FPS = 40
BG_COLOR = (200,255,255)
pygame.init()
window = pygame.display.set_mode((500,500))
window.fill(BG_COLOR)
clock = pygame.time.Clock()

BLACK = (0,0,0)
GREEN = (0,255,0)
YELLOW = (255,255,0)
BLUE = (0,0,255)
RED = (255,0,0)


class Game():
    run = True
    finish = False
    events = None
    button = None
    pos = None
    def update(self):
        self.events = pygame.event.get()
        for event in self.events:
            if event.type == pygame.QUIT:
                self.run = False
                






game = Game()

while game.run:
    game.update()



    clock.tick(FPS)
    pygame.display.update()


