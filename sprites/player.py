import pygame
from constants import GRAVITY

vec = pygame.math.Vector2
birdImg = pygame.image.load("images/bird.png")

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.surf = pygame.Surface((100, 70))
        self.rect = self.surf.get_rect()

        self.hitbox_surf = pygame.Surface((75, 60))
        self.hitbox = self.hitbox_surf.get_rect()

        self.original_image = pygame.transform.scale(birdImg,(100, 65))
        self.image = self.original_image

        self.pos = vec((500, 400))
        self.vel = vec(0,0)
        self.rect.midbottom = self.pos
        self.hitbox.midbottom = self.pos
    
    def move(self, events, gameStarted):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and gameStarted:
                self.vel.y = -14

        self.vel.y += GRAVITY

        if self.pos.y <= 50 and self.vel.y <= 0:
            return

        self.pos += self.vel
        self.rect.midbottom = self.pos
        self.hitbox.midbottom = self.pos

        rotation = -self.vel.y * 2
        self.image = pygame.transform.rotate(self.original_image, rotation)