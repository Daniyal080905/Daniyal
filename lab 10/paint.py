import pygame

pygame.init()

# Screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

current_color = BLACK  # current drawing color

# Modes
mode = "DRAW"  # DRAW / RECT / CIRCLE / ERASER

# Variables
drawing = False
start_pos = None

screen.fill(WHITE)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Mouse pressed
        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            start_pos = event.pos

        # Mouse released
        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False

            end_pos = event.pos

            # Draw rectangle
            if mode == "RECT":
                x1, y1 = start_pos
                x2, y2 = end_pos
                rect = pygame.Rect(x1, y1, x2 - x1, y2 - y1)
                pygame.draw.rect(screen, current_color, rect, 2)

            # Draw circle
            if mode == "CIRCLE":
                x1, y1 = start_pos
                x2, y2 = end_pos
                radius = int(((x2 - x1)**2 + (y2 - y1)**2)**0.5)
                pygame.draw.circle(screen, current_color, start_pos, radius, 2)

        # Keyboard controls
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                current_color = BLACK
            if event.key == pygame.K_2:
                current_color = RED
            if event.key == pygame.K_3:
                current_color = BLUE
            if event.key == pygame.K_4:
                current_color = GREEN

            # Modes
            if event.key == pygame.K_d:
                mode = "DRAW"
            if event.key == pygame.K_r:
                mode = "RECT"
            if event.key == pygame.K_c:
                mode = "CIRCLE"
            if event.key == pygame.K_e:
                mode = "ERASER"

    # Drawing with mouse (free draw)
    if drawing:
        mouse_pos = pygame.mouse.get_pos()

        if mode == "DRAW":
            pygame.draw.circle(screen, current_color, mouse_pos, 5)

        # Eraser (draw white)
        if mode == "ERASER":
            pygame.draw.circle(screen, WHITE, mouse_pos, 10)

    pygame.display.update()

pygame.quit()