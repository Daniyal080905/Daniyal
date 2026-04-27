import pygame
from clock import MickeyClock

pygame.init()

WIDTH, HEIGHT = 900, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mickey Clock")

game_clock = pygame.time.Clock()
mickey_clock = MickeyClock(screen)

running = True

while running:
    game_clock.tick(1)  # update every second

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    mickey_clock.draw()
    pygame.display.update()

pygame.quit()