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

# images
bg = pygame.image.load("images/background.jpg")

running = True
game_started = False
game_over = False
difficulty = 1
last_game_ended = 0

player = Player()

pipes = pygame.sprite.Group()
score_hitboxes = pygame.sprite.Group()


def spawn_pipe():
    height = random.randint(300, 600)
    bottom_pipe = Pipe(height, bottom=True)
    top_pipe = Pipe(height - 250, bottom=False)
    pipes.add(bottom_pipe)
    pipes.add(top_pipe)

    score_hitbox = ScoreHitbox()
    score_hitboxes.add(score_hitbox)


# events
spawn_event = pygame.USEREVENT + 1
pygame.time.set_timer(spawn_event, 1000 - ((difficulty - 1) * 100))

difficulty_event = pygame.USEREVENT + 3
pygame.time.set_timer(difficulty_event, 10000)


def restart():
    global player, game_started, game_over, difficulty, clock, last_game_ended

    game_started = False
    game_over = False
    difficulty = 1
    player = Player()
    pipes.empty()
    # TODO: reset time


while running:
    # poll for events
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        if (
            event.type == pygame.KEYDOWN
            and event.key == pygame.K_SPACE
            and not game_started
        ):
            game_started = True
        if event.type == spawn_event and not game_over and game_started:
            spawn_pipe()
        if event.type == difficulty_event and not game_over and game_started:
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
    if game_over:
        font = pygame.font.Font(None, 50)
        text = font.render(
            "You suck! Press space to restart or e to exit", True, (0, 0, 0)
        )
        text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        screen.blit(text, text_rect)

        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                restart()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                running = False

    if game_started and not game_over:
        player.move(events, game_started)
        for pipe in pipes:
            pipe.move(difficulty)

    # game over state
    for pipe in pipes:
        if player.hitbox.colliderect(pipe.rect):
            game_over = True
    if player.pos.y >= 700 and player.vel.y >= 0:
        game_over = True

    pygame.display.flip()
    clock.tick(60)


pygame.quit()
