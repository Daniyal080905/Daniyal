import pygame
import math

pygame.init()

# Screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint Advanced")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

current_color = BLACK

# Modes
mode = "DRAW"  # DRAW / SQUARE / TRIANGLE_R / TRIANGLE_E / RHOMBUS

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

        # Mouse released -> draw shapes
        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            end_pos = event.pos

            x1, y1 = start_pos
            x2, y2 = end_pos

            # 🔲 Square (равные стороны)
            if mode == "SQUARE":
                side = max(abs(x2 - x1), abs(y2 - y1))
                pygame.draw.rect(screen, current_color, (x1, y1, side, side), 2)

            # 🔺 Right triangle (прямоугольный)
            if mode == "TRIANGLE_R":
                points = [(x1, y1), (x2, y1), (x1, y2)]
                pygame.draw.polygon(screen, current_color, points, 2)

            # 🔺 Equilateral triangle (равносторонний)
            if mode == "TRIANGLE_E":
                side = abs(x2 - x1)
                height = side * math.sqrt(3) / 2

                points = [
                    (x1, y1),
                    (x1 + side, y1),
                    (x1 + side / 2, y1 - height)
                ]
                pygame.draw.polygon(screen, current_color, points, 2)

            # 🔷 Rhombus (ромб)
            if mode == "RHOMBUS":
                cx = (x1 + x2) // 2
                cy = (y1 + y2) // 2

                points = [
                    (cx, y1),
                    (x2, cy),
                    (cx, y2),
                    (x1, cy)
                ]
                pygame.draw.polygon(screen, current_color, points, 2)

        # Keyboard
        if event.type == pygame.KEYDOWN:
            # Colors
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
            if event.key == pygame.K_q:
                mode = "SQUARE"
            if event.key == pygame.K_t:
                mode = "TRIANGLE_R"
            if event.key == pygame.K_e:
                mode = "TRIANGLE_E"
            if event.key == pygame.K_r:
                mode = "RHOMBUS"

    # Free draw (кисть)
    if drawing and mode == "DRAW":
        mouse_pos = pygame.mouse.get_pos()
        pygame.draw.circle(screen, current_color, mouse_pos, 4)

    pygame.display.update()

pygame.quit()