import pygame
from constants import WIDTH

vec = pygame.math.Vector2


class Pipe(pygame.sprite.Sprite):
    def __init__(self, height, bottom: bool):
        super().__init__()
        self.surf = pygame.Surface((100, 1000))
        self.surf.fill((3, 163, 46))
        self.rect = self.surf.get_rect()
        self.bottom = bottom

        self.pos = vec((WIDTH + 50, height))
        self.vel = vec(0, 0)
        if bottom:
            self.rect.midtop = self.pos
        else:
            self.rect.midbottom = self.pos

    def move(self, difficulty):
        self.pos.x -= 7 * difficulty

        if self.bottom:
            self.rect.midtop = self.pos
        else:
            self.rect.midbottom = self.pos

