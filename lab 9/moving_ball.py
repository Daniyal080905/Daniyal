import pygame
import sys

pygame.init()

# Screen settings
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Ball Game")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Ball settings
radius = 25
x = WIDTH // 2
y = HEIGHT // 2
step = 20

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Keyboard control
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if y - step - radius >= 0:
                    y -= step

            elif event.key == pygame.K_DOWN:
                if y + step + radius <= HEIGHT:
                    y += step

            elif event.key == pygame.K_LEFT:
                if x - step - radius >= 0:
                    x -= step

            elif event.key == pygame.K_RIGHT:
                if x + step + radius <= WIDTH:
                    x += step

    # Draw
    screen.fill(WHITE)
    pygame.draw.circle(screen, RED, (x, y), radius)

    pygame.display.update()
    clock.tick(60)