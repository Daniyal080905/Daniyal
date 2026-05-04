import pygame
from collections import deque
from datetime import datetime


def save_canvas(canvas):
    filename = f"paint_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    pygame.image.save(canvas, filename)
    print(f"Saved as {filename}")


def draw_square(surface, color, start, end, width):
    x1, y1 = start
    x2, y2 = end
    size = min(abs(x2 - x1), abs(y2 - y1))

    x = x1 if x2 >= x1 else x1 - size
    y = y1 if y2 >= y1 else y1 - size

    pygame.draw.rect(surface, color, (x, y, size, size), width)


def draw_rectangle(surface, color, start, end, width):
    x1, y1 = start
    x2, y2 = end

    rect = pygame.Rect(
        min(x1, x2),
        min(y1, y2),
        abs(x2 - x1),
        abs(y2 - y1)
    )

    pygame.draw.rect(surface, color, rect, width)


def draw_circle(surface, color, start, end, width):
    x1, y1 = start
    x2, y2 = end

    radius = int(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5)

    pygame.draw.circle(surface, color, start, radius, width)


def draw_right_triangle(surface, color, start, end, width):
    x1, y1 = start
    x2, y2 = end

    points = [
        (x1, y1),
        (x1, y2),
        (x2, y2)
    ]

    pygame.draw.polygon(surface, color, points, width)


def draw_equilateral_triangle(surface, color, start, end, width):
    x1, y1 = start
    x2, y2 = end

    side = x2 - x1
    height = int(abs(side) * 0.866)

    points = [
        (x1, y2),
        (x2, y2),
        ((x1 + x2) // 2, y2 - height)
    ]

    pygame.draw.polygon(surface, color, points, width)


def draw_rhombus(surface, color, start, end, width):
    x1, y1 = start
    x2, y2 = end

    center_x = (x1 + x2) // 2
    center_y = (y1 + y2) // 2

    points = [
        (center_x, y1),
        (x2, center_y),
        (center_x, y2),
        (x1, center_y)
    ]

    pygame.draw.polygon(surface, color, points, width)


def flood_fill(surface, start_pos, fill_color):
    width, height = surface.get_size()

    target_color = surface.get_at(start_pos)
    fill_color = pygame.Color(fill_color)

    if target_color == fill_color:
        return

    queue = deque()
    queue.append(start_pos)

    while queue:
        x, y = queue.popleft()

        if x < 0 or x >= width or y < 0 or y >= height:
            continue

        if surface.get_at((x, y)) != target_color:
            continue

        surface.set_at((x, y), fill_color)

        queue.append((x + 1, y))
        queue.append((x - 1, y))
        queue.append((x, y + 1))
        queue.append((x, y - 1))