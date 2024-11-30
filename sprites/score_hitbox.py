import pygame
from constants import WIDTH

vec = pygame.math.Vector2


class ScoreHitbox(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((50, 1000))
        self.rect = self.surf.get_rect()

        self.pos = vec((WIDTH + 60, 0))
        self.vel = vec(0, 0)

        self.rect.center = self.pos

    def move(self, difficulty):
        self.pos.x -= 7 * difficulty

        self.rect.center = self.pos

