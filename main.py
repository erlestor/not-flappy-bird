import pygame
import random

from constants import WIDTH, HEIGHT
from sprites.player import Player
from sprites.pipe import Pipe
from sprites.score_hitbox import ScoreHitbox

# pygame setup
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
vec = pygame.math.Vector2
running = True

# images
bg = pygame.image.load("images/background.jpg")

gameStarted = False
gameOver = False
difficulty = 1
last_game_ended = 0

player = Player()

pipes = pygame.sprite.Group()
score_hitboxes = pygame.sprite.Group()

def spawnPipe():
    height = random.randint(300, 600)
    bottomPipe = Pipe(height, bottom=True)
    topPipe = Pipe(height - 250, bottom=False)
    pipes.add(bottomPipe)
    pipes.add(topPipe)

    score_hitbox = ScoreHitbox()
    score_hitboxes.add(score_hitbox)


# events
spawnEvent = pygame.USEREVENT+1
pygame.time.set_timer(spawnEvent, 1000 - ((difficulty - 1) * 100))

difficultyEvent = pygame.USEREVENT+2
pygame.time.set_timer(difficultyEvent, 10000)

def restart(): 
    global player, gameStarted, gameOver, difficulty, clock, last_game_ended

    gameStarted = False
    gameOver = False
    difficulty = 1
    player = Player()
    pipes.empty()
    # reset time

while running:
    # poll for events
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not gameStarted:
            gameStarted = True
        if event.type == spawnEvent and not gameOver and gameStarted:
            spawnPipe()
        if event.type == difficultyEvent and not gameOver and gameStarted:
            difficulty += 0.1

    # background image
    screen.blit(bg, (0, 0))

    # draw entities
    screen.blit(player.image, player.rect)
    # uncomment to test hitbox
    # screen.blit(player.hitbox_surf, player.hitbox)
    for pipe in pipes:
        screen.blit(pipe.surf, pipe.rect)
    for score_hitbox in score_hitboxes:
        screen.blit(score_hitbox.surf, score_hitbox.rect)

    # game over state
    if gameOver:
        font = pygame.font.Font(None, 50)
        text = font.render("You suck! Press space to restart or e to exit", True, (0, 0, 0))
        text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
        screen.blit(text, text_rect)

        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                restart()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                running = False

    if gameStarted and not gameOver:
        player.move(events, gameStarted)
        for pipe in pipes:
            pipe.move(difficulty)

    # game over state
    for pipe in pipes:
        if player.hitbox.colliderect(pipe.rect):
            gameOver = True
    if player.pos.y >= 700 and player.vel.y >= 0:
        gameOver = True

    # flip() the display to put your work on screen
    pygame.display.flip()
    # limit to 60 fps
    clock.tick(60)


pygame.quit()
